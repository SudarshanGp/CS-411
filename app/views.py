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
render_data1 = []

@app.route('/')
@app.route('/index')
def index():
    """
    The index function is called when the a user makes a request to the ip address at which
    the website is hosted. It returns the base.html template and is rendered by jinja2
    :return: Return the base.html template when the root / or /index is requested
    """
    # print(render_data)
    create_2014()
    return render_template('base.html', data =render_data)

@app.route('/delete', methods=['GET', 'POST'])
def year_delete_response():
    if '2014' in (request.form.keys())[0]:
        delete_2014()
        return render_template('base.html')
    else:
        delete_2015()
        return render_template('base.html')

@app.route('/addcomment', methods=['GET', 'POST'])
def year_response():
    print("HERE")
    if '2014' in (request.form.keys())[0]:
        create_2014()
        return render_template('base.html', data =render_data)
    else:
        create_2015()
        return render_template('base.html', data =render_data1)

@app.errorhandler(Exception)
def exception_handler(error):
    """
    Handles exceptions that are raised by the program during run time
    :param error: Error code that is raised
    :return: Error information
    """
    return 'ERROR ' + repr(error)

def delete_2014():
    cursor.execute("DELETE FROM db.State WHERE State.Year = 'fa14'")

def delete_2015():
    cursor.execute("DELETE FROM db.State WHERE State.Year = 'fa15'")

def create_2014():
    # f = open('fa14_create.sql', 'r')
    # query = " ".join(f.readlines())
    # cursor.execute(query)
    # db.commit()
    cursor.execute("SELECT * FROM db.State WHERE Year = 'fa14'")
    desc = cursor.description
    column_names = [col[0] for col in desc]
    states = [dict(itertools.izip(column_names, row))
            for row in cursor.fetchall()]

    for pop, state in states[0].iteritems():
        temp = {}
        temp['state'] = pop
        temp['students'] = state
        for key, value in enumerate(data['objects']['units']['geometries']):
            if value['properties']['name'].replace(" ", "").lower() in pop.replace(" ", "").lower() and len(value['properties']['name'].replace(" ", "").lower()) == len(pop.replace(" ", "").lower()):
                temp['FIPS'] = value['id']
                render_data.append(temp)

def create_2015():
    # f = open('fa15_create.sql', 'r')
    # query = " ".join(f.readlines())
    # cursor.execute(query)
    # db.commit()
    cursor.execute("SELECT * FROM db.State WHERE Year = 'fa15'")
    desc = cursor.description
    column_names = [col[0] for col in desc]
    states = [dict(itertools.izip(column_names, row))
            for row in cursor.fetchall()]
    print(states)
    for pop, state in states[0].iteritems():
        temp = {}
        temp['state'] = pop
        temp['students'] = state
        for key, value in enumerate(data['objects']['units']['geometries']):
            if value['properties']['name'].replace(" ", "").lower() in pop.replace(" ", "").lower() and len(value['properties']['name'].replace(" ", "").lower()) == len(pop.replace(" ", "").lower()):
                temp['FIPS'] = value['id']
                render_data1.append(temp)

if __name__ == '__main__':
    db = pymysql.connect(host='162.243.195.102',user='root', passwd ='411Password', db = 'db')
    cursor = db.cursor()
    with open('static/d3-geomap/topojson/countries/USA.json') as data_file:
        data = json.load(data_file)

    # cursor.execute("SELECT * FROM db.State WHERE Year = 'fa14'")
    # desc = cursor.description
    # column_names = [col[0] for col in desc]
    # states = [dict(itertools.izip(column_names, row))
    #         for row in cursor.fetchall()]
    #
    # for pop, state in states[0].iteritems():
    #     temp = {}
    #     temp['state'] = pop
    #     temp['students'] = state
    #     for key, value in enumerate(data['objects']['units']['geometries']):
    #         if value['properties']['name'].replace(" ", "").lower() in pop.replace(" ", "").lower() and len(value['properties']['name'].replace(" ", "").lower()) == len(pop.replace(" ", "").lower()):
    #             temp['FIPS'] = value['id']
    #             render_data.append(temp)

    # cursor.execute("SELECT * FROM db.State WHERE Year = 'fa15'")
    # desc = cursor.description
    # column_names = [col[0] for col in desc]
    # states = [dict(itertools.izip(column_names, row))
    #         for row in cursor.fetchall()]
    # print(states)
    # for pop, state in states[0].iteritems():
    #     temp = {}
    #     temp['state'] = pop
    #     temp['students'] = state
    #     for key, value in enumerate(data['objects']['units']['geometries']):
    #         if value['properties']['name'].replace(" ", "").lower() in pop.replace(" ", "").lower() and len(value['properties']['name'].replace(" ", "").lower()) == len(pop.replace(" ", "").lower()):
    #             temp['FIPS'] = value['id']
    #             render_data1.append(temp)

    app.run()
