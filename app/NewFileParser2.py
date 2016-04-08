import sys

sys.path.insert(2, '/usr/local/lib/python2.7/site-packages')
import timeit #test how long it takes
import xlrd #for reading .xlsx files
import csv #for readin .csv files
import sys  #getting sys arguments
import os #for getting cwd

db_name = 'Demo.db'
CurrentDir= os.getcwd()+"/static/res/"
# /Users/Aadhya/GitHub

def buildOutputSQL(file_name, db_name):
   f = open(file_name, "wb")
   f.write("CREATE DATABASE "+db_name+";\n")
   f.write("DROP TABLE IF EXISTS "+db_name+".id;\n")
   f.write("CREATE TABLE "+db_name+'''.id (
    ID int not null,
    Year VARCHAR(8) not null,
    Department VARCHAR(128) not null,
    Major VARCHAR(128) not null,
    Total int not null,
    primary key (ID)
    );\n''')

   f.write("DROP TABLE IF EXISTS "+db_name+".Ethnicity;\n")
   f.write("CREATE TABLE "+db_name+'''.Ethnicity (
    ID int not null,
    White int not null,
    Asian int not null,
    AfAm int not null,
    Hisp int not null,
    NativeAmAl int not null,
    NativeHaw int not null,
    Multi int not null,
    Foreigner int not null,
    Other int not null,
    primary key (ID)
    );\n''')
   f.write("DROP TABLE IF EXISTS "+db_name+".Gender;\n")
   f.write("CREATE TABLE "+db_name+'''.Gender (
    ID int not null,
    Male int not null,
    Female int not null,
    Other int not null,
    primary key (ID)
    );\n''')
   f.write("DROP TABLE IF EXISTS "+db_name+".Residency;\n")
   f.write("CREATE TABLE "+db_name+'''.Residency (
    ID int not null,
    IL int not null,
    NonIL int not null,
    primary key (ID)
    );\n''')
   f.close

def FilePar(fileloc):
   
    Gender=[]
    Ethnicity=[]
    Residency = []
    Department={}
    Departmentlist=[]
    wb=xlrd.open_workbook(fileloc)
    current_sheet=wb.sheet_by_index(0)
  
    dep = 0
    counter=0 # for ID
    counterlist=[]
    
    for i in range(1, current_sheet.nrows):
        
        if(i>11):
            #print 'a'+current_sheet.cell(i,2).value+'a'
            #it was a double space for some reason....
            
            if(current_sheet.cell(i,2).value=='  ' and current_sheet.cell(i,3).value=='  ' and 
                current_sheet.cell(i,4).value=='  ' and current_sheet.cell(i,5).value!='  ' and 
                current_sheet.cell(i,6).value=='  ' and current_sheet.cell(i,7).value=='  '):
                thisdep = '"'+current_sheet.cell(i,5).value
                thisdep=thisdep[0:len(thisdep)-1]
                thisdep+='"'
                Departmentlist.append(thisdep)
                dep += 1
                Department[Departmentlist[dep-1]]=[]
                
                continue
        
            if(current_sheet.cell(i,5).value!=''):
                if (current_sheet.cell(i,5).value not in Department[Departmentlist[dep-1]]):
                    maj='"'+current_sheet.cell(i,5).value
                    maj= maj[0:len(maj)-1]
                    maj+='"'
                    Department[Departmentlist[dep-1]].append(maj)
                    counter += 1
                if counter in counterlist:
                    #find same counter then add the points
                    for j in range(0,len(Gender)):
                        #all are the same length
                        if(Gender[j][0]==counter):
                            Gender[j][1]+=current_sheet.cell(i,9).value
                            Gender[j][2]+=current_sheet.cell(i,10).value
                            Gender[j][3]+=current_sheet.cell(i,11).value
                    
                        if(Ethnicity[j][0]==counter):
                            #could change this too a for loop.
                            Ethnicity[j][1]+=current_sheet.cell(i,12).value
                            Ethnicity[j][2]+=current_sheet.cell(i,13).value
                            Ethnicity[j][3]+=current_sheet.cell(i,14).value
                            Ethnicity[j][4]+=current_sheet.cell(i,15).value
                            Ethnicity[j][5]+=current_sheet.cell(i,16).value
                            Ethnicity[j][6]+=current_sheet.cell(i,17).value
                            Ethnicity[j][7]+=current_sheet.cell(i,18).value
                            Ethnicity[j][8]+=current_sheet.cell(i,19).value
                            Ethnicity[j][9]+=current_sheet.cell(i,20).value
                            
                        if(Residency[j][0]==counter):
                            Residency[j][1]+=current_sheet.cell(i,19).value
                            Residency[j][2]+=current_sheet.cell(i,20).value
                            
                else:
                    #not the same counter so just add to the list
                    counterlist.append(counter)
                
                    Gender.append([counter,current_sheet.cell(i,9).value, current_sheet.cell(i,10).value, current_sheet.cell(i,11).value])
                
                    Ethnicity.append([counter,current_sheet.cell(i,12).value,current_sheet.cell(i,13).value,current_sheet.cell(i,14).value, 
                                    current_sheet.cell(i,15).value, current_sheet.cell(i,16).value, current_sheet.cell(i,17).value, 
                                    current_sheet.cell(i,18).value, current_sheet.cell(i,19).value, current_sheet.cell(i,20).value])
                    Residency.append([counter,current_sheet.cell(i,19).value,current_sheet.cell(i,20).value])
   
    return Department,Gender,Ethnicity,Residency

