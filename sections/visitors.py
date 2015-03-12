# -*- coding: utf-8 -*-

from hashlib import sha1

from Crypto.Cipher import AES
from flask import Blueprint, g, render_template, request
from ujson import loads

from modules import models
from settings import CLICKBANK_SECRET_KEY

blueprint = Blueprint('visitors', __name__)


@blueprint.route('/')
def dashboard():
    return render_template('visitors/views/dashboard.html')


@blueprint.route('/instant-notification', methods=['POST'])
def instant_notification():
    message = loads(request.data)
    iv = message['iv']
    encrypted_string = message['notification']
    sha1_ = sha1()
    sha1_.update(CLICKBANK_SECRET_KEY)
    cipher = AES.new(sha1_.hexdigest()[:32], AES.MODE_CBC, iv.decode('base64'))
    decrypted_string = cipher.decrypt(
        encrypted_string.decode('base64')
    ).strip()
    decrypted_string = loads(''.join([
        character for character in decrypted_string if ord(character) >= 32
    ]))
    order = models.order(**{
        'amounts_account': decrypted_string['lineItems'][0]['accountAmount'],
        'amounts_order': decrypted_string['totalOrderAmount'],
        'amounts_shipping': decrypted_string['totalShippingAmount'],
        'amounts_tax': decrypted_string['totalTaxAmount'],
        'attempts': decrypted_string['attemptCount'],
        'currency': decrypted_string['currency'],
        'language': decrypted_string['orderLanguage'],
        'payment_method': decrypted_string['paymentMethod'],
        'receipt': decrypted_string['receipt'],
        'role': decrypted_string['role'],
        'timestamp': decrypted_string['transactionTime'],
        'type': decrypted_string['transactionType'],
        'vendor': decrypted_string['vendor'],
        'version': decrypted_string['version'],
    })
    g.mysql.add(order)
    g.mysql.add(models.order_product(**{
        'amount': decrypted_string['lineItems'][0]['accountAmount'],
        'item_number': decrypted_string['lineItems'][0]['itemNo'],
        'order': order,
        'recurring': decrypted_string['lineItems'][0]['recurring'],
        'shippable': decrypted_string['lineItems'][0]['shippable'],
        'title': decrypted_string['lineItems'][0]['productTitle'],
        'url': decrypted_string['lineItems'][0]['downloadUrl'],
    }))
    g.mysql.add(models.customer(**{
        'address': ', '.join([
            '%(key)s: %(value)s' % {'key': key, 'value': value}
            for key, value in decrypted_string['customer']['billing']['address'].iteritems()
        ]),
        'email': decrypted_string['customer']['billing']['email'],
        'first_name': decrypted_string['customer']['billing']['firstName'],
        'full_name': decrypted_string['customer']['billing']['fullName'],
        'last_name': decrypted_string['customer']['billing']['lastName'],
    }))
    g.mysql.commit()
    return '200'
