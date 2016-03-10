__author__ = 'SUSAN SUCKS'
import sqlite3
import os
import datetime

from HVAC_DB_Schema_Constants import *


def writeDataSetInfo(conn, data_set_info):
    c = conn.cursor()
    DataSetInfo=[]
    execString= "SELECT * FROM DataSetInfo"
    c.execute(execString)
    DatsSetInfoRows=c.fetchall()
    for i in DatsSetInfoRows:
        DataSetInfo.append(i[0])
    conn.execute('pragma foreign_keys=ON')
    for j in data_set_info:
        if j[0] not in DataSetInfo:
            cmd_text = """insert into DataSetInfo values (?,?,?,?,?,?)"""
            c.executemany(cmd_text, data_set_info)
    conn.commit()
    c.close()

def writeECUInstanceInfo(conn, data_list):
    c= conn.cursor()
    #conn.execute('pragma foreign_keys=ON')
    cmd_text = """insert into ECUInstanceInfo values (?,?,?,?)"""
    c.executemany(cmd_text, data_list)
    conn.commit()
    c.close()


def writeECUData(conn, data_list):
    c= conn.cursor()
    conn.execute('pragma foreign_keys=ON')
    cmd_text = """insert into ECUData values (?,?,?,?,?,?,?,?,?)"""
    c.executemany(cmd_text, data_list)
    conn.commit()
    c.close()

  
def writeShelterWeatherData(conn, data_list):
    c= conn.cursor()
    conn.execute('pragma foreign_keys=ON')
    cmd_text = """insert into AcademicCollege values (?,?,?,?,?,?,?,?,?,?,?,?)"""
    c.executemany(cmd_text, data_list)
    conn.commit()
    c.close()
def writeAcademicCollege(conn, data_list):
    c= conn.cursor()
    conn.execute('pragma foreign_keys=ON')
    cmd_text = """insert into AcademicCollege values (?,?,?,?,?,?,?,?,?,?,?,?)"""
    c.executemany(cmd_text, data_list)
    conn.commit()
    c.close()

def buildOutputDatabase(db_name):
    """Initialize DB - Note this clobbers all previous DBs!"""
    try:
        os.remove(db_name)
    except:
        pass
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute(''' CREATE TABLE AcademicCollege (
    Year VARCHAR(8) not null,
    AgConsEnvSci int not null,
    ApHealthSci int not null,
    Business int not null,
    Edu int not null,
    Eng int not null, 
    Art int not null,
    GenStud int not null,
    Las int not null,
    Media int not null,
    SocWork int not null,
    Total int not null,
    primary key (Year)
    )''')

    c.execute(''' CREATE TABLE Ethnicity (
    Year VARCHAR(8) not null,
    AfAm int not null,
    Asian int not null,
    Hisp int not null,
    Multi int not null,
    NativeAmAl int not null,
    White int not null,
    Foreigner int not null,
    Unknown int not null,
    Total int not null,
    primary key (Year)
    )''')
    
    c.execute(''' CREATE TABLE Gender (
    Year VARCHAR(8) not null,
    Male int not null,
    Female int not null,
    Total int not null,
    primary key (Year)
    )''')
    
    c.execute(''' CREATE TABLE State (
    Year VARCHAR(8) not null,
    Alabama int not null,
    Alaska int not null,
    Arizona int not null,
    Arkansas int not null,
    CA int not null,
    Colorado int not null,
    Connecticut int not null,
    Delaware int not null,
    DC int not null,
    FL int not null,
    GA int not null,
    Idaho int not null,
    IL int not null,
    Indiana int not null,
    Iowa int not null,
    Kansas int not null,
    Kentucky int not null,
    Louisiana int not null,
    Maryland int not null,
    Massachusetts int not null,
    Michigan int not null,
    Minnesota int not null,
    Mississippi int not null,
    Missouri int not null,
    Nebraska int not null,
    Nevada int not null,
    NH int not null,
    NJ int not null,
    NM int not null,
    NY int not null,
    NC int not null,
    Ohio int not null,
    Oregon int not null,
    PA int not null,
    PR int not null,
    RI int not null,
    SC int not null,
    SD int not null,
    Tennessee int not null,
    Texas int not null,
    Utah int not null,
    Virginia int not null,
    WA int not null,
    WI int not null,
    Military int not null,
    Other Countries int not null,
    Unknown int not null,
    Total int not null,
    primary key (Year)
    )''')

    conn.commit()
    conn.close()
