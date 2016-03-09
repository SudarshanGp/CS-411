__author__ = 'RDCERNHP'
import sqlite3
import os
import datetime

from HVAC_DB_Schema_Constants import *

def getAllRows(conn, ShelterInstanceId, EcuInstanceId, avgInterval, time_col_index):
    c = conn.cursor()
    queryString = "SELECT * from ShortestAvgShelterWeatherData where ShelterInstanceId = " + "'" + ShelterInstanceId + "'" + " and EcuInstanceId = " + "'" + EcuInstanceId + "'" + " and avgInterval = " + "'" + avgInterval + "'"
    c.execute(queryString)
    allRows = c.fetchall()

    output_list = []
    for row in range(len(allRows)):
        output_list.append([])
        for col in range(len(allRows[row])):
            if allRows[row][col] == 'NO_VALUE' or allRows[row][col] == 'OUT_OF_BOUNDS':
                output_list[row].append(9999)
            else:
                output_list[row].append(allRows[row][col])

    conn.commit()

    c.close()
    output_list = sorted(output_list, key=lambda x: datetime.datetime.strptime(x[time_col_index], '%Y-%m-%d %H:%M:%S'))
    return output_list

def pullInstances(rdbcon, pdbcon, Shelter_ID):
    p_cur = pdbcon.cursor()
    r_cur = rdbcon.cursor()

    queryString = "SELECT * from ShelterInstanceInfo where ShelterId = " + "'" + Shelter_ID + "'"
    r_cur.execute(queryString)
    allRows = r_cur.fetchall()

    instance_ID_list = []
    for row in range(len(allRows)):
        instance_ID_list.append(allRows[row][0])

    instance_pairs_list = []
    for instance in instance_ID_list:
        queryString = "SELECT * from ShortestAvgShelterWeatherData where ShelterInstanceId = " + "'" + str(instance) + "'"
        p_cur.execute(queryString)
        allRows = p_cur.fetchall()

        for row in range(len(allRows)):
            ECU_inst = str(allRows[row][1])
            instance_pairs_list.append(str(instance) + '_and_' + ECU_inst)

    instance_pairs_set = list(set(instance_pairs_list))

    instance_dict = {}
    for inst in instance_pairs_set:
        instance_dict[inst] = []

    for instance in instance_ID_list:
        queryString = "SELECT * from ShortestAvgShelterWeatherData where ShelterInstanceId = " + "'" + str(instance) + "'"
        p_cur.execute(queryString)
        allRows = p_cur.fetchall()
        for row in range(len(allRows)):
            ECU_inst = str(allRows[row][1])
            key = (str(instance) + '_and_' + ECU_inst)
            instance_dict[key].append([])
            for col in range(len(allRows[row])):
                if allRows[row][col] == 'NO_VALUE' or allRows[row][col] == 'OUT_OF_BOUNDS':
                    instance_dict[key][row].append(9999)
                else:
                    instance_dict[key][row].append(allRows[row][col])

    p_cur.close()
    r_cur.close()
    return instance_dict

def writeExcerptedData(conn, averaged_list):
    c = conn.cursor()
    for row in range(len(averaged_list)):
        cmd_text = """insert into ExcerptedShelterWeatherData values (?,?,?,?,?,?,?,?,?,?,?)"""
        c.execute(cmd_text, (averaged_list[row][0], averaged_list[row][1], averaged_list[row][2], averaged_list[row][3], averaged_list[row][4], averaged_list[row][5], averaged_list[row][6], averaged_list[row][7], averaged_list[row][8], averaged_list[row][9], averaged_list[row][10]))
    conn.commit()
    c.close()

def writeAveragedData(conn, averaged_list):
    c = conn.cursor()
    point_counter_list = [0]*2
    for row in range(len(averaged_list)):
        # if interior temp is less than ambient
        if averaged_list[row][5] < averaged_list[row][8]:
            # we are cooling
            point_counter_list[0] += 1
        else:
            # we are heating
            point_counter_list[1] += 1
        cmd_text = """insert into AveragedShelterWeatherData values (?,?,?,?,?,?,?,?,?,?,?)"""
        c.execute(cmd_text, (averaged_list[row][0], averaged_list[row][1], averaged_list[row][2], averaged_list[row][3], averaged_list[row][4], averaged_list[row][5], averaged_list[row][6], averaged_list[row][7], averaged_list[row][8], averaged_list[row][9], averaged_list[row][10]))
    conn.commit()
    c.close()
    return point_counter_list

