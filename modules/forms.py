# -*- coding: utf-8 -*-

from bcrypt import gensalt, hashpw
from flask import g, session
from flask_wtf import Form
from wtforms.fields import PasswordField, TextField

from modules import models, validators


class sign_in(Form):

    username = TextField(validators=[validators.required()])
    password = PasswordField(validators=[validators.required()])

    def validate(self):
        if super(sign_in, self).validate():
            username = g.mysql.query(models.setting).filter(models.setting.key == 'username').first().value
            password = g.mysql.query(models.setting).filter(models.setting.key == 'password').first().value
            if (
                username == self.username.data
                and
                hashpw(self.password.data.encode('utf-8'), password.encode('utf-8')) == password
            ):
                session['administrator'] = True
                return True
        self.username.errors = ['Invalid Username/Password']
        self.password.errors = ['Invalid Username/Password']
        return False


class settings(Form):

    username = TextField(validators=[validators.required()])
    password = PasswordField(validators=[validators.required()])

    def persist(self):
        g.mysql.query(models.setting).filter(models.setting.key == 'username').update({
            'value': self.username.data,
        })
        g.mysql.query(models.setting).filter(models.setting.key == 'password').update({
            'value': hashpw(self.password.data.encode('utf-8'), gensalt(10)),
        })
        g.mysql.commit()
