#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

import logging
from logging.handlers import RotatingFileHandler
import argparse

from gen_mcq import display
import pandas as pd

app = Flask(__name__)

# Script arguments can include path of the config
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--host', type=str, default="0.0.0.0")
arg_parser.add_argument('--port', type=str, default="5100")
arg_parser.add_argument('--log', type=str, default="gcm-qa.log")
args = arg_parser.parse_args()

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/query', methods=['GET', 'POST'])
def mcq_results():
    # Use these signatures to pass in function
    app.logger.info('paragraph: %s', request.form['paragraph'])
    app.logger.info('num: %s', request.form['num'])
    display(request.form['paragraph'], request.form['num'])
    data = pd.read_json('response.json')
    data = data.to_json(orient='records')
    app.logger.info('data: %s', data)
    print("Finally returning Response...")
    return data  # pass JSON as string, will be parsed in JQuery

if __name__ == "__main__":
    handler = RotatingFileHandler(args.log, maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host=args.host, port=args.port)
