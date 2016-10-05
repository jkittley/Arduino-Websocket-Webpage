import json
import random
import asyncio
import concurrent
import time
import os
import click
from unipath import Path
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_socketio import SocketIO, send, emit
from config import *

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)
print (socketio)

# ------------------------------------------------------------------------------
# Web pages
# ------------------------------------------------------------------------------

# Index Page
@app.route('/')
def index():
    menu = [
        {"name": "Pomg", "url": "/pong", "img": "pong.png" },
    ]
    return render_template('index.html', menu=menu)


# Pong Game
@app.route('/pong')
def play_pong():
    return render_template('pong.html')


# ------------------------------------------------------------------------------
# Message handlers
# ------------------------------------------------------------------------------

# Listen to all messages with unknown event
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

# Listen to browser response
@socketio.on('from_browser')
def handle_message(json):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = { 'timestamp': timestamp, 'data': json }
    socketio.emit('feedback', data)
    print('from_browser: ' + str(json))


# Listen to data receiver from serial monitor
@socketio.on('from_serial_monitor')
def handle_json(json):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = { 'timestamp': timestamp, 'data': json }
    socketio.emit('update', data)
    print('from_serial_monitor: ' + str(json))




# ------------------------------------------------------------------------------
# Start App
# ------------------------------------------------------------------------------

@click.command()
@click.option('--prod', is_flag=True, default=False, help='Switch to production mode')
def main(prod):
    if not prod:
        servermode = 'local'
    else:
        servermode = 'prod'
    app.debug = True
    app.use_reloader = False
    server_settings = WEB_SERVER[servermode]
    socketio.run(app, port=server_settings['port'], host=server_settings['host'])

if __name__ == '__main__':
   main()
