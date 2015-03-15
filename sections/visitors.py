# -*- coding: utf-8 -*-

from hashlib import sha1

from Crypto.Cipher import AES
from flask import Blueprint, g, redirect, request
from ujson import loads

from modules import models

from settings import CLICKBANK

blueprint = Blueprint('visitors', __name__)


@blueprint.route('/')
def dashboard():
    return redirect('administrators.dashboard')


@blueprint.route('/notify', methods=['POST'])
def instant_notification():
    message = loads(request.data)
    algorithm = sha1()
    algorithm.update(CLICKBANK)
    dictionary = loads(''.join([
        character
        for character in AES.new(
            algorithm.hexdigest()[:32], AES.MODE_CBC, message['iv'].decode('base64')
        ).decrypt(
            message['notification'].decode('base64')
        ).strip()
        if ord(character) >= 32
    ]))
    customer = g.mysql.query(models.customer).filter(email=dictionary['customer']['billing']['email']).first()
    if not customer:
        customer = models.customer(**{
            'address': ', '.join([
                '%(key)s: %(value)s' % {
                    'key': key, 'value': value
                }
                for key, value in dictionary['customer']['billing']['address'].iteritems()
            ]),
            'email': dictionary['customer']['billing']['email'],
            'first_name': dictionary['customer']['billing']['firstName'],
            'full_name': dictionary['customer']['billing']['fullName'],
            'last_name': dictionary['customer']['billing']['lastName'],
        })
    g.mysql.add(customer)
    order = models.order(**{
        'amounts_account': dictionary['totalAccountAmount'],
        'amounts_order': dictionary['totalOrderAmount'],
        'amounts_shipping': dictionary['totalShippingAmount'],
        'amounts_tax': dictionary['totalTaxAmount'],
        'attempts': dictionary['attemptCount'],
        'currency': dictionary['currency'],
        'customer': customer,
        'language': dictionary['orderLanguage'],
        'payment_method': dictionary['paymentMethod'],
        'receipt': dictionary['receipt'],
        'role': dictionary['role'],
        'timestamp': dictionary['transactionTime'],
        'type': dictionary['transactionType'],
        'vendor': dictionary['vendor'],
        'version': dictionary['version'],
    })
    g.mysql.add(order)
    for item in dictionary['lineItems']:
        g.mysql.add(models.order_product(**{
            'amount': item['accountAmount'],
            'item_number': item['itemNo'],
            'order': order,
            'recurring': item['recurring'],
            'shippable': item['shippable'],
            'title': item['productTitle'],
            'url': item['downloadUrl'],
        }))
    g.mysql.commit()
    return ('', 204)
