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
			raise e
				
		configJson = json.loads(filetext)
		self.host = configJson['host']
		self.port = int(configJson['port'])
		self.user = configJson['user']
		self.passwd = configJson['passwd']
		self.db = configJson['db']
		self.cellDeviceTable = configJson['cellDeviceTable']
		self.gasDeviceTable = configJson['gasDeviceTable']
		self.boxDeviceTable = configJson['boxDeviceTable']
		self.temDeviceTable = configJson['temDeviceTable']
		self.boxHistoryDataTable = configJson['boxHistoryDataTable']
		self.gasHistoryDataTable = configJson['gasHistoryDataTable']
		self.temHistoryDataTable = configJson['temHistoryDataTable']
				
	def insertCellDeviceTable(self,datadict):		
		dbconnection = pymysql.connect(host=self.host,port=self.port,user=self.user ,passwd=self.passwd,db=self.db,charset="utf8")
		cursor= dbconnection.cursor()
		
		ROWstr=[]
		COLstr=''
		ss=''
		from  collections import Iterable
		a=isinstance(datadict, Iterable)
		for key in datadict:
			ROWstr.append(datadict[key])
			COLstr=COLstr+key+','
			ss = ss+'%s'+','
		COLstr=COLstr[:-1]
		ss=ss[:-1]
		
		sql = "insert into  "+self.cellDeviceTable+"("+COLstr+") values ("+ss+")"

		print(sql)
		try:
			cursor.execute(sql,ROWstr)
			dbconnection.commit()
		except Exception as e:
			print(e)
			dbconnection.rollback()

		dbconnection.close()
	
	def insertBoxDeviceHistoryDataTable(self,datadict):
		dbconnection = pymysql.connect(host=self.host,port=self.port,user=self.user ,passwd=self.passwd,db=self.db,charset="utf8")
		cursor= dbconnection.cursor()
		
		ROWstr=[]
		COLstr=''
		ss=''
		from  collections import Iterable
		a=isinstance(datadict, Iterable)
		for key in datadict:
			ROWstr.append(datadict[key])
			COLstr=COLstr+key+','
			ss = ss+'%s'+','
		COLstr=COLstr[:-1]
		ss=ss[:-1]
		
		sql = "insert into  "+self.boxHistoryDataTable+"("+COLstr+") values ("+ss+")"

		#print(sql)
		try:
			cursor.execute(sql,ROWstr)
			dbconnection.commit()
		except Exception as e:
			print(e)
			dbconnection.rollback()

		dbconnection.close()
		
	def updateCellDeviceTable(self,boxid, chnNum, datadict):
		dbconnection = pymysql.connect(host=self.host,port=self.port,user=self.user ,passwd=self.passwd,db=self.db,charset="utf8")
		cursor= dbconnection.cursor()	
		
		ROWstr=''
				
		#UPDATE table_name SET field1=new-value1, field2=new-value2 WHERE runoob_id=3;
		
		from  collections import Iterable
		a=isinstance(datadict, Iterable)
		for key in datadict:
			if isinstance(datadict[key],str)==True:					
				ROWstr = ROWstr + key + '=\'' + datadict[key] + '\','
			else:
				ROWstr = ROWstr + key + '=' + str(datadict[key]) + ','			
		
		ROWstr=ROWstr[:-1];
		ROWstr = ROWstr +' '
			
		sql= 'update '+self.cellDeviceTable+' SET '+ROWstr + 'where (boxID_id = ' + str(boxid) + ') and ' + '(chnNum = ' + str(chnNum)+')' 
		
		#print(sql)
		try:
			cursor.execute(sql)
		except Exception as e:
			print(e)
			dbconnection.rollback()
		dbconnection.commit()
		dbconnection.close()

	def updateCellDeviceTable_Gas_Temp(self, cellid, datadict):
		dbconnection = pymysql.connect(host=self.host,port=self.port,user=self.user ,passwd=self.passwd,db=self.db,charset="utf8")
		cursor= dbconnection.cursor()
		
		ROWstr=''
				
		#UPDATE table_name SET field1=new-value1, field2=new-value2 WHERE runoob_id=3;
		
		from  collections import Iterable
		a=isinstance(datadict, Iterable)
		for key in datadict:
			if isinstance(datadict[key],str)==True:			
				ROWstr = ROWstr + key + '=\'' + datadict[key] + '\','
			else:
				ROWstr = ROWstr + key + '=' + str(datadict[key]) + ','			
		
		ROWstr=ROWstr[:-1];
		ROWstr = ROWstr +' '
			
		sql= 'update '+self.cellDeviceTable+' SET '+ROWstr + 'where (cellID = ' + str(cellid) + ')' 
		
		#print(sql)
		try:
			cursor.execute(sql)
		except Exception as e:
			print(e)
			dbconnection.rollback()
		dbconnection.commit()
		dbconnection.close()		
		
		
	def getBoxComInfo(self):
		dbconnection = pymysql.connect(host=self.host,port=self.port,user=self.user ,passwd=self.passwd,db=self.db,charset="utf8")
		cursor= dbconnection.cursor()
		#sql = 'SELECT boxID, boxIP, boxPort, cellID_id FROM ' + self.boxDeviceTable
		sql = 'SELECT * FROM ' + self.boxDeviceTable
		#print(sql)
		try:
			cursor.execute(sql)			
			result = cursor.fetchall()
			#print (type(result))
			#print(result)
			return result
		except Exception as e:
			print(e)
			dbconnection.rollback()
		dbconnection.commit()
		dbconnection.close()
		
	def getGasComInfo(self):
		dbconnection = pymysql.connect(host=self.host,port=self.port,user=self.user ,passwd=self.passwd,db=self.db,charset="utf8")
		cursor= dbconnection.cursor()	
		#sql = 'SELECT qCoef, qIP, qPort, cellID_id, type_id FROM ' + self.gasDeviceTable
		sql = 'SELECT * FROM ' + self.gasDeviceTable
		#print(sql)
		try:
			cursor.execute(sql)	
			result = cursor.fetchall()
			#print (type(result))
			#print(result)
			return result
		except Exception as e:
			print(e)
			dbconnection.rollback()
		dbconnection.commit()
		dbconnection.close()

	def getTemComInfo(self):
		dbconnection = pymysql.connect(host=self.host,port=self.port,user=self.user ,passwd=self.passwd,db=self.db,charset="utf8")
		cursor= dbconnection.cursor()	
		#sql = 'SELECT qCoef, qIP, qPort, cellID_id, type_id FROM ' + self.temDeviceTable
		sql = 'SELECT * FROM ' + self.temDeviceTable
		#print(sql)
		try:
			cursor.execute(sql)	
			result = cursor.fetchall()
			#print (type(result))
			#print(result)
			return result
		except Exception as e:
			print(e)
			dbconnection.rollback()
		dbconnection.commit()
		dbconnection.close()

		
	def getCellInfo(self):
		dbconnection = pymysql.connect(host=self.host,port=self.port,user=self.user ,passwd=self.passwd,db=self.db,charset="utf8")
		cursor= dbconnection.cursor()
		sql = 'SELECT cellID, boxID_id, chnNum FROM ' + self.cellDeviceTable
		#print(sql)
		try:
			cursor.execute(sql)
			result = cursor.fetchall()
			#print (type(result))
			#print(result)
			return result
		except Exception as e:
			print(e)
			dbconnection.rollback()
		dbconnection.commit()
		dbconnection.close()