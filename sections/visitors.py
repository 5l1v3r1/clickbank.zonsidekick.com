# -*- coding: utf-8 -*-

from hashlib import sha1

from Crypto.Cipher import AES
from flask import abort, Blueprint, g, redirect, request, url_for
from ujson import loads

from modules import models

from settings import CLICKBANK

blueprint = Blueprint('visitors', __name__)


@blueprint.route('/')
def dashboard():
    return redirect(url_for('administrators.dashboard'))


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
    customer_billing = {}
    try:
        customer_billing = dictionary['customer']['billing']
    except KeyError:
        pass
    email = customer_billing.get('email', '')
    if not email:
        abort(400)
    customer = g.mysql.query(models.customer).filter(email=email).first()
    if not customer:
        customer = models.customer(**{
            'address': customer_billing.get('address', ''),
            'email': email,
            'first_name': customer_billing.get('firstName', ''),
            'full_name': customer_billing.get('fullName', ''),
            'last_name': customer_billing.get('lastName', ''),
            'phone_number': customer_billing.get('phoneNumber', ''),
        })
    g.mysql.add(customer)
    order = models.order(**{
        'affiliate': dictionary.get('affiliate', ''),
        'amounts_account': dictionary.get('totalAccountAmount', 0.00),
        'amounts_order': dictionary.get('totalOrderAmount', 0.00),
        'amounts_shipping': dictionary.get('totalShippingAmount', 0.00),
        'amounts_tax': dictionary.get('totalTaxAmount', 0.00),
        'currency': dictionary.get('currency', ''),
        'customer': customer,
        'language': dictionary.get('orderLanguage', ''),
        'payment_method': dictionary.get('paymentMethod', ''),
        'receipt': dictionary.get('receipt', ''),
        'role': dictionary.get('role', ''),
        'timestamp': dictionary.get('transactionTime', ''),
        'tracking_codes': dictionary.get('trackingCodes', []),
        'type': dictionary.get('transactionType', ''),
        'vendor': dictionary.get('vendor', ''),
        'vendor_variables': dictionary.get('vendorVariables', {}),
    })
    g.mysql.add(order)
    for item in dictionary.get('lineItems', []):
        g.mysql.add(models.order_product(**{
            'amount': item.get('accountAmount', 0.00),
            'item_number': item.get('itemNo', ''),
            'order': order,
            'recurring': item.get('recurring', ''),
            'shippable': item.get('shippable', ''),
            'title': item.get('productTitle', ''),
            'url': item.get('downloadUrl', ''),
        }))
    g.mysql.commit()
    return ('', 204)
