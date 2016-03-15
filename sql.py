import pymysql
db = pymysql.connect(host='162.243.195.102',user='root', passwd ='411Password', db='mysql')
# conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='mysql')

cursor = db.cursor()
f = open('demo1.sql', 'r')
query = " ".join(f.readlines())
# for line in open('demo.sql'):
    # cursor.execute(line)
cursor.execute(query)
for r in cursor:
	print r