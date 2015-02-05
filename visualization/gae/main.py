#!/usr/bin/env python

# Import the Flask Framework
from flask import Flask, jsonify, abort, request, make_response, url_for
import requests
import ConfigParser
import json

app = Flask(__name__, static_url_path = "")

# Configuration
configF = ConfigParser.RawConfigParser()
configF.read('settings.cfg')
config = {
    'apiURL' : configF.get('Mongolab', 'apiURL'),
    'apiKey' : configF.get('Mongolab', 'apiKey'),
    'database' : configF.get('Mongolab', 'database')
}

@app.route('/api/projects', methods=['GET'])
def getProjects():
    tags = request.args.get('tags')
    query = ""
    if tags:
        query = "&q={'_category': '"+ tags +"'}"
    url = config['apiURL'] + config['database'] \
        +"/collections/projects?apiKey=" + config['apiKey'] + query +'&s={"_category": 1, "_rank": -1}'
    headers = {'content-type': 'application/json'}
    r = requests.get(url)
    return jsonify(projects = r.json())

@app.route('/api/projects/<string:project_id>', methods=['GET'])
def getProject(project_id):
    url = config['apiURL'] + config['database'] \
        +"/collections/projects/" + project_id \
        + "?apiKey=" + config['apiKey']
    headers = {'content-type': 'application/json'}
    r = requests.get(url)
    return jsonify(project = r.json())

@app.route('/api/categories', methods=['GET'])
def getCategories():
    url = config['apiURL'] + config['database'] \
        +"/collections/categories?apiKey=" + config['apiKey']
    headers = {'content-type': 'application/json'}
    r = requests.get(url)
    return jsonify(categories = r.json())

@app.route('/api/categories/<string:category_id>', methods=['GET'])
def getCategory(category_id):
    url = config['apiURL'] + config['database'] \
        +"/collections/categories/" + category_id \
        + "?apiKey=" + config['apiKey']
    headers = {'content-type': 'application/json'}
    r = requests.get(url)
    return jsonify(categories = r.json())

@app.route('/api/search', methods=['GET'])
def getKeywords():
    # Get list of categories 
    url = config['apiURL'] + config['database'] \
        +"/collections/categories?apiKey=" + config['apiKey']
    headers = {'content-type': 'application/json'}
    r = requests.get(url)
    cats1 = r.json()
    
    # extract category names 
    cats = []
    for catDict in cats1:
        cats.append(catDict['name'])
    term = request.args.get('term')
    matching = [s for s in cats if term in s]
    return json.dumps(matching)