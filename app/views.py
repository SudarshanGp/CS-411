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

    return render_template('base.html', data =render_data)

@app.route('/dashboard', methods = ['GET','POST'])
def dashboard():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('dashboard.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('dashboard.html')
        else:
            return render_template('upload.html', message = "File not able to upload")
    return render_template('upload.html', message = "No file uploaded")

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


if __name__ == '__main__':
    db = pymysql.connect(host='162.243.195.102',user='root', passwd ='411Password', db = 'db3')
    cursor = db.cursor()

    app.run(debug=True)
