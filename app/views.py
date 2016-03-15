#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

sys.path.insert(2, '/usr/local/lib/python2.7/site-packages')
from flask import Flask, render_template, request, jsonify
import pymysql, json
import itertools

app = Flask(__name__)

db  = ""
cursor = ""




@app.route('/')
@app.route('/index')
def index():
    """
    The index function is called when the a user makes a request to the ip address at which
    the website is hosted. It returns the base.html template and is rendered by jinja2
    :return: Return the base.html template when the root / or /index is requested
    """


    return render_template('base.html')


# @app.route('/info', methods=['GET', 'POST'])
# def revision_response():
#     """
#     revision_response handles GET and POST requests made by its caller function and returns
#     revision information about a specific file that is passed in when the AJAX request is
#     made by the caller
#     :return: Returns a json object to the caller function that made the AJAX request
#     """
#     if 'DIR' in request.json['type']:
#         return jsonify(msg='NO')
#     title = str(request.json['url'])
#     name = '/' + '/'.join(title.split('/')[5:])
#     if 'FILE' in request.json['type']:
#         file_revisions = svn_log[name]
#         json_data = []
#         for (i, val) in enumerate(file_revisions):
#             json_data.append(val.__dict__)
#         return jsonify(
#             msg='YES',
#             url=request.json['url'],
#             name=request.json['name'],
#             revision=request.json['revision'].strip(),
#             revisions=json_data,
#             title=title[6],
#         )


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
    print(states)
    render_data = {}
    print(type(data))
    print(data['objects']['units']['geometries'])
    print(len(data['objects']['units']['geometries']))
    print(len(states[0]))
    for state, pop in enumerate(states[0]):
        temp = {}
        temp['state'] = pop
        temp['students'] = state
        print(state)
        # print(data['objects']['units']['geometries'])
        # print(type(data['objects']['units']['geometries']))
        for key, value in enumerate(data['objects']['units']['geometries']):
            # print(value)
            if value['properties']['name'] is state:
                print("HERE", state, value['properties']['name'])
        #         temp['FIPS'] = value['id']
        #
        print(temp)
    # for key, value in data.iteritems():
    #     print(key)
    #     print(value)

    # app.run(host='0.0.0.0')