#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

sys.path.insert(2, '/usr/local/lib/python2.7/site-packages')
from flask import Flask, render_template, request, jsonify,send_from_directory, redirect
import pymysql, json
import itertools
import pprint
import os
app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
db  = ""
cursor = ""
render_data = []
render_data1 = []

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    """
    The index function is called when the a user makes a request to the ip address at which
    the website is hosted. It returns the base.html template and is rendered by jinja2
    :return: Return the base.html template when the root / or /index is requested
    """
    # print(render_data)
    create_2014()

    return render_template('base.html', data =render_data)

@app.route('/dashboard', methods = ['GET','POST'])
def dashboard():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('dashboard.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/addpassword', methods=['GET', 'POST'])
def addpassword():
    inUse = request.form['username']
    inPass = request.form['password']
    check = "SELECT * FROM db.LoginInfo WHERE Username = %s"
    cursor.execute(check,(inUse))
    db.commit()
    if(cursor.rowcount == 0):
        insertLog = "INSERT INTO db.LoginInfo VALUES(%s,%s)"
        cursor.execute(insertLog, (inUse, inPass))
        db.commit()
    else:
        print "oops, username taken"
        desc = cursor.description
        r = cursor.fetchall()
        print r[0][1]
        if inPass in r[0][1]:
            return render_template('base_no_login.html',data =render_data)
        else:
            return render_template('base.html',data =render_data)
    return render_template('base_no_login.html',data =render_data)

@app.route('/forgotpasswordreset', methods=['GET', 'POST'])
def forgotpassword():
    inUse = request.form['username']
    inPass = request.form['password']
    print inUse, inPass
    check = "SELECT * FROM db.LoginInfo WHERE Username = %s"
    cursor.execute(check,(inUse))
    print "finished select"
    if(cursor.rowcount == 0):
        insertLog = "INSERT INTO db.LoginInfo VALUES(%s,%s)"
        cursor.execute(insertLog, (inUse, inPass))
        db.commit()
    else:
        print "in update"
        insertLog = "UPDATE db.LoginInfo SET Password = %s WHERE Username = %s"
        cursor.execute(insertLog, (inPass, inUse))
        db.commit()
    return render_template('base_no_login.html',data =render_data)

@app.route('/forgotpassword')
def forgotpage():
    return render_template('forgotpassword.html',data =render_data)

@app.route('/delete', methods=['GET', 'POST'])
def year_delete_response():
    print "delete"
    if '2014Del' in (request.form.keys())[0]:
        print "deleting"
        delete_2014()
        render_data = {}
        return render_template('base.html', data = render_data)
    elif '2015Del' in (request.form.keys())[0]:
        delete_2015()
        render_data1 = {}
        return render_template('base.html', data = render_data1)

@app.route('/addcomment', methods=['GET', 'POST'])
def year_response():
    print("HERE")
    if '2014' in (request.form.keys())[0]:
        create_2014()
        return render_template('base.html', data =render_data)
    else:
        create_2015()
        return render_template('base.html', data =render_data1)

# @app.errorhandler(Exception)
# def exception_handler(error):
#     """
#     Handles exceptions that are raised by the program during run time
#     :param error: Error code that is raised
#     :return: Error information
#     """
#     return 'ERROR ' + repr(error)

def delete_2014():
    print "deleting year row"
    f = open('rmfa14.sql', 'r')
    query = " ".join(f.readlines())
    f.close()
    cursor.execute(query)
    db.commit()

def delete_2015():
    f = open('rmfa15.sql', 'r')
    query = " ".join(f.readlines())
    f.close()
    cursor.execute(query)
    db.commit()

def create_2014():
    f = open('fa14.sql', 'r')
    query = " ".join(f.readlines())
    f.close()
    cursor.execute(query)
    db.commit()
    cursor.execute("SELECT *  FROM db.State WHERE Year = 'fa14'")
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
                if temp['FIPS'] == 'US17':
                    temp['students'] = 0
                render_data.append(temp)

def create_2015():
    f = open('fa15.sql', 'r')
    query = " ".join(f.readlines())
    f.close()
    cursor.execute(query)
    db.commit()
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
                if temp['FIPS'] == 'US17':
                    temp['students'] = 0
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

    app.run(debug=True)
