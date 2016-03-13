__author__ = 'Nathan'
#!/usr/bin/env python
import timeit #test how long it takes
import xlrd #for reading .xlsx files
import csv #for readin .csv files
import sys  #getting sys arguments
import os #for getting cwd

db_name = 'Demo.db'
CurrentDir= os.getcwd()+"/data/"
# /Users/Aadhya/GitHub

def buildOutputSQL(file_name, db_name):
   f = open(file_name, "wb")
   f.write("CREATE DATABASE "+db_name+";\n")
   f.write("DROP TABLE IF EXISTS "+db_name+".AcademicCollege;\n")
   f.write("CREATE TABLE "+db_name+'''.AcademicCollege (
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
    );\n''')
   f.write("DROP TABLE IF EXISTS "+db_name+".Ethnicity;\n")
   f.write("CREATE TABLE "+db_name+'''.Ethnicity (
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
    );\n''')
   f.write("DROP TABLE IF EXISTS "+db_name+".Gender;\n")
   f.write("CREATE TABLE "+db_name+'''.Gender (
    Year VARCHAR(8) not null,
    Male int not null,
    Female int not null,
    Total int not null,
    primary key (Year)
    );\n''')
   f.write("DROP TABLE IF EXISTS "+db_name+".State;\n")
   f.write("CREATE TABLE "+db_name+'''.State (
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
    Hawaii int not null,
    Idaho int not null,
    IL int not null,
    Indiana int not null,
    Iowa int not null,
    Kansas int not null,
    Kentucky int not null,
    Louisiana int not null,
    Maine int not null,
    Maryland int not null,
    Massachusetts int not null,
    Michigan int not null,
    Minnesota int not null,
    Mississippi int not null,
    Missouri int not null,
    Montana int not null,
    Nebraska int not null,
    Nevada int not null,
    NH int not null,
    NJ int not null,
    NM int not null,
    NY int not null,
    NC int not null,
    ND int not null,
    Ohio int not null,
    OK int not null,
    Oregon int not null,
    PA int not null,
    PR int not null,
    RI int not null,
    SC int not null,
    SD int not null,
    Tennessee int not null,
    Texas int not null,
    Utah int not null,
    Vermont int not null,
    Virginia int not null,
    WA int not null,
    WV int not null,
    WI int not null,
    WY int not null,
    Military int not null,
    Other Countries int not null,
    Unknown int not null,
    Total int not null,
    primary key (Year)
    );\n''')
   f.close

def AcademicCollege(fileloc):
    AcademicCollege=[]
    ReturnList=[]
    wb=xlrd.open_workbook(fileloc)
    current_sheet=wb.sheet_by_index(0)
    for i in range(5, 16): #starts at row 5 
        AcademicCollege=AcademicCollege+[int(current_sheet.cell(i,1).value)]
    AcademicCollege.insert(0,str(sys.argv[1][0:4]))
    ReturnList.append(AcademicCollege)
    return ReturnList
    
def Gender(fileloc):
    Gender=[]
    ReturnList=[]
    wb=xlrd.open_workbook(fileloc)
    current_sheet=wb.sheet_by_index(0)
    for i in range(30, 34): #starts at row 5
        if i!=32: #we don't want the blank
            Gender=Gender+[int(current_sheet.cell(i,5).value)]
    Gender.insert(0,str(sys.argv[1][0:4]))
    ReturnList.append(Gender)
    return ReturnList

def Ethnicity(fileloc):
    Ethnicity=[]
    ReturnList=[]
    wb=xlrd.open_workbook(fileloc)
    current_sheet=wb.sheet_by_index(0)
    for i in range(23, 34): #starts at row 5
        if i!=32: #we don't want the blank
            Ethnicity=Ethnicity+[int(current_sheet.cell(i,1).value)]
    Ethnicity.insert(0,str(sys.argv[1][0:4]))
    ReturnList.append(Ethnicity)
    return ReturnList

def State(fileloc):
    State=[]
    ReturnList=[]
    wb=xlrd.open_workbook(fileloc)
    current_sheet=wb.sheet_by_index(0)
    for i in range(5, 45):
        val = current_sheet.cell(i,9).value
        if val != '':
            State=State+[int(val)]
        else:
            State=State+[0]

    for i in range(5, 30):
        if i<20 or i==29:
            val = current_sheet.cell(i,13).value
            if val != '':
                State=State+[int(val)]
            else:
                State=State+[0]

    State.insert(0,str(sys.argv[1][0:4]))
    ReturnList.append(State)
    return ReturnList

def length(i):
    """returns the length of i"""
    return len(str(i))

def writeInsert(file_name, db_name, list, insType):
    f = open(file_name, "a")
    f.write("INSERT INTO ")
    f.write(db_name)
    f.write(".")
    f.write(insType)
    f.write(" VALUES(")
    f.write("'")
    f.write(str(list[0][0]))
    f.write("',")
    list = list[0][1:]
    f.write(",".join(str(i) for i in list))
    f.write(");\n")
    f.close()

def main():
    file_name = "output.sql"
    dbName = "db"
    buildOutputSQL(file_name, dbName)

    fileloc=CurrentDir+str(sys.argv[1])

    AcademicList=AcademicCollege(fileloc) 
    GenderList=Gender(fileloc)
    EthnicityList=Ethnicity(fileloc)
    StateList=State(fileloc)

    writeInsert(file_name, dbName, AcademicList, "AcademicCollege")
    writeInsert(file_name, dbName, GenderList, "Gender")
    writeInsert(file_name, dbName, EthnicityList, "Ethnicity")
    writeInsert(file_name, dbName, StateList, "State")

   
   
if __name__ == '__main__':
    #main()
    #runs the main, and prints the time taken to run
    print timeit.timeit(main,number=1)
