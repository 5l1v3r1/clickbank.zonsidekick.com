# -*- coding: utf-8 -*-

from flask import g
from flask_wtf import Form
from wtforms.fields import SelectField, TextField

from modules import models


class customers(Form):

    email = TextField()
    full_name = TextField(label='Full Name')

    def apply(self, query):
        if self.email.data:
            query = query.filter(models.customer.email.like('%%%(email)s%%' % {
                'email': self.email.data,
            }))
        if self.full_name.data:
            query = query.filter(models.customer.full_name.like('%%%(full_name)s%%' % {
                'full_name': self.full_name.data,
            }))
        return query


class orders(Form):

    customer = SelectField(choices=[], default='')
    receipt = TextField()
    type = TextField()
    role = TextField()
    affiliate = TextField()
    payment_method = TextField(label='Payment Method')
    vendor = TextField()

    def __init__(self, *args, **kwargs):
        super(orders, self).__init__(*args, **kwargs)
        self.customer.choices = [('', 'All')] + [
            (customer.id, customer.full_name)
            for customer in g.mysql.query(models.customer).order_by('full_name asc').all()
        ]

    def apply(self, query):
        if self.receipt.data:
            query = query.filter(models.order.receipt.like('%%%(receipt)s%%' % {
                'receipt': self.receipt.data,
            }))
        if self.type.data:
            query = query.filter(models.order.type.like('%%%(type)s%%' % {
                'type': self.type.data,
            }))
        if self.role.data:
            query = query.filter(models.order.role.like('%%%(role)s%%' % {
                'role': self.role.data,
            }))
        if self.affiliate.data:
            query = query.filter(models.order.affiliate.like('%%%(affiliate)s%%' % {
                'affiliate': self.affiliate.data,
            }))
        if self.payment_method.data:
            query = query.filter(models.order.payment_method.like('%%%(payment_method)s%%' % {
                'payment_method': self.payment_method.data,
            }))
        if self.vendor.data:
            query = query.filter(models.order.vendor.like('%%%(vendor)s%%' % {
                'vendor': self.vendor.data,
            }))
        return query
