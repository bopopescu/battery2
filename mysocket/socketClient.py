#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from dbClass import dbClass
import threading
import socket
import signal
import base64
import time
import json
import binascii
from datetime import datetime

class socketConnect(object):
	"""docstring for socketListen"""
	def __init__(self, ip, port):
		self.port = port
		self.ip = ip

	def connect(self):					   
		cmdReadBoxRealData = bytearray([0xAA,0x55,0x0C,0x00,0x00,0x00,0x06,0x09,0x00,0x00,0x00,0x00,0x00,0x00,0x0F,0x00,0x55,0xAA])
		cmdReadGasRealData = bytearray([0x01,0x02])
		cmdReadTemRealData = bytearray([0x01,0x03,0x00,0x00,0x00,0x08,0x44,0x0C])
		timeout = 4
		timesleep = 0.5
		
		while True:
			db = dbClass()
			boxComInfo = db.getBoxComInfo()
			gasComInfo = db.getGasComInfo()
			temComInfo = db.getTemComInfo()
			cellInfo = db.getCellInfo()
			
			for ibox in range(len(boxComInfo)):
				boxID = boxComInfo[ibox][0]
				boxIP = boxComInfo[ibox][1]
				boxPort = boxComInfo[ibox][2]

				signal.signal(signal.SIGINT, quit)
				signal.signal(signal.SIGTERM, quit)
				
				try:
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
					s.connect((boxIP,boxPort))
					print('connect box: ' + str(boxID) + ': ' + boxIP + ':' + str(boxPort) +' success')
					#更新校验和	
					checksum = cmdReadBoxRealData[14] + (cmdReadBoxRealData[15]<<8) + boxID - cmdReadBoxRealData[6]
					cmdReadBoxRealData[6] = boxID
					cmdReadBoxRealData[14] = checksum & 0xFF
					cmdReadBoxRealData[15] = (checksum &0xFF00) >> 8
										
					#print (cmdReadBoxRealData)
					
					#发送抄读命令
					s.send(cmdReadBoxRealData) #读取实时数据
					s.settimeout(timeout)
													
					try:
						time.sleep(1)				
						boxData = s.recv(4000)					
						self.updateCellBoxData(boxData, boxID)				
					except:
						print('recv boxData timeout')																				
					s.shutdown(2)	
					s.close()			
				except:
					print('connect box: ' + boxIP + ':' + str(boxPort) +' failed')		
				
				time.sleep(timesleep)
			
			for igas in range(len(gasComInfo)):
				gasID = gasComInfo[igas][0]
				gasCoef = gasComInfo[igas][1]
				gasIP = gasComInfo[igas][2]
				gasPort = gasComInfo[igas][3]
				cellID = gasComInfo[igas][4]
				gasType = gasComInfo[igas][5]		

				signal.signal(signal.SIGINT, quit)
				signal.signal(signal.SIGTERM, quit)
				
				try:
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
					s.connect((gasIP,gasPort))
					print('connect gas: ' + gasIP + ':' + str(gasPort) +' success')
					#更新ID

					#发送抄读命令
					s.send(cmdReadGasRealData) #读取实时数据
					s.settimeout(timeout)
													
					#try:				
					gasData = s.recv(1000)	
					#print(gasData.hex())
					self.updateCellGasData(gasData, cellID, gasType, gasCoef)			
					#except:
					#	print('recv gasData timeout')																				
					s.shutdown(2)		
					s.close()		
				except:
					print('connect gas: ' + gasIP + ':' + str(gasPort) +' failed')		
				
				time.sleep(timesleep)											
			
			for item in range(len(temComInfo)):
				temID = temComInfo[item][0]
				temCoef = temComInfo[item][1]
				temIP = temComInfo[item][2]
				temPort = temComInfo[item][3]
				cellID = temComInfo[item][4]
				temType = temComInfo[item][5]				

				signal.signal(signal.SIGINT, quit)
				signal.signal(signal.SIGTERM, quit)
				
				try:
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
					s.connect((temIP,temPort))
					print('connect tem: ' + temIP + ':' + str(temPort) +' success')
					#更新ID

					#发送抄读命令
					try:
						s.send(cmdReadTemRealData) #读取实时数据
						s.settimeout(timeout)
														
						try:
							#time.sleep(0.2)				
							temData = s.recv(1000)		
							self.updateCellTemData(temData, temID, cellID)
						except:
							print('recv temData timeout')
					except:
						print('send temReadCmd error')
					s.shutdown(2)		
					s.close()			
				except:
					print('connect tem: ' + temIP + ':' + str(temPort) +' failed')		
				
				time.sleep(timesleep)			
			
	def updateCellBoxData(self,data,id):
		#print(data.hex())	
		#print(type(data))
		if ((data[0]==0xAA) and (data[1]==0x55) and (data[-1]==0xAA) and (data[-2]==0x55)):   #帧头帧尾校验			
			if ((len(data) == data[2]+(data[3]<<8)+6) and len(data)==3471):					  #数据长度校验
				db = dbClass()
				HistoryData={}
				HistoryData['value'] = data.hex()
				HistoryData['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				HistoryData['boxID_id'] = id
				HistoryData['type_id'] = 1
				db.insertBoxDeviceHistoryDataTable(HistoryData)
				
				for i in range(64):					
					DataDict = {}
					
					#cellID = i
					#DataDict['cellID']= i
					#DataDict['boxID_id'] = id					
					#DataDict['chnNum']= data[11+i*54]+1
					
					chnNum= data[11+i*54]				
					DataDict['state']= data[11+i*54+1]
					DataDict['mode']= data[11+i*54+8]
					DataDict['tc']=(data[11+i*54+10]<<24) + (data[11+i*54+11]<<16) + (data[11+i*54+12]<<8) + (data[11+i*54+13])
					DataDict['ta']=(data[11+i*54+14]<<24) + (data[11+i*54+15]<<16) + (data[11+i*54+16]<<8) + (data[11+i*54+17])
					DataDict['n']= (data[11+i*54+5])
					DataDict['k']= (data[11+i*54+6]) +  (data[11+i*54+7]<<8)
					DataDict['u']= (data[11+i*54+19]<<24) + (data[11+i*54+20]<<16) + (data[11+i*54+21]<<8) + (data[11+i*54+22])
					DataDict['i']= (data[11+i*54+23]<<24) + (data[11+i*54+24]<<16) + (data[11+i*54+25]<<8) + (data[11+i*54+26])
					DataDict['q']= (data[11+i*54+27]<<24) + (data[11+i*54+28]<<16) + (data[11+i*54+29]<<8) + (data[11+i*54+30])
					DataDict['qA']=(data[11+i*54+31]<<24) + (data[11+i*54+32]<<16) + (data[11+i*54+33]<<8) + (data[11+i*54+34])
					DataDict['T']= (data[11+i*54+35]<<24) + (data[11+i*54+36]<<16) + (data[11+i*54+37]<<8) + (data[11+i*54+38])
					DataDict['r']= (data[11+i*54+39]<<24) + (data[11+i*54+40]<<16) + (data[11+i*54+41]<<8) + (data[11+i*54+42])										
					'''
					DataDict['qH2']=0
					DataDict['qN2']=0
					DataDict['qCH4']=0
					DataDict['qAIR']=0
					DataDict['qH2O']=0
					DataDict['T1']=0
					DataDict['T2']=0
					DataDict['T3']=0
					DataDict['gasdata_time']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")	
					'''					
					DataDict['celldata_time']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")														
					db.updateCellDeviceTable(id, chnNum, DataDict)
														
	
	def updateCellGasData(self,data,id,type,coef):		
		#print(data.hex())
		#print(type)
		DataDict={}
		if type == 'H2':
			DataDict['qH2']=0			
		elif type == 'N2':
			DataDict['qN2']=0
		elif type == 'CH4':
			DataDict['qCH4']=0
		elif type == 'H2O':
			DataDict['qH2O']=0
		elif type == 'AIR':
			DataDict['qAIR']=0
					
		DataDict['gasdata_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					
		db = dbClass()
		
		db.updateCellDeviceTable_Gas_Temp(id, DataDict);

	def updateCellTemData(self,data,temid,cellid):
		#print(data.hex())	
		#print(type(data))
		if ((data[0]==temid) and (data[1]==0x03) and (data[2]==0x10)):		#帧头帧尾校验			
			if (len(data) == data[2]+5):				  				 	#数据长度校验
				db = dbClass()
				DataDict = {}
				DataDict['T1'] = ((data[3]<<8) + data[4])/10
				DataDict['T2'] = ((data[5]<<8) + data[6])/10
				DataDict['T3'] = ((data[7]<<8) + data[8])/10			
				DataDict['T4'] = ((data[9]<<8) + data[10])/10			
				DataDict['temdata_time']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")																		
				db.updateCellDeviceTable_Gas_Temp(cellid, DataDict)															
		
if __name__ == '__main__':
	socketRun = socketConnect("localhost", 3092)
	socketRun.connect()