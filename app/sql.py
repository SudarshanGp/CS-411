import sys

sys.path.insert(2, '/usr/local/lib/python2.7/site-packages')
import pymysql, json
import itertools

db = pymysql.connect(host='162.243.195.102',user='root', passwd ='411Password', db = 'db')

cursor = db.cursor()
# print(cursor)
# f = open('output.sql', 'r')
# query = " ".join(f.readlines())
# cursor.execute(query)
# db.commit()
cursor.execute("SELECT * FROM db.State")
desc = cursor.description
column_names = [col[0] for col in desc]
data = [dict(itertools.izip(column_names, row))
        for row in cursor.fetchall()]
# rows = [ dict(rec) for rec in recs ]
print(data)
# print/(json.dumps(recs))
# print(json.dumps(recs)[0])
# for r in cursor:
#     print('here')
#     print(r)
#     print(type(r))