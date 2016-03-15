DROP DATABASE IF EXISTS db;
CREATE DATABASE db;
DROP TABLE IF EXISTS db.AcademicCollege;
CREATE TABLE db.AcademicCollege (
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
    );
DROP TABLE IF EXISTS db.Ethnicity;
CREATE TABLE db.Ethnicity (
    Year VARCHAR(8) not null,
    AfAm int not null,
    Asian int not null,
    Hisp int not null,
    Multi int not null,
    NativeAmAl int not null,
    NativeHaw int not null,
    White int not null,
    Foreigner int not null,
    Other int not null,
    Total int not null,
    primary key (Year)
    );
DROP TABLE IF EXISTS db.Gender;
CREATE TABLE db.Gender (
    Year VARCHAR(8) not null,
    Male int not null,
    Female int not null,
    Total int not null,
    primary key (Year)
    );
DROP TABLE IF EXISTS db.State;
CREATE TABLE db.State (
    Year VARCHAR(8) not null,
    Alabama int not null,
    Alaska int not null,
    Arizona int not null,
    Arkansas int not null,
    California int not null,
    Colorado int not null,
    Connecticut int not null,
    Delaware int not null,
    DistrictOfColumbia int not null,
    Florida int not null,
    Georgia int not null,
    Guam int not null,
    Hawaii int not null,
    Idaho int not null,
    Illinois int not null,
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
    NewHampshire int not null,
    NewJersey int not null,
    NewMexico int not null,
    NewYork int not null,
    NorthCarolina int not null,
    NorthDakota int not null,
    Ohio int not null,
    Oklahoma int not null,
    Oregon int not null,
    Pennsylvania int not null,
    PuertoRico int not null,
    RhodeIsland int not null,
    SouthCarolina int not null,
    SouthDakota int not null,
    Tennessee int not null,
    Texas int not null,
    Utah int not null,
    Vermont int not null,
    Virginia int not null,
    Washington int not null,
    WestVirginia int not null,
    Wisconsin int not null,
    Wyoming int not null,
    Military int not null,
    International int not null,
    Other int not null,
    Total int not null,
    primary key (Year)
    );
INSERT INTO db.AcademicCollege VALUES('fa14',436,196,571,131,1566,303,1474,2074,156,30,6937);
INSERT INTO db.Gender VALUES('fa14',3834,3103,6937);
INSERT INTO db.Ethnicity VALUES('fa14',356,1352,719,188,6,5,3198,1059,54,6937);
INSERT INTO db.State VALUES('fa14',5,2,10,6,220,17,8,2,3,25,20,0,0,3,4927,21,10,5,12,2,0,14,22,22,23,1,33,0,3,2,1,79,4,63,6,0,33,0,6,19,4,2,2,2,10,35,4,0,36,22,0,16,0,2,1061,112,6882);
