#!/usr/bin/python
#coding:utf-8

#from ansible import callbacks
#import ansible.runner
from flask import Flask, request, jsonify, render_template,abort

import commands, json
app = Flask(__name__)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001, debug=True)