def writeFirstAveragedData(conn, averaged_list):
    c = conn.cursor()
    for row in range(len(averaged_list)):
        cmd_text = """insert into ShortestAvgShelterWeatherData values (?,?,?,?,?,?,?,?,?,?,?)"""
        c.execute(cmd_text, (averaged_list[row][0], averaged_list[row][1], averaged_list[row][2], averaged_list[row][3], averaged_list[row][4], averaged_list[row][5], averaged_list[row][6], averaged_list[row][7], averaged_list[row][8], averaged_list[row][9], averaged_list[row][10]))
    conn.commit()
    c.close()

def writeDataGroupInfo(conn, datalist):
    c= conn.cursor()
    DataGroupInfo=[]
    execString= "SELECT * FROM DataGroupInfo"
    c.execute(execString)

    DatsGroupInfoRows=c.fetchall()
    for i in DatsGroupInfoRows:
        DataGroupInfo.append(i[0])

    conn.execute('pragma foreign_keys=ON')
    for j in datalist:
        if j[0] not in DataGroupInfo:
            cmd_text = """insert into DataGroupInfo values (?,?)"""
            c.execute(cmd_text, (j[0],j[1]))
    conn.commit()
    c.close()

def writeLocationInfo(conn, datalist):
    c= conn.cursor()
    LocationInfo=[]
    execString= "SELECT * FROM LocationInfo"
    c.execute(execString)

    LocationInfoRows=c.fetchall()
    for i in LocationInfoRows:
        LocationInfo.append(i[0])

    conn.execute('pragma foreign_keys=ON')
    for j in datalist:
        if j[0] not in LocationInfo:
            cmd_text = """insert into LocationInfo values (?,?)"""
            c.execute(cmd_text, (j[0],j[1]))
    conn.commit()
    c.close()

def writeECUTypeInfo(conn, cdb_conn, ID):
    c = conn.cursor()
    #cdb = cdb_conn.cursor()

    # Get info from Comps DB
    #queryString = "SELECT componentTypeName from ComponentType where componentTypeID = " + "'" + ID + "'"
    #cdb.execute(queryString)
    #componentTypeName = cdb.fetchone()[0]
    #cdb.close()

    EcuTypeInfo=[]
    execString= "SELECT * FROM ECUTypeInfo"
    c.execute(execString)

    EcuTypeInfoRows=c.fetchall()
    for i in EcuTypeInfoRows:
        EcuTypeInfo.append(i[0])

    conn.execute('pragma foreign_keys=ON')
    if ID not in EcuTypeInfo:
        cmd_text = """insert into ECUTypeInfo values (?,?)"""
        c.executemany(cmd_text, ID)
        #cmd_text = """insert into ECUTypeInfo values (?,?)"""
        #c.execute(cmd_text, (ID, componentTypeName))
    conn.commit()
    c.close()


def writeShelterTypeInfo(conn, cdb_conn, ID):
    c = conn.cursor()
    #cdb = cdb_conn.cursor()

    # Get info from Comps DB
    #queryString = "SELECT componentTypeName from ComponentType where componentTypeID = " + "'" + ID + "'"
    #cdb.execute(queryString)
    #componentTypeName = cdb.fetchone()[0]
    #cdb.close()

    EcuTypeInfo=[]
    execString= "SELECT * FROM ShelterTypeInfo"
    c.execute(execString)

    EcuTypeInfoRows=c.fetchall()
    for i in EcuTypeInfoRows:
        EcuTypeInfo.append(i[0])

    conn.execute('pragma foreign_keys=ON')
    if ID not in EcuTypeInfo:
        cmd_text = """insert into ShelterTypeInfo values (?,?)"""
        c.executemany(cmd_text, ID)
        #cmd_text = """insert into ShelterTypeInfo values (?,?)"""
        #c.execute(cmd_text, (ID, componentTypeName))
    conn.commit()
    c.close()

def writeWeatherStationInfo(conn, weather_station_info):
    c = conn.cursor()
    WeatherInfo=[]
    execString= "SELECT * FROM WeatherStationInfo"
    c.execute(execString)
    WeatherStationInfoRows=c.fetchall()
    for i in WeatherStationInfoRows:
        WeatherInfo.append(i[0])
    conn.execute('pragma foreign_keys=ON')
    for j in weather_station_info:
        if j[0] not in WeatherInfo:
            cmd_text = """insert into WeatherStationInfo values (?,?,?)"""
            c.execute(cmd_text, (j[0],j[1],j[2]))
    conn.commit()
    c.close()

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

def writeShelterInstanceInfo(conn, data_list):
    c= conn.cursor()
    conn.execute('pragma foreign_keys=ON')
    cmd_text = """insert into ShelterInstanceInfo values (?,?,?,?)"""
    c.executemany(cmd_text, data_list)
    conn.commit()
    c.close()
