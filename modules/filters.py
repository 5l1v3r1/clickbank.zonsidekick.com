# -*- coding: utf-8 -*-

from flask import g
from flask_wtf import Form
from wtforms.fields import SelectField, TextField

from modules import models


class customers(Form):

    email = TextField()
    name = TextField()

    def apply(self, query):
        if self.email.data:
            query = query.filter(models.customer.email.like('%%%(email)s%%' % {
                'email': self.email.data,
            }))
        if self.name.data:
            query = query.filter(models.customer.name.like('%%%(name)s%%' % {
                'name': self.name.data,
            }))
        return query


class orders(Form):

    customer = SelectField(choices=[], default='')
    receipt = TextField()
    type = SelectField(
        choices=[
            ('', 'All',),
            ('SALE', 'SALE',),
            ('RFND', 'RFND',),
            ('CGBK', 'CGBK',),
            ('FEE', 'FEE',),
            ('BILL', 'BILL',),
            ('TEST_SALE', 'TEST_SALE',),
            ('TEST_BILL', 'TEST_BILL',),
            ('TEST_RFND', 'TEST_RFND',),
            ('TEST_FEE', 'TEST_FEE',),
        ],
        default='',
    )
    role = TextField()
    affiliate = TextField()
    payment_method = TextField(label='Payment Method')
    vendor = TextField()

    def __init__(self, *args, **kwargs):
        super(orders, self).__init__(*args, **kwargs)
        self.customer.choices = [('', 'All')] + [
            (customer.id, customer.name)
            for customer in g.mysql.query(models.customer).order_by('id desc').all()
        ]

    def apply(self, query):
        if self.receipt.data:
            query = query.filter(models.order.receipt.like('%%%(receipt)s%%' % {
                'receipt': self.receipt.data,
            }))
        if self.type.data:
            query = query.filter(models.order.type == self.type.data)
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
