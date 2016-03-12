-- DROP TABLE IF EXISTS AcademicCollege;
CREATE DATABASE db;
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
INSERT INTO db.AcademicCollege VALUES('fa14',436,196,571,131,1566,303,1474,2074,156,30,6937);
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
    blah int not null,
    Total int not null,
    primary key (Year)
    );
INSERT INTO db.Ethnicity VALUES('fa14',356,1352,719,188,6,5,3198,1059,54,6937);
DROP TABLE IF EXISTS db.Gender;
CREATE TABLE db.Gender (
    Year VARCHAR(8) not null,
    Male int not null,
    Female int not null,
    Total int not null,
    primary key (Year)
    );
INSERT INTO db.Gender VALUES('fa14',3834,3103,6937);
DROP TABLE IF EXISTS db.State;
CREATE TABLE db.State (
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
    OtherCountries int null,
    blah int null,
    Total int not null,
    primary key (Year)
    );
INSERT INTO db.State VALUES('fa14',5,2,10,6,220,17,8,2,3,25,20,'',3,4927,21,10,5,12,2,'',14,22,22,23,1,33,'',3,2,1,79,4,63,6,'',33,'',6,19,4,2,2,2,10,35,4,36,'',22,'',16,'',2,1061,112,6886);
