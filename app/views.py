#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from sqlite3 import OperationalError

sys.path.insert(2, '/usr/local/lib/python2.7/site-packages')
from flask import Flask, render_template, request, jsonify,send_from_directory, redirect, url_for
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


def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(itertools.izip([col[0] for col in desc], row))
            for row in cursor.fetchall()]


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
    get_departments_names = "SELECT DISTINCT Department from db5.id;"
    cursor.execute(get_departments_names)
    get_department_names_json = dictfetchall(cursor)
    get_gender_all_years = "SELECT db5.id.Year, db5.id.Department, db5.id.Major, Male, Female, Other FROM db5.Gender INNER JOIN db5.id ON db5.id.ID = db5.Gender.ID ;"
    cursor.execute(get_gender_all_years)
    get_gender_all_years_json = dictfetchall(cursor)
    get_gender_sum = "SELECT db5.id.Year, db5.id.Department, db5.id.Major, (Male+ Female+Other) AS major_sum FROM db5.Gender INNER JOIN db5.id ON db5.id.ID = db5.Gender.ID ;"
    cursor.execute(get_gender_sum)
    get_gender_sum_json = dictfetchall(cursor)
    all_department_gender_sum_year = "SELECT a.Department, a.Year, SUM(a.major_sum) as total\
            FROM (SELECT db5.id.Year, db5.id.Department, db5.id.Major, (Male+ Female+Other) AS major_sum FROM db5.Gender INNER JOIN db5.id ON db5.id.ID = db5.Gender.ID ) a \
            GROUP BY a.Department, a.Year;"
    cursor.execute(all_department_gender_sum_year)
    all_department_gender_sum_year_json = dictfetchall(cursor)

    # pprint.pprint(get_department_names_json)
    # pprint.pprint(get_gender_all_years_json)
    # pprint.pprint(get_gender_sum_json)

    # pprint.pprint(all_department_gender_sum_year_json)
    sp16_data = []
    for key, value in enumerate(all_department_gender_sum_year_json):
        if value['Year'] in 'sp16':
            temp = {}
            temp['label'] = value['Department']
            temp['value'] = int(value['total'])
            sp16_data.append(temp)
    pprint.pprint(sp16_data)

    return render_template('dashboard.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print filename
            file_split = filename.split('.')
            sql_file = file_split[0] + ".sql"
            if "rm" in filename.lower():
                if os.path.isfile(sql_file):
                    executeScriptsFromFile(sql_file)
                else:
                    print "file does not exist"
            else:
                python_command = "python " + "file_parser.py" + " " + filename
                os.system(python_command)
                file_split = filename.split('.')
                sql_file = file_split[0] + ".sql"
                print sql_file
                executeScriptsFromFile(sql_file)
            return redirect(url_for('dashboard'))
        else:
            return render_template('upload.html', message = "File not able to upload")
    return render_template('upload.html', message = "No file uploaded")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

def executeScriptsFromFile(filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    cursor.execute(sqlFile)
    db.commit()
    # # Execute every command from the input file
    # for command in sqlCommands:
    #     # This will skip and report errors
    #     # For example, if the tables do not yet exist, this will skip over
    #     # the DROP TABLE commands
    #     try:
    #         cursor.execute(command)
    #     except OperationalError, msg:
    #         print "Command skipped: ", msg

if __name__ == '__main__':
    db = pymysql.connect(host='162.243.195.102',user='root', passwd ='411Password', db = 'db5')
    cursor = db.cursor()

    app.run(debug=True)