def writeWeatherData(conn, data_list):
    c= conn.cursor()
    conn.execute('pragma foreign_keys=ON')
    cmd_text = """insert into WeatherData values (?,?,?,?,?,?,?,?,?,?,?)"""
    # print data_list
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

def writeShelterData(conn, data_list):
    c= conn.cursor()
    conn.execute('pragma foreign_keys=ON')
    cmd_text = """insert into ShelterData values (?,?,?,?,?,?,?,?,?,?,?)"""
    c.executemany(cmd_text, data_list)
    conn.commit()
    c.close()

def writeAvgShelterWeatherData(conn, data_list):
    c= conn.cursor()
    conn.execute('pragma foreign_keys=ON')
    cmd_text = """insert into AvgShelterWeatherData values (?,?,?,?,?,?,?,?,?,?,?,?)"""
    c.executemany(cmd_text, data_list)
    conn.commit()
    c.close()
def writeShelterWeatherData(conn, data_list):
    c= conn.cursor()
    conn.execute('pragma foreign_keys=ON')
    cmd_text = """insert into ShelterWeatherData values (?,?,?,?,?,?,?,?,?,?,?,?)"""
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

    c.execute(''' CREATE TABLE ShortestAvgShelterWeatherData (
    ShelterInstanceId CHAR(30) not null,
    ECUInstanceId CHAR(30) not null,
    timestamp DATETIME not null,
    avgInterval int not null,
    avgInteriorAirTemp FLOAT not null, --in F
    avgECUPower FLOAT not null, --in kW
    avgPlugLoad FLOAT not null, -- in kW
    ambientAirTemp FLOAT not null, --in F
    globalHorizontalSolar FLOAT not null, --in W/m2
    relativeHumidity FLOAT not null, --in percent
    windSpeed FLOAT not null, --in mph
    primary key (ShelterInstanceId, EcuInstanceId, timestamp, avgInterval)
    )''')

    c.execute(''' CREATE TABLE AveragedShelterWeatherData (
    ShelterInstanceId CHAR(30) not null,
    ECUInstanceId CHAR(30) not null,
    timestamp DATETIME not null,
    avgInterval int not null,
    avgInteriorAirTemp FLOAT not null, --in F
    avgECUPower FLOAT not null, --in kW
    avgPlugLoad FLOAT not null, -- in kW
    ambientAirTemp FLOAT not null, --in F
    globalHorizontalSolar FLOAT not null, --in W/m2
    relativeHumidity FLOAT not null, --in percent
    windSpeed FLOAT not null, --in mph
    primary key (ShelterInstanceId, EcuInstanceId, timestamp, avgInterval)
    )''')

    c.execute(''' CREATE TABLE ExcerptedShelterWeatherData (
    ShelterInstanceId CHAR(30) not null,
    ECUInstanceId CHAR(30) not null,
    timestamp DATETIME not null,
    avgInterval int not null,
    avgInteriorAirTemp FLOAT not null, --in F
    avgECUPower FLOAT not null, --in kW
    avgPlugLoad FLOAT not null, -- in kW
    ambientAirTemp FLOAT not null, --in F
    globalHorizontalSolar FLOAT not null, --in W/m2
    relativeHumidity FLOAT not null, --in percent
    windSpeed FLOAT not null, --in mph
    primary key (ShelterInstanceId, EcuInstanceId, timestamp, avgInterval)
    )''')

    c.execute(''' CREATE TABLE ShelterWeatherDataWithModel (
    ShelterInstanceId CHAR(30) not null,
    ECUInstanceId CHAR(30) not null,
    timestamp DATETIME not null,
    avgInterval int not null,
    avgInteriorAirTemp FLOAT not null, --in F
    avgECUPower FLOAT not null, --in kW
    avgPlugLoad FLOAT not null, -- in kW
    ambientAirTemp FLOAT not null, --in F
    globalHorizontalSolar FLOAT not null, --in W/m2
    relativeHumidity FLOAT not null, --in percent
    windSpeed FLOAT not null, --in mph
    paramsID INT not null,
    QCalc FLOAT not null,
    PwrCalc FLOAT not null,
    primary key (ShelterInstanceId, EcuInstanceId, timestamp, avgInterval, paramsID)
    )''')

    c.execute(''' CREATE TABLE ShelterWeatherDataWithBESTModel (
    ShelterInstanceId CHAR(30) not null,
    ECUInstanceId CHAR(30) not null,
    timestamp DATETIME not null,
    avgInterval int not null,
    avgInteriorAirTemp FLOAT not null, --in F
    avgECUPower FLOAT not null, --in kW
    avgPlugLoad FLOAT not null, -- in kW
    ambientAirTemp FLOAT not null, --in F
    globalHorizontalSolar FLOAT not null, --in W/m2
    relativeHumidity FLOAT not null, --in percent
    windSpeed FLOAT not null, --in mph
    paramsID INT not null,
    QCalc FLOAT not null,
    PwrCalc FLOAT not null,
    primary key (ShelterInstanceId, EcuInstanceId, timestamp, avgInterval, paramsID)
    )''')

    c.execute(''' CREATE TABLE ParametersInfo (
    paramsID INT not null,
    LUMPED_HEAT_TRANSFER_COEFFICIENT FLOAT not null,
    LUMPED_SOLAR_COEFFICIENT FLOAT not null,
    MAX_Q_HEAT FLOAT not null,
    HIHEAT FLOAT not null,
    MAX_Q_COOL FLOAT not null,
    HICOOL FLOAT not null,
    LOW_Q_HEAT FLOAT not null,
    LOWHEAT FLOAT not null,
    LOW_Q_COOL FLOAT not null,
    LOWCOOL FLOAT not null,
    RMSE FLOAT not null,
    TOTAL_ERROR FLOAT not null,
    COMBINED_OBJ_FCN FLOAT not null,
    primary key (paramsID)
    )''')

    conn.commit()
    conn.close()

