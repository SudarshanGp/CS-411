import xlrd #for reading .xlsx files


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
                Departmentlist.append(current_sheet.cell(i,5).value)
                dep += 1
                Department[Departmentlist[dep-1]]=[]
                
                continue
        
            if(current_sheet.cell(i,5).value!=''):
                if (current_sheet.cell(i,5).value not in Department[Departmentlist[dep-1]]):
                    Department[Departmentlist[dep-1]].append(current_sheet.cell(i,5).value)
                    counter += 1
                if counter in counterlist:
                    #find same counter and add the points
                    for i in range(0,len(Gender)):
                        if(Gender[i][0]==counter):
                            #print Gender[i][0]
                            #print type(Gender[i][1])
                            #print type(current_sheet.cell(i,9).value)
                            try:
                                print ((current_sheet.cell(i,9).value).decode('utf-8'))
                            except TypeError and AttributeError:
                                print type(current_sheet.cell(i,9).value)
                            #add the list together
                            #Gender[i][1]+= int(current_sheet.cell(i,9).value)
                            #Gender[i][2]+=current_sheet.cell(i,10).value
                            #Gender[i][3]+=current_sheet.cell(i,11).value
                    
                        if(Ethnicity[i][0]==counter):
                            #could change this too a for loop.
                            #Ethnicity[i][1]+=current_sheet.cell(i,12).value
                            #Ethnicity[i][2]+=current_sheet.cell(i,13).value
                            #Ethnicity[i][3]+=current_sheet.cell(i,14).value
                            #Ethnicity[i][4]+=current_sheet.cell(i,15).value
                            #Ethnicity[i][5]+=current_sheet.cell(i,16).value
                            #Ethnicity[i][6]+=current_sheet.cell(i,17).value
                            #Ethnicity[i][7]+=current_sheet.cell(i,18).value
                            #Ethnicity[i][8]+=current_sheet.cell(i,19).value
                            #Ethnicity[i][9]+=current_sheet.cell(i,20).value
                            pass
                        if(Residency[i][0]==counter):
                            #Residency[i][1]+=current_sheet.cell(i,19).value
                            #Residency[i][2]+=current_sheet.cell(i,20).value
                            pass
                else:
                    counterlist.append(counter)
                
                    Gender.append([counter,current_sheet.cell(i,9).value, current_sheet.cell(i,10).value, current_sheet.cell(i,11).value])
                
                    Ethnicity.append([counter,current_sheet.cell(i,12).value,current_sheet.cell(i,13).value,current_sheet.cell(i,14).value, 
                                    current_sheet.cell(i,15).value, current_sheet.cell(i,16).value, current_sheet.cell(i,17).value, 
                                    current_sheet.cell(i,18).value, current_sheet.cell(i,19).value, current_sheet.cell(i,20).value])
                    Residency.append([counter,current_sheet.cell(i,19).value,current_sheet.cell(i,20).value])
   
    
    return Department,Gender,Ethnicity,Residency
    
def main():
    FilePar("ethsexfa10.xls")
if __name__ == '__main__':
    main()
