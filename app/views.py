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
    get_departments_names = "SELECT DISTINCT Department from db.id;"
    cursor.execute(get_departments_names)
    get_department_names_json = dictfetchall(cursor)
    get_gender_all_years = "SELECT db.id.Year, db.id.Department, db.id.Major, Male, Female, Other FROM db.Gender INNER JOIN db.id ON db.id.ID = db.Gender.ID ;"
    cursor.execute(get_gender_all_years)
    get_gender_all_years_json = dictfetchall(cursor)
    get_gender_sum = "SELECT db.id.Year, db.id.Department, db.id.Major, (Male+ Female+Other) AS major_sum FROM db.Gender INNER JOIN db.id ON db.id.ID = db.Gender.ID ;"
    cursor.execute(get_gender_sum)
    get_gender_sum_json = dictfetchall(cursor)
    all_department_gender_sum_year = "SELECT a.Department, a.Year, SUM(a.major_sum) as total\
            FROM (SELECT db.id.Year, db.id.Department, db.id.Major, (Male+ Female+Other) AS major_sum FROM db.Gender INNER JOIN db.id ON db.id.ID = db.Gender.ID ) a \
            GROUP BY a.Department, a.Year;"
    cursor.execute(all_department_gender_sum_year)
    all_department_gender_sum_year_json = dictfetchall(cursor)
    get_ethinicity_all_years = "SELECT db.id.Year, db.id.Department, db.id.Major, db.Ethnicity.* FROM db.Ethnicity INNER JOIN db.id ON db.id.ID = db.Ethnicity.ID ;"
    cursor.execute(get_ethinicity_all_years)
    get_ethinicity_all_years_json = dictfetchall(cursor)
    ethinicity_dict = {}
    for key, value in enumerate(get_ethinicity_all_years_json):
        if value['Year'] in ethinicity_dict.keys():
            # if value['Department'] in ethinicity_dict[value['Year']]:
            temp_list = []
            temp_list.append({'label' : 'African American', 'value' : value['AfAm']})
            temp_list.append({'label' : 'Asian', 'value' : value['Asian']})
            temp_list.append({'label': 'Foreigner', 'value': value['Foreigner']})
            temp_list.append({'label': 'Hispanic', 'value': value['Hisp']})
            temp_list.append({'label': 'Multi Racial', 'value': value['Multi']})
            temp_list.append({'label': 'Native American', 'value': value['NativeAmAl']})
            temp_list.append({'label': 'Native Hawaiian', 'value': value['NativeHaw']})
            temp_list.append({'label': 'White', 'value': value['White']})
            temp_list.append({'label': 'Other', 'value': value['Other']})
            if value['Department'] in ethinicity_dict[value['Year']].keys():
                ethinicity_dict[value['Year']][value['Department']][value['Major']] = temp_list
            else:
                ethinicity_dict[value['Year']][value['Department']] = {}
                ethinicity_dict[value['Year']][value['Department']][value['Major']] = temp_list
        else:
            ethinicity_dict[value['Year']] = {}
            ethinicity_dict[value['Year']][value['Department']] = {}
            temp_list = []
            temp_list.append({'label': 'African American', 'value': value['AfAm']})
            temp_list.append({'label': 'Asian', 'value': value['Asian']})
            temp_list.append({'label': 'Foreigner', 'value': value['Foreigner']})
            temp_list.append({'label': 'Hispanic', 'value': value['Hisp']})
            temp_list.append({'label': 'Multi Racial', 'value': value['Multi']})
            temp_list.append({'label': 'Native American', 'value': value['NativeAmAl']})
            temp_list.append({'label': 'Native Hawaiian', 'value': value['NativeHaw']})
            temp_list.append({'label': 'White', 'value': value['White']})
            temp_list.append({'label': 'Other', 'value': value['Other']})
            ethinicity_dict[value['Year']][value['Department']][value['Major']] = temp_list


    # pprint.pprint(get_ethinicity_all_years_json)
    # pprint.pprint(get_department_names_json)
    # pprint.pprint(get_gender_all_years_json)
    # pprint.pprint(get_gender_sum_json)
    major_dict = {} # Enrollment by Major
    for key, value in enumerate(get_gender_sum_json):
        if value['Year'] in major_dict.keys():
            if value['Department'] in major_dict[value['Year']]:
                curr_list = major_dict[value['Year']][value['Department']]
                temp_dict = {}
                temp_dict['label'] = value['Major']
                temp_dict['value'] = value['major_sum']
                curr_list.append(temp_dict)
                major_dict[value['Year']][value['Department']] = curr_list
            else:
                temp_list = []
                temp_dict = {}
                temp_dict['label'] = value['Major']
                temp_dict['value'] = value['major_sum']
                temp_list.append(temp_dict)
                major_dict[value['Year']][value['Department']] = temp_list
        else:
            temp_list = []
            temp_dict = {}
            temp_dict['label'] = value['Major']
            temp_dict['value'] = value['major_sum']
            temp_list.append(temp_dict)
            major_dict[value['Year']] = {value['Department'] :temp_list }
            # major_dict[value['Year']] = temp_list


    # pprint.pprint(all_department_gender_sum_year_json)
    department_dict = {} # Enrollment by department
    for key, value in enumerate(all_department_gender_sum_year_json):
        if value['Year'] in department_dict.keys():
            curr_list = department_dict[value['Year']]
            temp = {}
            temp['label'] = value['Department']
            temp['value'] = int(value['total'])
            curr_list.append(temp)
            department_dict[value['Year']] = curr_list
        else:
            temp_list = []
            temp = {}
            temp['label'] = value['Department']
            temp['value'] = int(value['total'])
            temp_list.append(temp)
            department_dict[value['Year']] = temp_list


    return render_template('dashboard.html', pie_department_data = department_dict, pie_major_data = major_dict, ethinicity_data = ethinicity_dict)

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


if __name__ == '__main__':
    db = pymysql.connect(host='162.243.195.102',user='root', passwd ='411Password', db = 'db')
    cursor = db.cursor()

    app.run(debug=True)
