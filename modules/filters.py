# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms.fields import TextField

from modules import models, validators


class customers(Form):
    email = TextField(validators=[
        validators.required(),
    ])
    first_name = TextField(label='First Name', validators=[
        validators.required(),
    ])
    last_name = TextField(label='Last Name', validators=[
        validators.required(),
    ])

    def apply(self, query):
        if self.email.data:
            query = query.filter(models.customer.email.like('%%%(email)s%%' % {
                'email': self.email.data,
            }))
        if self.first_name.data:
            query = query.filter(models.customer.first_name.like('%%%(first_name)s%%' % {
                'first_name': self.first_name.data,
            }))
        if self.last_name.data:
            query = query.filter(models.customer.last_name.like('%%%(last_name)s%%' % {
                'last_name': self.last_name.data,
            }))
        return query


class orders(Form):
    type = TextField(label='Type', validators=[
        validators.required(),
    ])

    def apply(self, query):
        if self.type.data:
            query = query.filter(models.order.type.like('%%%(type)s%%' % {
                'type': self.type.data,
            }))
        return query
