from src import app
from src import mongo
from flask import Flask, render_template, request, redirect, jsonify
import socket

### for log injection and custom instrumentation
from src import log
from ddtrace import tracer

@app.route('/hostinfo', methods=['GET'])
def get_host_info():
# Get Socket to investigate Pod address and hostname
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  ip = s.getsockname()[0]
  h = socket.gethostname()
  log.info('You got host info!')
  return jsonify({"ip": ip, "host":h})

@app.route('/', methods=['GET'])
def get_all():
  fruits = mongo.db.fruits.find(projection={'_id':0, 'owner':1, 'id':1, 'name':1, 'production':1, 'quantity':1}, sort=[('id',1)])
  entries = []
  for row in fruits:
    entries.append({"id": row['id'], "owner": row['owner'], "name": row['name'], "production": row['production'], "quantity": row['quantity']})
  log.warn('You got all fruits inventory!')

  return jsonify(entries)

@app.route('/get_error', methods=['GET'])
def get_error():
  fruits = mongo.db.fruits.find(projection={'_id':0, 'owner':1, 'id':1, 'name':1, 'projection':1, 'quantity':1}, sort=[('id',1)])
  entries = []
  for row in fruits:
    entries.append({"id": row['id'], "owner": row['owner'], "name": row['name'], "production": row['production'], "quantity": row['quantity']})

  return jsonify(entries)

@app.route('/get_fruits', methods=['GET'])
@tracer.wrap(service="fruits-app", resource="GET /get_fruits")
def get_fruits():
  owner_id = request.args.get("owner")
  tracer.set_tags({'owner_id': owner_id})

  error = request.args.get("error")
  if error is None:
    fruits = mongo.db.fruits.find( {'owner':owner_id}, projection={'_id':0, 'owner':1, 'id':1, 'name':1, 'production':1, 'quantity':1}, sort=[('id',1)])
    entries = []
    for row in fruits:
      entries.append({"id": row['id'], "name": row['name'], "production": row['production'], "quantity": row['quantity']})
    log.warn('Owner-ID:' + owner_id + ' got the fruits inventory!')
  else:
    raise Exception

  return jsonify(entries)