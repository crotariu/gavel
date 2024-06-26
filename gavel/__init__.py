# Copyright (c) 2015-2019 Anish Athalye (me@anishathalye.com)
#
# This software is released under AGPLv3. See the included LICENSE.txt for
# details.

from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

import gavel.settings as settings
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = settings.SECRET_KEY

from flask_assets import Environment, Bundle
assets = Environment(app)
assets.config['pyscss_style'] = 'expanded'
assets.url = app.static_url_path
scss = Bundle(
    'css/style.scss',
    depends='**/*.scss',
    filters=('pyscss',),
    output='all.css'
)
assets.register('scss_all', scss)

from celery import Celery
app.config['CELERY_BROKER_URL'] = settings.BROKER_URI
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from gavel.models import db
db.app = app
db.init_app(app)

import gavel.template_filters # registers template filters

import gavel.controllers # registers controllers