def writeInsert(file_name, db_name, list, insType, first):
    if first == True:
        f = open(file_name, "w")
    else:
        f=open(file_name,"a")

    for i in range(len(list)):
        f.write("INSERT IGNORE INTO ")
        f.write(db_name)
        f.write(".")
        f.write(insType)
        f.write(" VALUES(")
        f.write("'")
        f.write(str(list[i][0]))
        f.write("',")
        temp = list[i][1:]
        f.write(",".join(str(j) for j in temp))
        f.write(");\n")
    f.close()

def writeDel(file_name, db_name, insType, first):
    yearVal = file_name[2:]
    yearVal = yearVal[:-4]
    if first == True:
        f = open(file_name, "w")
    else:
        f=open(file_name,"a")
    f.write("DELETE FROM ")
    f.write(db_name)
    f.write(".")
    f.write(insType)
    f.write(" WHERE Year = '")
    f.write(yearVal)
    f.write("';\n")
    f.close()

def main():
    dbName = "db"

    fileloc=CurrentDir+str(sys.argv[1])
    file_name = str(sys.argv[1])[:-4]+".sql"
    # rm_file = "rm"+file_name
    # createNew = ""
    # if(len(sys.argv) == 3):
    #     createNew = str(sys.argv[2])
    
    first = True;

    # if(createNew is 'n'):
    #     buildOutputSQL(file_name, dbName)
    #     first = False;

    Department, Gender, Ethnicity, Residency=FilePar(fileloc)
    ids = []
    gen = []
    eth = []
    res = []
    count=0

    for key in Department:
        for val in Department[key]:
            temp=[]
            temp.append(str(count))
            temp.append('"'+str(sys.argv[1])[:-4]+'"')
            temp.append(key)
            temp.append(val)
            ids.append(temp)
            count += 1
    # AcademicList=AcademicCollege(fileloc) 
    # GenderList=Gender(fileloc)
    # EthnicityList=Ethnicity(fileloc)
    # StateList=State(fileloc)
    writeInsert(file_name, dbName, ids, "id", first)
    # writeDel(rm_file, dbName, "id", first)
    first = False;
    writeInsert(file_name, dbName, Gender, "Gender", first)
    # writeDel(rm_file, dbName, "Gender", first)
    writeInsert(file_name, dbName, Ethnicity, "Ethnicity", first)
    # writeDel(rm_file, dbName, "Ethnicity", first)
    writeInsert(file_name, dbName, Residency, "Residency", first)
    # writeDel(rm_file, dbName, "State", first)


if __name__ == '__main__':
    #main()
    #runs the main, and prints the time taken to run
    print timeit.timeit(main,number=1)