def initializeHVACDB(db_name):
    """Initialize DB - Note this clobbers all previous DBs!"""
    try:
        os.remove(db_name)
    except:
        pass
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''CREATE TABLE LocationInfo (
    LocationId CHAR(20) not null primary key,
    Description VARCHAR(100) not null
    )''')

    c.execute('''CREATE TABLE WeatherStationInfo (
    WeatherStationId CHAR(20) not null primary key,
    LocationId CHAR(20) not null,
    Description VARCHAR(100) not null
    )''')

    c.execute('''CREATE TABLE DataGroupInfo (
    DataGroupId CHAR(20) not null primary key,
    Description VARCHAR(100) not null
    )''')

    c.execute('''CREATE TABLE DataSetInfo (
    DataSetId CHAR(20) not null primary key,
    DataGroupId CHAR(20) not null references DataGroupInfo(DataGroupId),
    LocationId CHAR(20) not null references LocationInfo(LocationId),
    Description VARCHAR(100) not null,
    SensorsDescription VARCHAR(500) not null,
    DocumentationDescription VARCHAR(500) not null
    )''')

    # These are just copies of Components DB info
    c.execute('''CREATE TABLE ECUTypeInfo (
    componentTypeID CHAR(20) not null primary key,
    componentTypeName VARCHAR(100) not null
    )''')

    c.execute('''CREATE TABLE ShelterTypeInfo (
    componentTypeID CHAR(20) not null primary key,
    componentTypeName VARCHAR(100) not null
    )''')

    c.execute('''CREATE TABLE ShelterInstanceInfo (
    ShelterInstanceId CHAR(30) not null primary key,
    ShelterId CHAR(20) not null references ShelterTypeInfo(componentTypeID),
    LocationId CHAR(20) not null references LocationInfo(LocationId),
    Description VARCHAR(100) not null
    )''')

    c.execute('''CREATE TABLE ECUInstanceInfo (
    ECUInstanceId CHAR(30) not null primary key,
    ECUId CHAR(20) not null references ECUTypeInfo(componentTypeID),
    LocationId CHAR(20) not null references LocationInfo(LocationId),
    Description VARCHAR(100) not null
    )''')

    # '_' as a prefix indicates "bad" data
    c.execute(''' CREATE TABLE WeatherData (
    WeatherStationId CHAR(20) not null references WeatherStationInfo(WeatherStationId),
    timestamp DATETIME not null,
    avgInterval int not null,
    ambientAirTemp FLOAT DEFAULT null, --in F
    globalHorizontalSolar FLOAT DEFAULT null, --in W/m2
    relativeHumidity FLOAT DEFAULT null, --in percent
    windSpeed FLOAT DEFAULT null, --in mph
    _ambientAirTemp FLOAT DEFAULT null, --in F
    _globalHorizontalSolar FLOAT DEFAULT null, --in W/m2
    _relativeHumidity FLOAT DEFAULT null, --in percent
    _windSpeed FLOAT DEFAULT null, --in mph
    primary key (WeatherStationId, timestamp, avgInterval)
    )''')

    c.execute(''' CREATE TABLE ECUData (
    ShelterInstanceId CHAR(30) not null references ShelterInstanceInfo(ShelterInstanceId),
    ECUInstanceId CHAR(30) not null references EcuInstanceInfo(EcuInstanceId),
    DataSetId CHAR(20) not null references DataSetInfo(DataSetId),
    timestamp DATETIME not null,
    avgInterval int not null,
    avgECUPower FLOAT DEFAULT null, --in kW
    ECUMode TEXT DEFAULT null, --would be nice to know
    _avgECUPower FLOAT DEFAULT null, --in kW
    _ECUMode TEXT DEFAULT null, --would be nice to know
    primary key (ShelterInstanceId, EcuInstanceId, DataSetId, timestamp, avgInterval)
    )''')

    c.execute(''' CREATE TABLE ShelterData (
    ShelterInstanceId CHAR(30) not null references ShelterInstanceInfo(ShelterInstanceId),
    EcuInstanceId CHAR(30) not null references EcuInstanceInfo(EcuInstanceId),
    DataSetId CHAR(20) not null references DataSetInfo(DataSetId),
    timestamp DATETIME not null,
    avgInterval int not null,
    avgInteriorAirTemp FLOAT DEFAULT null, --in F
    avgPlugLoad FLOAT DEFAULT null, -- in kW
    avgOccupancy FLOAT DEFAULT null, --also nice to know
    _avgInteriorAirTemp FLOAT DEFAULT null, --in F
    _avgPlugLoad FLOAT DEFAULT null, -- in kW
    _avgOccupancy FLOAT DEFAULT null, --also nice to know
    primary key (ShelterInstanceId, EcuInstanceId, DataSetId, timestamp, avgInterval)
    )''')
    conn.commit()
    conn.close()

def writeModelData(conn, modeled_list, params_list, best_errors, last_flag):
    best_RMSE = best_errors[0][0]
    best_Total_Error = best_errors[0][1]
    best_combined_obj_fcn = best_errors[0][2]
    best_params = best_errors[0][3]
    best_row_data = best_errors[1]
    good_paramIDs = []
    c = conn.cursor()
    for row in range(len(params_list)):
        if params_list[row][11] < best_RMSE:
            best_RMSE = params_list[row][11]
            # good_paramIDs.append(params_list[row][0])
        if params_list[row][12] < best_Total_Error:
            best_Total_Error = params_list[row][12]
            # good_paramIDs.append(params_list[row][0])
        if params_list[row][13] < best_combined_obj_fcn:
            best_combined_obj_fcn = params_list[row][13]
            good_paramIDs.append(params_list[row][0])
            best_params = params_list[row]
        cmd_text = """insert into ParametersInfo values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        c.execute(cmd_text, (params_list[row][0], params_list[row][1], params_list[row][2], params_list[row][3], params_list[row][4], params_list[row][5], params_list[row][6], params_list[row][7], params_list[row][8], params_list[row][9], params_list[row][10], params_list[row][11], params_list[row][12], params_list[row][13]))
    conn.commit()
    c.close()

    good_paramIDs = list(set(good_paramIDs))

    c = conn.cursor()
    if len(good_paramIDs) > 0:
        best_row_data = []
    for row in range(len(modeled_list)):
        if modeled_list[row][11] in good_paramIDs:
            cmd_text = """insert into ShelterWeatherDataWithModel values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
            c.execute(cmd_text, (modeled_list[row][0], modeled_list[row][1], modeled_list[row][2], modeled_list[row][3], modeled_list[row][4], modeled_list[row][5], modeled_list[row][6], modeled_list[row][7], modeled_list[row][8], modeled_list[row][9], modeled_list[row][10], modeled_list[row][11], modeled_list[row][12], modeled_list[row][13]))
            if modeled_list[row][11] == max(good_paramIDs):
                best_row_data.append(modeled_list[row])
    conn.commit()
    c.close()

    if last_flag == 1:
        c = conn.cursor()
        for row in range(len(best_row_data)):
            cmd_text = """insert into ShelterWeatherDataWithBESTModel values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
            c.execute(cmd_text, (best_row_data[row][0], best_row_data[row][1], best_row_data[row][2], best_row_data[row][3], best_row_data[row][4], best_row_data[row][5], best_row_data[row][6], best_row_data[row][7], best_row_data[row][8], best_row_data[row][9], best_row_data[row][10], best_row_data[row][11], best_row_data[row][12], best_row_data[row][13]))
        conn.commit()
        c.close()
    return [[best_RMSE, best_Total_Error, best_combined_obj_fcn, best_params], best_row_data]