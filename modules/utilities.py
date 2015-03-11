# -*- coding: utf-8 -*-

from locale import LC_ALL, format, setlocale

from flask import request, session

setlocale(LC_ALL, 'en_US.UTF-8')


def get_filters_order_by_limit_page(table, filters, order_by, limit, page):
    if table not in session:
        session[table] = {}
    if 'filters' in session[table]:
        filters = session[table]['filters']
    if 'order_by' in session[table]:
        order_by = session[table]['order_by']
    if 'limit' in session[table]:
        limit = session[table]['limit']
    if 'page' in session[table]:
        page = session[table]['page']
    return filters, order_by, limit, page


def get_float(value):
    return format('%.2f', value, grouping=True)


def get_integer(value):
    return format('%d', value, grouping=True)


def set_filters(table, form):
    if table not in session:
        session[table] = {}
    if request.form.get('submit', default='') == 'set':
        session[table]['filters'] = form(request.form).data
        session[table]['page'] = 1
    if request.form.get('submit', default='') == 'unset':
        session[table]['filters'] = {}
        session[table]['page'] = 1


def set_order_by_limit_page(table):
    if table not in session:
        session[table] = {}
    if 'order_by_column' in request.args and 'order_by_direction' in request.args:
        session[table]['order_by'] = {
            'column': request.args['order_by_column'],
            'direction': request.args['order_by_direction'],
        }
    if 'limit' in request.args:
        session[table]['limit'] = int(request.args['limit'] or 0)
    if 'page' in request.args:
        session[table]['page'] = int(request.args['page'] or 0)
