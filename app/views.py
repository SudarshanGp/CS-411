#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

sys.path.insert(2, '/usr/local/lib/python2.7/site-packages')
from flask import Flask, render_template, request, jsonify
import pymysql, json
import itertools
import pprint
app = Flask(__name__)

db  = ""
cursor = ""
render_data = []


@app.route('/')
@app.route('/index')
def index():
    """
    The index function is called when the a user makes a request to the ip address at which
    the website is hosted. It returns the base.html template and is rendered by jinja2
    :return: Return the base.html template when the root / or /index is requested
    """
    # print(render_data)

    return render_template('base.html', data =render_data)


@app.route('/addcomment', methods=['GET', 'POST'])
def year_response():
    print("HERE")
    if '2014' in (request.form.keys())[0]:
        return render_template('base.html', data =render_data)
    else:


@app.errorhandler(Exception)
def exception_handler(error):
    """
    Handles exceptions that are raised by the program during run time
    :param error: Error code that is raised
    :return: Error information
    """
    return 'ERROR ' + repr(error)


if __name__ == '__main__':
    db = pymysql.connect(host='162.243.195.102',user='root', passwd ='411Password', db = 'db')
    cursor = db.cursor()
    with open('static/d3-geomap/topojson/countries/USA.json') as data_file:
        data = json.load(data_file)

    cursor.execute("SELECT * FROM db.State")
    desc = cursor.description
    column_names = [col[0] for col in desc]
    states = [dict(itertools.izip(column_names, row))
            for row in cursor.fetchall()]
    # print(states[0])
    # print(type(data))
    # print(data['objects']['units']['geometries'])
    # print(len(data['objects']['units']['geometries']))
    # print(len(states[0]))
    for pop, state in states[0].iteritems():
        temp = {}
        # print(pop)
        # print(state)
        temp['state'] = pop
        temp['students'] = state
        # print("STAETE " , state)
        for key, value in enumerate(data['objects']['units']['geometries']):
            if value['properties']['name'].replace(" ", "").lower() in pop.replace(" ", "").lower() and len(value['properties']['name'].replace(" ", "").lower()) == len(pop.replace(" ", "").lower()):
                # print("IN IF")
                # print(value['properties']['name'].replace(" ", "").lower() ,state.replace(" ", "").lower() )

                temp['FIPS'] = value['id']
                render_data.append(temp)

    # pprint.pprint(render_data)
    # print(len(render_data))
    app.run(host='0.0.0.0')
