# -*- coding: utf-8 -*-

from datetime import datetime
from os.path import abspath, dirname, join, realpath

from flask import Flask, g, got_request_exception, send_from_directory, session, url_for
from flask.ext.assets import Bundle, Environment
from rollbar import init
from rollbar.contrib.flask import report_exception

from modules import database, utilities

from sections import administrators, others, visitors

from settings import ROLLBAR

application = Flask(__name__, static_folder=join(abspath(dirname(__file__)), 'resources'))
application.config.from_pyfile('settings.py')
application.jinja_env.add_extension('jinja2.ext.do')
application.jinja_env.add_extension('jinja2.ext.loopcontrols')
application.jinja_env.add_extension('jinja2.ext.with_')
application.register_blueprint(administrators.blueprint, url_prefix='/administrators')
application.register_blueprint(others.blueprint, url_prefix='/others')
application.register_blueprint(visitors.blueprint)


def url_for_(rule, **kwargs):
    kwargs.setdefault('_external', True)
    return url_for(rule, **kwargs)

application.jinja_env.globals['url_for'] = url_for_

assets = Environment(application)
assets.cache = False
assets.debug = application.config['DEBUG']
assets.directory = application.static_folder
assets.manifest = 'json:assets/versions.json'
assets.url = application.static_url_path
assets.url_expire = True
assets.versions = 'hash'
assets.register(
    'javascripts',
    Bundle(
        'vendors/jquery/dist/jquery.js',
        'vendors/bootstrap/dist/js/bootstrap.js',
        'javascripts/all.js',
        filters='rjsmin' if not application.config['DEBUG'] else None,
        output='assets/compressed.js',
    )
)
assets.register(
    'stylesheets',
    Bundle(
        Bundle('stylesheets/all.less', filters='less', output='stylesheets/all.css'),
        filters='cssmin,cssrewrite'if not application.config['DEBUG'] else None,
        output='assets/compressed.css',
    )
)


@application.before_first_request
def init_rollbar():
    init(
        ROLLBAR['access_token'],
        ROLLBAR['environment'],
        allow_logging_basic_config=False,
        root=dirname(realpath(__file__)),
    )
    got_request_exception.connect(report_exception, application)


@application.before_request
def before_request():
    g.mysql = database.session()
    g.year = datetime.now().strftime('%Y')
    session.permanent = True


@application.after_request
def after_request(response):
    g.mysql.close()
    return response


@application.route('/404')
@application.errorhandler(404)
def errors_404(error=None):
    return others.errors_404(error)


@application.route('/500')
@application.errorhandler(500)
def errors_500(error=None):
    return others.errors_500(error)


@application.route('/favicon.ico')
def favicon():
    return send_from_directory(join(application.root_path, 'resources', 'images'), 'favicon.ico')


@application.template_filter('format_integer')
def format_integer(value):
    return utilities.get_integer(value)


@application.template_filter('format_float')
def format_float(value):
    return utilities.get_float(value)

if __name__ == '__main__':
    application.run()
