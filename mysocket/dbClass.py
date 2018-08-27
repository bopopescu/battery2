# -*- coding: utf-8 -*-
# @Author: wx
# @Date:   2018-05-16 14:18:31
# @Last Modified by:   wx
# @Last Modified time: 2018-06-07 10:50:25

import pymysql
import json
from datetime import datetime
from apps.models import *


class dbClass(object):
    """docstring for dbClass"""

    def __init__(self):
        try:
            with open("db_config.json", 'r') as f:
                filetext = f.read()
        except Exception as e:
            raise e

        configJson = json.loads(filetext)
        self.host = configJson['host']
        self.port = int(configJson['port'])
        self.user = configJson['user']
        self.passwd = configJson['passwd']
        self.db = configJson['db']
        self.cellDeviceTable = configJson['cellDeviceTable']
        self.boxDeviceTable = configJson['boxDeviceTable']
        self.cellDeviceTable = configJson["cellDeviceTable"]
        self.H2DeviceTable = configJson["H2DeviceTable"]
        self.H2ODeviceTable = configJson["H2ODeviceTable"]
        self.CO2DeviceTable = configJson["CO2DeviceTable"]
        self.CH4DeviceTable = configJson["CH4DeviceTable"]
        self.N2DeviceTable = configJson["N2DeviceTable"]
        self.AIRDeviceTable = configJson["AIRDeviceTable"]
        self.wdjDeviceTable = configJson["wdjDeviceTable"]
        self.ovenDeviceTable = configJson["ovenDeviceTable"]
        self.ovenPlanTable = configJson["ovenPlanTable"]
        self.ovenPlanDetailTable = configJson["ovenPlanDetailTable"]
        self.cellPlanTable = configJson["cellPlanTable"]
        self.cellPlanDetailTable = configJson["cellPlanDetailTable"]
        self.BigTestInfoTable = configJson["BigTestInfoTable"]
        self.testInfoTable = configJson["testInfoTable"]
        self.cellTestRealDataTable = configJson["cellTestRealDataTable"]
        self.eventTable = configJson["eventTable"]
        self.cellTestHistoryDataTable = configJson["cellHistoryDataTable"]

    def updateCellDeviceTable(self, boxid, chnNum, datadict):
        dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                       db=self.db,
                                       charset="utf8")
        cursor = dbconnection.cursor()

        ROWstr = ''

        # UPDATE table_name SET field1=new-value1, field2=new-value2 WHERE runoob_id=3;

        from collections import Iterable
        a = isinstance(datadict, Iterable)
        for key in datadict:
            if isinstance(datadict[key], str) == True:
                ROWstr = ROWstr + key + '=\'' + datadict[key] + '\','
            else:
                ROWstr = ROWstr + key + '=' + str(datadict[key]) + ','

        ROWstr = ROWstr[:-1];
        ROWstr = ROWstr + ' '

        sql = 'update ' + self.cellDeviceTable + ' SET ' + ROWstr + 'where (boxID_id = ' + str(
            boxid) + ') and ' + '(chnNum = ' + str(chnNum) + ')'

        # print(sql)
        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)
            dbconnection.rollback()
        dbconnection.commit()
        dbconnection.close()

    def updateCellDeviceTable_Gas_Temp(self, cellid, datadict):
        dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                       db=self.db,
                                       charset="utf8")
        cursor = dbconnection.cursor()

        ROWstr = ''

        # UPDATE table_name SET field1=new-value1, field2=new-value2 WHERE runoob_id=3;

        from collections import Iterable
        a = isinstance(datadict, Iterable)
        for key in datadict:
            if isinstance(datadict[key], str) == True:
                ROWstr = ROWstr + key + '=\'' + datadict[key] + '\','
            else:
                ROWstr = ROWstr + key + '=' + str(datadict[key]) + ','

        ROWstr = ROWstr[:-1];
        ROWstr = ROWstr + ' '

        sql = 'update ' + self.cellDeviceTable + ' SET ' + ROWstr + 'where (cellID = ' + str(cellid) + ')'

        # print(sql)
        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)
            dbconnection.rollback()
        dbconnection.commit()
        dbconnection.close()

    def executeGetSQL(self, sql):
        dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                       db=self.db, charset="utf8")
        cursor = dbconnection.cursor()
        result = None
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            # print (type(result))
            # print(result)
        except Exception as e:
            print(e)
            dbconnection.rollback()
        dbconnection.commit()
        dbconnection.close()
        return result

    def getBoxComInfo(self):
        # sql = 'SELECT boxID, boxIP, boxPort, cellID_id FROM ' + self.boxDeviceTable
        sql = 'SELECT * FROM ' + self.boxDeviceTable
        result = self.executeGetSQL(sql)
        return result

    def getGasComInfo(self):
        # sql = 'SELECT qCoef, qIP, qPort, cellID_id, type_id FROM ' + self.gasDeviceTable
        sql = 'SELECT * FROM ' + self.gasDeviceTable
        # print(sql)
        result = self.executeGetSQL(sql)
        return result

    def getTemComInfo(self):
        # sql = 'SELECT qCoef, qIP, qPort, cellID_id, type_id FROM ' + self.temDeviceTable
        sql = 'SELECT * FROM ' + self.temDeviceTable
        # print(sql)
        result = self.executeGetSQL(sql)
        return result

    def getCellInfo(self):
        sql = 'SELECT cellID, boxID_id, chnNum FROM ' + self.cellDeviceTable
        result = self.executeGetSQL(sql)
        return result

    def getCellsUnderHandle(self):
        sql = 'SELECT cellID_id, boxID, chnNum, planID_id, testID_id, currState, nextState FROM ' + self.cellTestRealDataTable + ' WHERE (currState!=nextState) OR ((currState=\'start\') AND (nextState=\'start\' )) '
        result = self.executeGetSQL(sql)
        return result

    def getCellsTestPlan(self):
        sql = 'SELECT * FROM ' + self.cellPlanTable + ' WHERE planID_id in (SELECT planID_id FROM ' + self.cellRealDataTable + ' WHERE (currState!=nextState) OR ((currState=\'start\') AND (nextState=\'start\' ))  OR (currOvenState!=nextOvenState) OR (H2curr!=H2next) OR (N2curr!=N2next) OR (CO2curr!=CO2next) OR (H2Ocurr!=H2Onext) OR (CH4curr!=CH4next) OR (AIRcurr!=AIRnext) ORDER BY step ASC)'
        result = self.executeGetSQL(sql)
        return result

    def getCellsComponetCOM(self):
        sql = 'SELECT * FROM ' + self.cellDeviceTable + ' WHERE cellID in (SELECT cellID FROM ' + self.cellRealDataTable + ' WHERE (currState!=nextState) OR ((currState=\'start\') AND (nextState=\'start\' ))'
        result = self.executeGetSQL(sql)
        return result

    def getOvenUnderHandle(self):
        sql = 'SELECT ID, currState, nextState, IP, PortNum, Addr, ovenPlanID_id FROM ' + self.ovenDeviceTable + ' WHERE (currState!=nextState)'
        result = self.executeGetSQL(sql)
        return result

    def getOvenTestPlan(self):
        sql = 'SELECT * FROM' + self.ovenDeviceTable + 'WHERE planID_id in (SELECT planID_id FROM ' + self.cellRealDataTable + ' WHERE (currState != nextState) OR((currState=\'start\') AND (nextState=\'start\' )) ORDER BY step ASC)'
        result = self.executeGetSQL(sql)
        return result

    def executeInsertSQL(self, datadict, table):
        dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                       db=self.db, charset="utf8")
        cursor = dbconnection.cursor()
        ROWstr = []
        COLstr = ''
        ss = ''
        from collections import Iterable
        a = isinstance(datadict, Iterable)
        for key in datadict:
            ROWstr.append(datadict[key])
            COLstr = COLstr + key + ','
            ss = ss + '%s' + ','
        COLstr = COLstr[:-1]
        ss = ss[:-1]
        sql = "insert into  " + table + "(" + COLstr + ") values (" + ss + ")"
        try:
            cursor.execute(sql, ROWstr)
            dbconnection.commit()
        except Exception as e:
            print(e)
            dbconnection.rollback()
        dbconnection.close()

    def insertCellALLRealData(self, datadict):
        self.executeInsertSQL(self, datadict, self.cellTestHistoryDataTable)

    def updateCellRealData(self, cellid, datadict):
        dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                       db=self.db,
                                       charset="utf8")
        cursor = dbconnection.cursor()

        ROWstr = ''

        from collections import Iterable
        a = isinstance(datadict, Iterable)
        for key in datadict:
            if isinstance(datadict[key], str) == True:
                ROWstr = ROWstr + key + '=\'' + datadict[key] + '\','
            else:
                ROWstr = ROWstr + key + '=' + str(datadict[key]) + ','

        ROWstr = ROWstr[:-1];
        ROWstr = ROWstr + ' '

        sql = 'update ' + self.cellRealDataTable + ' SET ' + ROWstr + 'where (cellID_id = ' + str(cellid) + ')'

        # print(sql)
        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)
            dbconnection.rollback()
        dbconnection.commit()
        dbconnection.close()
