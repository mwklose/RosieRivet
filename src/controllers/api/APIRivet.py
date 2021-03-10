import flask
from flask import request
import json
import os
app = flask.Flask(__name__)
app.config["DEBUG"] = True
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

@app.route('/v1/analyze', methods=['POST'])
def analyze():
    file = request.files['file']
    file.save(os.path.join(ROOT_PATH,file.filename))


    return 'Hello World'
app.run()