# -*- coding: utf-8 -*-

from hashlib import sha1

from Crypto.Cipher import AES
from flask import Blueprint, render_template, request
from ujson import loads

from settings import CLICKBANK_SECRET_KEY

blueprint = Blueprint('visitors', __name__)


@blueprint.route('/')
def dashboard():
    return render_template('visitors/views/dashboard.html')


@blueprint.route('/instant-notification', methods=['POST'])
def instant_notification():
    message = loads(request.data)
    iv = message['iv']
    encrypted_str = message['notification']
    sha1_ = sha1()
    sha1_.update(CLICKBANK_SECRET_KEY)
    cipher = AES.new(sha1_.hexdigest()[:32], AES.MODE_CBC, iv.decode('base64'))
    print cipher.decrypt(encrypted_str.decode('base64')).strip()
