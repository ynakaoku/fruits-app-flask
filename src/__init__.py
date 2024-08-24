from flask import Flask
from flask_pymongo import PyMongo
# import sys
import os

### Libs for ddtrace and logging
#from ddtrace import tracer
import logging

app = Flask(__name__)
app.secret_key = 'secret'

app.config['MONGO_URI'] = "mongodb://" + os.environ['MONGO_USERNAME'] + ":" + os.environ['MONGO_PASSWORD'] + "@" + os.environ['MONGO_HOST'] + ":" + os.environ['MONGO_PORT'] + "/fruitsdb"
#app.config['MONGO_URI'] = "mongodb://localhost:27017/fruitsdb"

app.config['JSON_AS_ASCII'] = False     # use Japanese Char-set

#mongo = PyMongo(app, config_prefix='MONGO')
mongo = PyMongo(app)

### Datadog APM Log Injection settings
FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
          '- %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)
log.level = logging.INFO


import src.db