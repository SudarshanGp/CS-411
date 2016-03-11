__author__ = 'SUSAN SUCKS'
import sqlite3
import os
import datetime

def writeAcademicCollege(conn, data_list):
    c= conn.cursor()
    conn.execute('pragma foreign_keys=ON')
    cmd_text = """insert into AcademicCollege values (?,?,?,?,?,?,?,?,?,?,?,?)"""
    c.executemany(cmd_text, data_list)
    conn.commit()
    c.close()

def writeEthnicity(conn, data_list):
    c= conn.cursor()
    conn.execute('pragma foreign_keys=ON')
    cmd_text = """insert into Ethnicity values (?,?,?,?,?,?,?,?,?,?,?)"""
    c.executemany(cmd_text, data_list)
    conn.commit()
    c.close()

def writeGender(conn, data_list):
    c= conn.cursor()
    conn.execute('pragma foreign_keys=ON')
    cmd_text = """insert into Gender values (?,?,?,?)"""
    c.executemany(cmd_text, data_list)
    conn.commit()
    c.close()

def writeState(conn, data_list):
    c= conn.cursor()
    conn.execute('pragma foreign_keys=ON')
    cmd_text = """insert into State values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
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
    NativeHaw int not null,
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
    Alabama int null,
    Alaska int null,
    Arizona int null,
    Arkansas int null,
    CA int null,
    Colorado int null,
    Connecticut int null,
    Delaware int null,
    DC int null,
    FL int null,
    GA int null,
    Hawaii int null,
    Idaho int null,
    IL int null,
    Indiana int null,
    Iowa int null,
    Kansas int null,
    Kentucky int null,
    Louisiana int null,
    Maine int null,
    Maryland int null,
    Massachusetts int null,
    Michigan int null,
    Minnesota int null,
    Mississippi int null,
    Missouri int null,
    Montana int null,
    Nebraska int null,
    Nevada int null,
    NH int null,
    NJ int null,
    NM int null,
    NY int null,
    NC int null,
    ND int null,
    Ohio int null,
    OK int null,
    Oregon int null,
    PA int null,
    PR int null,
    RI int null,
    SC int null,
    SD int null,
    Tennessee int null,
    Texas int null,
    Utah int null,
    Virginia int null,
    Vermont int null,
    WA int null,
    WV int null,
    WI int null,
    WY int null,
    Military int null,
    Other Countries int null,
    Unknown int null,
    Total int not null,
    primary key (Year)
    )''')

    conn.commit()
    conn.close()
