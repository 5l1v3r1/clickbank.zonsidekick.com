# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.orm import backref, relationship
from sqlalchemy.types import TEXT, TypeDecorator
from ujson import dumps, loads

from modules import database


class json(TypeDecorator):

    impl = TEXT

    def process_bind_param(self, value, dialect):
        return dumps(value)

    def process_result_value(self, value, dialect):
        return loads(value)


class mutators_dict(Mutable, dict):

    @classmethod
    def coerce(class_, key, value):
        if not isinstance(value, mutators_dict):
            if isinstance(value, dict):
                return mutators_dict(value)
            return Mutable.coerce(key, value)
        return value

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self.changed()

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self.changed()


class mutators_list(Mutable, list):

    @classmethod
    def coerce(class_, key, value):
        if not isinstance(value, mutators_list):
            if isinstance(value, list):
                return mutators_list(value)
            return Mutable.coerce(key, value)
        return value

    def append(self, value):
        list.append(self, value)
        self.changed()

    def __add__(self, value):
        list.__add__(self, value)
        self.changed()

    def __delitem__(self, index):
        list.__delitem__(self, index)
        self.changed()

    def __setitem__(self, key, value):
        list.__setitem__(self, key, value)
        self.changed()


class setting(database.base):

    __tablename__ = 'settings'
    __table_args__ = {
        'autoload': True,
    }


class customer(database.base):

    __tablename__ = 'customers'
    __table_args__ = {
        'autoload': True,
    }

    address = Column(mutators_dict.as_mutable(json))

    def get_amount(self):
        return sum([order.amounts_order for order in self.orders.order_by('timestamp DESC').all()])


class order(database.base):

    __tablename__ = 'orders'
    __table_args__ = {
        'autoload': True,
    }

    customer = relationship('customer', backref=backref('orders', cascade='all,delete-orphan', lazy='dynamic'))

    tracking_codes = Column(mutators_list.as_mutable(json))
    vendor_variables = Column(mutators_dict.as_mutable(json))

    def get_role(self):
        if self.role == 'AFFILIATE':
            return self.affiliate
        return self.vendor


class order_product(database.base):

    __tablename__ = 'orders_products'
    __table_args__ = {
        'autoload': True,
    }

    order = relationship('order', backref=backref('orders_products', cascade='all,delete-orphan', lazy='dynamic'))
