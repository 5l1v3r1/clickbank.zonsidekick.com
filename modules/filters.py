# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms.fields import TextField

from modules import models


class customers(Form):
    email = TextField()
    full_name = TextField(label='Full Name')

    def apply(self, query):
        if self.email.data:
            query = query.filter(
                models.customer.email.like(
                    '%%%(email)s%%' % {
                        'email': self.email.data,
                    }
                )
            )
        if self.full_name.data:
            query = query.filter(
                models.customer.full_name.like(
                    '%%%(full_name)s%%' % {
                        'full_name': self.full_name.data,
                    }
                )
            )
        return query


class orders(Form):
    receipt = TextField()
    type = TextField()
    role = TextField()
    affiliate = TextField()
    payment_method = TextField(label='Payment Method')
    vendor = TextField()

    def apply(self, query):
        if self.receipt.data:
            query = query.filter(
                models.order.receipt.like(
                    '%%%(receipt)s%%' % {
                        'receipt': self.receipt.data,
                    }
                )
            )
        if self.type.data:
            query = query.filter(
                models.order.type.like(
                    '%%%(type)s%%' % {
                        'type': self.type.data,
                    }
                )
            )
        if self.role.data:
            query = query.filter(
                models.order.role.like(
                    '%%%(role)s%%' % {
                        'role': self.role.data,
                    }
                )
            )
        if self.affiliate.data:
            query = query.filter(
                models.order.affiliate.like(
                    '%%%(affiliate)s%%' % {
                        'affiliate': self.affiliate.data,
                    }
                )
            )
        if self.payment_method.data:
            query = query.filter(
                models.order.payment_method.like(
                    '%%%(payment_method)s%%' % {
                        'payment_method': self.payment_method.data,
                    }
                )
            )
        if self.vendor.data:
            query = query.filter(
                models.order.vendor.like(
                    '%%%(vendor)s%%' % {
                        'vendor': self.vendor.data,
                    }
                )
            )
        return query
