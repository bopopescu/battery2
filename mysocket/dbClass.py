# -*- coding: utf-8 -*-
# @Author: wx
# @Date:   2018-05-16 14:18:31
# @Last Modified by:   wx
# @Last Modified time: 2018-06-07 10:50:25

import pymysql
import json
from datetime import datetime


class dbClass(object):
    """docstring for dbClass"""

    def __init__(self):
        try:
            with open("db_config.json", 'r') as f:
                filetext = f.read()
        except Exception as e:
            print(e)
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
        self.cellTestHistoryDataTable = configJson["cellTestHistoryDataTable"]

    def updateCellDeviceTable(self, boxid, chnNum, datadict):
        while True:
            try:
                dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                       db=self.db,charset="utf8")
                break
            except Exception as e:
                print(e)
                print("cannot connect to mysql, retrying........................")

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
        while True:
            try:
                dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                       db=self.db,charset="utf8")
                break
            except Exception as e:
                print(e)
                print("cannot connect to mysql, retrying........................")
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

    def executeGetSQL(self, sql, keys):
        while True:
            try:
                dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                       db=self.db,charset="utf8")
                break
            except Exception as e:
                print(e)
                print("cannot connect to mysql, retrying........................")
        cursor = dbconnection.cursor()
        r_list = []
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            for i in result:
                data = {}
                for j in range(0, len(keys)):
                    data[keys[j]] = i[j]
                r_list.append(data)
        except Exception as e:
            print(e)
            dbconnection.rollback()
        dbconnection.commit()
        dbconnection.close()
        return r_list

    def getCellsUnderHandle(self):
        print("get cell under handle")
        keys = ["cellID_id", "boxID_id", "testID_id", "bigTestID_id", "chnNum", "currState", "nextState"]
        keystr = ",".join(keys)
        sql = 'SELECT ' + keystr + ' FROM ' + self.cellTestRealDataTable + ' WHERE (currState!=nextState)'
        result = self.executeGetSQL(sql, keys)
        print("cell under handle:" + str(result))
        return result

    def getCellsTestPlan(self, cell):
        keys = ["planID_id", ]
        sql = 'SELECT planID_id FROM ' + self.testInfoTable + ' WHERE id=' + str(cell["testID_id"])
        result = self.executeGetSQL(sql, keys)
        keys = ["id", "planID_id", "step", "mode", "i", "u", "r", "p", "n", "nStart", "nStop", "nTarget", "tTH", "iTH",
                "uTH", "qTH"]
        keystr = ",".join(keys)
        sql = 'SELECT ' + keystr + ' FROM ' + self.cellPlanDetailTable + ' WHERE planID_id=' + str(result[0]["planID_id"]) + ' ORDER BY step'
        result = self.executeGetSQL(sql, keys)
        return result

    def getCellsComponetCOM(self, cell):
        keys = ["cellID", "chnNum", "boxID_id", "mAIRID_id", "mH2ID_id", "mCH4ID_id", "mN2ID_id", "mAIRID_id",
                "mH2OID_id", "mT1ID_id", "mT0ID_id"]
        keystr = ",".join(keys)
        sql = "SELECT " + keystr + " FROM " + self.cellDeviceTable + " WHERE cellID=" + str(cell["cellID_id"])
        cellDevice = self.executeGetSQL(sql, keys)[0]

        keys = ["ID", "IP", "PortNum", "Addr", "totalChnNum"]
        keystr = ",".join(keys)
        sql = "SELECT " + keystr + " FROM " + self.boxDeviceTable + " WHERE ID=" + str(cellDevice["boxID_id"])
        data = self.executeGetSQL(sql, keys)
        data[0]["chnNum"] = cellDevice["chnNum"]
        data[0]["cellID"] = cellDevice["cellID"]
        return data

    def getGasCOM(self, type, llj):
        keys = ["ID", "IP", "PortNum", "Addr"]
        keystr = ",".join(keys)
        if type == "H2":
            sql = "SELECT " + keystr + " FROM " + self.H2DeviceTable + " WHERE ID=" + str(llj["H2ID_id"])
        elif type == "N2":
            sql = "SELECT " + keystr + " FROM " + self.N2DeviceTable + " WHERE ID=" + str(llj["N2ID_id"])
        elif type == "CH4":
            sql = "SELECT " + keystr + " FROM " + self.CH4DeviceTable + " WHERE ID=" + str(llj["CH4ID_id"])
        elif type == "CO2":
            sql = "SELECT " + keystr + " FROM " + self.CO2DeviceTable + " WHERE ID=" + str(llj["CO2ID_id"])
        elif type == "AIR":
            sql = "SELECT " + keystr + " FROM " + self.AIRDeviceTable + " WHERE ID=" + str(llj["AIRID_id"])
        elif type == "H2O":
            sql = "SELECT " + keystr + " FROM " + self.H2ODeviceTable + " WHERE ID=" + str(llj["H2OID_id"])
        data = self.executeGetSQL(sql, keys)
        return data

    def getOvenCOM(self, oven):
        keys = ["ID", "IP", "PortNum", "Addr"]
        keystr = ",".join(keys)
        sql = "SELECT " + keystr + " FROM " + self.ovenDeviceTable + " WHERE ID=" + str(oven["ovenID_id"])
        data = self.executeGetSQL(sql, keys)
        return data

    def getWdjCOM(self, wdj):
        keys = ["ID", "IP", "PortNum", "Addr"]
        keystr = ",".join(keys)
        sql = "SELECT " + keystr + " FROM " + self.wdjDeviceTable + " WHERE ID=" + str(wdj["wdjID_id"])
        data = self.executeGetSQL(sql, keys)
        return data

    def getOvenUnderHandle(self):
        print("get oven under handle")
        keys = ["ID", "currState", "nextState", "IP", "PortNum", "Addr", "ovenPlanID_id"]
        keystr = ",".join(keys)
        sql = 'SELECT ' + keystr + ' FROM ' + self.ovenDeviceTable + ' WHERE (currState!=nextState)'
        result = self.executeGetSQL(sql, keys)
        print("oven under handle:"+str(result))
        return result

    def getLljUnderHandle(self):
        print("get MFC under handle")
        keys = ["ID", "currState", "nextState", "IP", "PortNum", "Addr"]
        keystr = ",".join(keys)
        data = []

        sql = 'SELECT ' + keystr + ' FROM ' + self.N2DeviceTable + ' WHERE (currState!=nextState)'
        result = self.executeGetSQL(sql, keys)
        for i in result:
            i["type"] = "N2"
        data = data + result

        sql = 'SELECT ' + keystr + ' FROM ' + self.H2DeviceTable + ' WHERE (currState!=nextState)'
        result = self.executeGetSQL(sql, keys)
        for i in result:
            i["type"] = "H2"
        data = data + result

        sql = 'SELECT ' + keystr + ' FROM ' + self.H2ODeviceTable + ' WHERE (currState!=nextState)'
        result = self.executeGetSQL(sql, keys)
        for i in result:
            i["type"] = "H2O"
        data = data + result

        sql = 'SELECT ' + keystr + ' FROM ' + self.CO2DeviceTable + ' WHERE (currState!=nextState)'
        result = self.executeGetSQL(sql, keys)
        for i in result:
            i["type"] = "CO2"
        data = data + result

        sql = 'SELECT ' + keystr + ' FROM ' + self.CH4DeviceTable + ' WHERE (currState!=nextState)'
        result = self.executeGetSQL(sql, keys)
        for i in result:
            i["type"] = "CH4"
        data = data + result

        sql = 'SELECT ' + keystr + ' FROM ' + self.AIRDeviceTable + ' WHERE (currState!=nextState)'
        result = self.executeGetSQL(sql, keys)
        for i in result:
            i["type"] = "AIR"
        data = data + result
        print("MFC under handle:" + str(result))
        return result

    def getOvenTestPlan(self, oven):
        keys = ["id", "step", "T", "time", "ovenPlanID_id"]
        keystr = ",".join(keys)
        sql = 'SELECT ' + keystr + ' FROM ' + self.ovenPlanDetailTable + ' WHERE ovenPlanID_id=' + str(oven["ovenPlanID_id"]) + ' ORDER BY step '
        result = self.executeGetSQL(sql, keys)
        return result

    def getUncompleteBigTest(self):
        print("get uncomplete test")
        keys = ["id", "chnNum", "AIRID_id", "CH4ID_id", "CO2ID_id", "H2ID_id", "H2OID_id", "N2ID_id", "boxID_id",
                "cellID_id", "ovenID_id", "wdjID_id"]
        keystr = ",".join(keys)
        sql = 'SELECT ' + keystr + ' FROM ' + self.BigTestInfoTable + ' WHERE completeFlag=0 '
        result = self.executeGetSQL(sql, keys)
        print("uncomplete test:"+str(result))
        return result

    def getTestIDfromCell(self, cellid):
        keys = ["cellID_id", "boxID_id", "chnNum", "bigTestID_id", "testID_id"]
        keystr = ",".join(keys)
        sql = 'SELECT ' + keystr + ' FROM ' + self.cellTestRealDataTable + ' WHERE cellID_id='+str(cellid)
        result = self.executeGetSQL(sql, keys)
        return result

    def executeInsertSQL(self, datadict, table):
        while True:
            try:
                dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                       db=self.db,charset="utf8")
                break
            except Exception as e:
                print(e)
                print("cannot connect to mysql, retrying........................")
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
        sql = "insert into  " + table + " (" + COLstr + ") values (" + ss + ")"
        try:
            cursor.execute(sql, ROWstr)
            dbconnection.commit()
        except Exception as e:
            print(e)
            dbconnection.rollback()
        dbconnection.close()

    def insertHistoryData(self, datadict):
        self.executeInsertSQL(datadict, self.cellTestHistoryDataTable)

    def updateGasTable(self, gastype, datadict, MFCid):
        while True:
            try:
                dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                       db=self.db,charset="utf8")
                break
            except Exception as e:
                print(e)
                print("cannot connect to mysql, retrying........................")
        cursor = dbconnection.cursor()
        if gastype == "H2":
            table = self.H2DeviceTable
        elif gastype == "CO2":
            table = self.CO2DeviceTable
        elif gastype == "N2":
            table = self.N2DeviceTable
        elif gastype == "AIR":
            table = self.AIRDeviceTable
        elif gastype == "H2O":
            table = self.H2ODeviceTable
        elif gastype == "CH4":
            table = self.CH4DeviceTable
        else:
            print("update gas table: unknown gas type")
            return None
        ROWstr = ''
        for key in datadict:
            if isinstance(datadict[key], str) == True:
                ROWstr = ROWstr + key + '=\'' + datadict[key] + '\','
            else:
                ROWstr = ROWstr + key + '=' + str(datadict[key]) + ','
        ROWstr = ROWstr[:-1];
        sql = 'update ' + table + ' SET ' + ROWstr + ' where ID=' + str(MFCid)
        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)
            dbconnection.rollback()
        dbconnection.commit()
        dbconnection.close()

    def updateOvenTable(self, datadict, Ovenid):
        while True:
            try:
                dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                       db=self.db,charset="utf8")
                break
            except Exception as e:
                print(e)
                print("cannot connect to mysql, retrying........................")
        cursor = dbconnection.cursor()
        ROWstr = ''
        for key in datadict:
            if isinstance(datadict[key], str) == True:
                ROWstr = ROWstr + key + '=\'' + datadict[key] + '\','
            else:
                ROWstr = ROWstr + key + '=' + str(datadict[key]) + ','
        ROWstr = ROWstr[:-1];
        sql = 'update ' + self.ovenDeviceTable + ' SET ' + ROWstr + ' where ID=' + str(Ovenid)
        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)
            dbconnection.rollback()
        dbconnection.commit()
        dbconnection.close()

    def updateCellRealData(self, cellid, datadict):
        while True:
            try:
                dbconnection = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,
                                       db=self.db,charset="utf8")
                break
            except Exception as e:
                print(e)
                print("cannot connect to mysql, retrying........................")
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
        sql = 'update ' + self.cellTestRealDataTable + ' SET ' + ROWstr + 'where (cellID_id = ' + str(cellid) + ')'
        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)
            dbconnection.rollback()
        dbconnection.commit()
        dbconnection.close()
