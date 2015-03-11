# -*- coding: utf-8 -*-

from datetime import datetime

from flask import g
from sqlalchemy.orm import backref, relationship

from modules import database


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


class order(database.base):
    __tablename__ = 'orders'
    __table_args__ = {
        'autoload': True,
    }


class order_product(database.base):
    __tablename__ = 'orders_products'
    __table_args__ = {
        'autoload': True,
    }

    order = relationship(
        'order', backref=backref('orders_products', cascade='all,delete-orphan', lazy='dynamic'),
    )
