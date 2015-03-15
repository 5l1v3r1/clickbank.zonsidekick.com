# -*- coding: utf-8 -*-

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from modules import classes, decorators, filters, forms, models, utilities

blueprint = Blueprint('administrators', __name__)


@blueprint.before_request
def before_request():
    g.administrator = False
    if 'administrator' in session:
        g.administrator = True


@blueprint.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if g.administrator:
        return redirect(request.args.get('next') or url_for('administrators.dashboard'))
    form = forms.sign_in(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            flash('You have been signed in successfully.', 'success')
            return redirect(request.args.get('next') or url_for('administrators.dashboard'))
        flash('You have not been signed in successfully.', 'danger')
    return render_template('administrators/views/sign_in.html', form=form)


@blueprint.route('/sign-out')
def sign_out():
    if 'administrator' in session:
        del session['administrator']
    flash('You have been signed out successfully.', 'success')
    return redirect(url_for('administrators.dashboard'))


@blueprint.route('/settings', methods=['GET', 'POST'])
@decorators.requires_administrator
def settings():
    form = forms.settings(
        request.form,
        username=g.mysql.query(models.setting).filter(models.setting.key == 'username').first().value,
    )
    if request.method == 'POST':
        if form.validate_on_submit():
            form.persist()
            flash('Your settings have been saved successfully.', 'success')
            return redirect(url_for('administrators.settings'))
        flash('Your settings have not been saved successfully.', 'danger')
    return render_template('administrators/views/settings.html', form=form)


@blueprint.route('/')
@decorators.requires_administrator
def dashboard():
    return render_template(
        'administrators/views/dashboard.html',
        customers=utilities.get_integer(g.mysql.query(models.customer).count()),
        orders=utilities.get_integer(g.mysql.query(models.order).count()),
    )


@blueprint.route('/customers/overview')
@decorators.requires_administrator
def customers_overview():
    filters_, order_by, limit, page = utilities.get_filters_order_by_limit_page(
        'customers',
        {},
        {
            'column': 'full_name',
            'direction': 'asc',
        },
        10,
        1
    )
    form = filters.customers(**filters_)
    query = form.apply(g.mysql.query(models.customer))
    pager = classes.pager(query.count(), limit, page)
    return render_template(
        'administrators/views/customers_overview.html',
        customers=query.order_by('%(column)s %(direction)s' % order_by).all()[pager.prefix:pager.suffix],
        form=form,
        order_by=order_by,
        pager=pager,
    )


@blueprint.route('/customers/process', methods=['GET', 'POST'])
@decorators.requires_administrator
def customers_process():
    if request.method == 'GET':
        utilities.set_order_by_limit_page('customers')
    if request.method == 'POST':
        utilities.set_filters('customers', filters.customers)
    return redirect(url_for('administrators.customers_overview'))


@blueprint.route('/orders/overview')
@decorators.requires_administrator
def orders_overview():
    filters_, order_by, limit, page = utilities.get_filters_order_by_limit_page(
        'orders',
        {},
        {
            'column': 'timestamp',
            'direction': 'desc',
        },
        10,
        1
    )
    form = filters.orders(**filters_)
    query = form.apply(g.mysql.query(models.order))
    pager = classes.pager(query.count(), limit, page)
    return render_template(
        'administrators/views/orders_overview.html',
        form=form,
        order_by=order_by,
        orders=query.order_by('%(column)s %(direction)s' % order_by).all()[pager.prefix:pager.suffix],
        pager=pager,
    )


@blueprint.route('/orders/process', methods=['GET', 'POST'])
@decorators.requires_administrator
def orders_process():
    if request.method == 'GET':
        utilities.set_order_by_limit_page('orders')
    if request.method == 'POST':
        utilities.set_filters('orders', filters.orders)
    return redirect(url_for('administrators.orders_overview'))
