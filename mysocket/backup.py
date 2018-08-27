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
import string
from datetime import datetime

class myConfig(object):
	def setConfig(self, type=None, cellid=None, ip=None, port=None, boxid=None, chnnum=None, cmd=None, plan=None, timeout=1, waittime=0.2, length=100, senddata=None, recvdata=None, testid=None, planid=None):				
		self.type = type
		self.cellid = cellid		
		self.ip = ip
		self.port = port
		self.boxid = boxid
		self.cmd = cmd
		self.chnnum = chnnum
		self.plan = plan
		self.timeout = timeout
		self.waittime = waittime
		self.length = length
		self.senddata = senddata
		self.recvdata = recvdata
		self.testid = testid
		self.planid = planid
		
class socketConnect(object):
	def checksum(self, data):
		sum = 0
		length = data[2] + (data[3]<<8)								
		for i in range(length-2):
			sum = sum + data[4+i]	
		return sum
	
	def buildCmdMessage(self,config):
		
		if (config.type =='box'):			
			if (config.cmd =='start'):
				#构造命令
				totalStep = len(config.plan)
				length = totalStep*40 + 309 + 98
				startCMD = bytearray()
				for i in range(length):
					startCMD.append(0x0)
				
				#构造报文头
				startCMD[0] = 0xAA
				startCMD[1] = 0x55
				startCMD[2] = (length-6)&0xFF
				startCMD[3] = ((length-6)&0xFF00)>>8
				startCMD[4] = 0x92
				startCMD[5] = 0
				
				#更新箱号
				startCMD[6] = config.boxid
				
				#命令号
				startCMD[7] = 0x06
				
				#更新通道号
				chnInt = config.chnnum//8
				chnRes = config.chnnum%8
				startCMD[8+chnInt] = 0x01<<chnRes   #Q1
				
				#测试方案ID号
				nowTime = datetime.now()
				startCMD[40] = nowTime.year-2000	#year
				startCMD[41] = nowTime.month 		#month
				startCMD[42] = nowTime.day			#day
				startCMD[43] = 0					#boxid
				startCMD[44] = 0					#chnnum
				startCMD[45] = 0x0F					#seq
				
				#启动时间
				startCMD[46] = nowTime.year-2000	#year
				startCMD[47] = nowTime.month 		#month
				startCMD[48] = nowTime.day			#day
				startCMD[49] = nowTime.hour			#hour
				startCMD[50] = nowTime.minute		#min
				startCMD[51] = nowTime.second  		#sec 
				
				
				#测试过程编程
				startCMD[304] = totalStep
				
				for j in range(totalStep):					
					startCMD[305+40*j] = j+1 #当前工步号从1开始
					if config.plan[j]['mode']=='静置':#00 71 B1 18
						startCMD[305+40*j+1] = 0x01						#工作模式
						startCMD[305+40*j+2] = 0	#(config.plan[j]['tTH']&0xFF000000)>>24	#主参数 4个字节
						startCMD[305+40*j+3] = 0x71	#(config.plan[j]['tTH']&0xFF0000)>>16	#主参数 4个字节			
						startCMD[305+40*j+4] = 0xB1 #(config.plan[j]['tTH']&0xFF00)>>8		#主参数 4个字节
						startCMD[305+40*j+5] = 0x18 #(config.plan[j]['tTH']&0xFF)			#主参数 4个字节
						
						startCMD[305+40*j+6] = 0			#副参数 4个字节
						startCMD[305+40*j+7] = 0			#副参数 4个字节			
						startCMD[305+40*j+8] = 0			#副参数 4个字节
						startCMD[305+40*j+9] = 1			#副参数 4个字节

						startCMD[305+40*j+10] = 0x11								#限制条件1
						startCMD[305+40*j+11] = (config.plan[j]['tTH']&0xFF000000)>>24		#限制条件 4个字节			
						startCMD[305+40*j+12] = (config.plan[j]['tTH']&0xFF0000)>>16		#限制条件 4个字节
						startCMD[305+40*j+13] = (config.plan[j]['tTH']&0xFF00)>>8			#限制条件 4个字节	
						startCMD[305+40*j+14] = (config.plan[j]['tTH']&0xFF)				#限制条件 4个字节

						startCMD[305+40*j+15] = 0xF1			#限制条件2
						startCMD[305+40*j+16] = 0				#限制条件 4个字节			
						startCMD[305+40*j+17] = 0				#限制条件 4个字节
						startCMD[305+40*j+18] = 0				#限制条件 4个字节	
						startCMD[305+40*j+19] = 0				#限制条件 4个字节
						
						startCMD[305+40*j+20] = 0xF1			#限制条件3
						startCMD[305+40*j+21] = 0				#限制条件 4个字节			
						startCMD[305+40*j+22] = 0				#限制条件 4个字节
						startCMD[305+40*j+23] = 0				#限制条件 4个字节	
						startCMD[305+40*j+24] = 0				#限制条件 4个字节
						
						startCMD[305+40*j+25] = 0xF1			#限制条件4
						startCMD[305+40*j+26] = 0				#限制条件 4个字节			
						startCMD[305+40*j+27] = 0				#限制条件 4个字节
						startCMD[305+40*j+28] = 0				#限制条件 4个字节	
						startCMD[305+40*j+29] = 0				#限制条件 4个字节
						
						
						startCMD[305+40*j+30] = 0xF1			#限制条件5
						startCMD[305+40*j+31] = 0				#限制条件 4个字节			
						startCMD[305+40*j+32] = 0				#限制条件 4个字节
						startCMD[305+40*j+33] = 0				#限制条件 4个字节	
						startCMD[305+40*j+34] = 0				#限制条件 4个字节						
						
						startCMD[305+40*j+35] = 0x11			#记录条件
						startCMD[305+40*j+36] = 0				#记录条件 4个字节			
						startCMD[305+40*j+37] = 0				#记录条件 4个字节
						startCMD[305+40*j+38] = 0xEA			#记录条件 4个字节	
						startCMD[305+40*j+39] = 0x60			#记录条件 4个字节											
												
					elif config.plan[j]['mode']=='恒流充电':
						startCMD[305+40*j+1] = 0x02								#工作模式
						startCMD[305+40*j+2] = (config.plan[j]['i']&0xFF000000)>>24	#主参数 4个字节
						startCMD[305+40*j+3] = (config.plan[j]['i']&0xFF0000)>>16		#主参数 4个字节			
						startCMD[305+40*j+4] = (config.plan[j]['i']&0xFF00)>>8			#主参数 4个字节
						startCMD[305+40*j+5] = (config.plan[j]['i']&0xFF)				#主参数 4个字节
						
						startCMD[305+40*j+6] = 0			#副参数 4个字节
						startCMD[305+40*j+7] = 0			#副参数 4个字节			
						startCMD[305+40*j+8] = 0			#副参数 4个字节
						startCMD[305+40*j+9] = 1			#副参数 4个字节
						
						startCMD[305+40*j+10] = 0x22		#限制条件
						startCMD[305+40*j+11] = (config.plan[j]['uTH']&0xFF000000)>>24		#限制条件 4个字节			
						startCMD[305+40*j+12] = (config.plan[j]['uTH']&0xFF0000)>>16		#限制条件 4个字节
						startCMD[305+40*j+13] = (config.plan[j]['uTH']&0xFF00)>>8			#限制条件 4个字节	
						startCMD[305+40*j+14] = (config.plan[j]['uTH']&0xFF)				#限制条件 4个字节

						startCMD[305+40*j+15] = 0xF1			#限制条件2
						startCMD[305+40*j+16] = 0				#限制条件 4个字节			
						startCMD[305+40*j+17] = 0				#限制条件 4个字节
						startCMD[305+40*j+18] = 0				#限制条件 4个字节	
						startCMD[305+40*j+19] = 0				#限制条件 4个字节
						
						startCMD[305+40*j+20] = 0xF1			#限制条件3
						startCMD[305+40*j+21] = 0				#限制条件 4个字节			
						startCMD[305+40*j+22] = 0				#限制条件 4个字节
						startCMD[305+40*j+23] = 0				#限制条件 4个字节	
						startCMD[305+40*j+24] = 0				#限制条件 4个字节
						
						startCMD[305+40*j+25] = 0xF1			#限制条件4
						startCMD[305+40*j+26] = 0				#限制条件 4个字节			
						startCMD[305+40*j+27] = 0				#限制条件 4个字节
						startCMD[305+40*j+28] = 0				#限制条件 4个字节	
						startCMD[305+40*j+29] = 0				#限制条件 4个字节
						
						
						startCMD[305+40*j+30] = 0xF1			#限制条件5
						startCMD[305+40*j+31] = 0				#限制条件 4个字节			
						startCMD[305+40*j+32] = 0				#限制条件 4个字节
						startCMD[305+40*j+33] = 0				#限制条件 4个字节	
						startCMD[305+40*j+34] = 0				#限制条件 4个字节						
						
						startCMD[305+40*j+35] = 0x11			#记录条件
						startCMD[305+40*j+36] = 0				#记录条件 4个字节			
						startCMD[305+40*j+37] = 0				#记录条件 4个字节
						startCMD[305+40*j+38] = 0xEA			#记录条件 4个字节	
						startCMD[305+40*j+39] = 0x60			#记录条件 4个字节
												
					elif config.plan[j]['mode']=='恒流放电':
						pass
						
					elif config.plan[j]['mode']=='恒压充电':
						startCMD[305+40*j+1] = 0x04							#工作模式
						startCMD[305+40*j+2] = (config.plan[j]['u']&0xFF000000)>>24	#主参数 4个字节
						startCMD[305+40*j+3] = (config.plan[j]['u']&0xFF0000)>>16		#主参数 4个字节			
						startCMD[305+40*j+4] = (config.plan[j]['u']&0xFF00)>>8		#主参数 4个字节
						startCMD[305+40*j+5] = (config.plan[j]['u']&0xFF)				#主参数 4个字节
						
						startCMD[305+40*j+6] = 0			#副参数 4个字节
						startCMD[305+40*j+7] = 0			#副参数 4个字节			
						startCMD[305+40*j+8] = 0			#副参数 4个字节
						startCMD[305+40*j+9] = 1			#副参数 4个字节
						
						startCMD[305+40*j+10] = 0x33		#限制条件
						startCMD[305+40*j+11] = (config.plan[j]['iTH']&0xFF000000)>>24		#限制条件 4个字节			
						startCMD[305+40*j+12] = (config.plan[j]['iTH']&0xFF0000)>>16			#限制条件 4个字节
						startCMD[305+40*j+13] = (config.plan[j]['iTH']&0xFF00)>>8				#限制条件 4个字节	
						startCMD[305+40*j+14] = (config.plan[j]['iTH']&0xFF)					#限制条件 4个字节

						startCMD[305+40*j+15] = 0xF1			#限制条件2
						startCMD[305+40*j+16] = 0				#限制条件 4个字节			
						startCMD[305+40*j+17] = 0				#限制条件 4个字节
						startCMD[305+40*j+18] = 0				#限制条件 4个字节	
						startCMD[305+40*j+19] = 0				#限制条件 4个字节
						
						startCMD[305+40*j+20] = 0xF1			#限制条件3
						startCMD[305+40*j+21] = 0				#限制条件 4个字节			
						startCMD[305+40*j+22] = 0				#限制条件 4个字节
						startCMD[305+40*j+23] = 0				#限制条件 4个字节	
						startCMD[305+40*j+24] = 0				#限制条件 4个字节
						
						startCMD[305+40*j+25] = 0xF1			#限制条件4
						startCMD[305+40*j+26] = 0				#限制条件 4个字节			
						startCMD[305+40*j+27] = 0				#限制条件 4个字节
						startCMD[305+40*j+28] = 0				#限制条件 4个字节	
						startCMD[305+40*j+29] = 0				#限制条件 4个字节
						
						
						startCMD[305+40*j+30] = 0xF1			#限制条件5
						startCMD[305+40*j+31] = 0				#限制条件 4个字节			
						startCMD[305+40*j+32] = 0				#限制条件 4个字节
						startCMD[305+40*j+33] = 0				#限制条件 4个字节	
						startCMD[305+40*j+34] = 0				#限制条件 4个字节						
						
						startCMD[305+40*j+35] = 0x11			#记录条件
						startCMD[305+40*j+36] = 0				#记录条件 4个字节			
						startCMD[305+40*j+37] = 0				#记录条件 4个字节
						startCMD[305+40*j+38] = 0xEA			#记录条件 4个字节	
						startCMD[305+40*j+39] = 0x60			#记录条件 4个字节
						
					elif config.plan[j]['mode']=='恒压放电':
						pass						
					elif config.plan[j]['mode']=='恒压限流充电':
						pass					
					elif config.plan[j]['mode']=='恒压限流放电':
						pass						
					elif config.plan[j]['mode']=='恒阻放电':
						pass
					elif config.plan[j]['mode']=='恒功率放电':
						pass
					elif config.plan[j]['mode']=='恒功率充电':
						pass
					elif config.plan[j]['mode']=='循环':
						pass						
					elif config.plan[j]['mode']=='跳转':
						pass
					elif config.plan[j]['mode']=='电压采样':
						pass
				
				#总的记录条件
				startCMD[305+40*totalStep] = 0					#记录条件
				startCMD[305+40*totalStep +1] = 0				#记录条件 4个字节			
				startCMD[305+40*totalStep +2] = 0				#记录条件 4个字节
				startCMD[305+40*totalStep +3] = 0				#记录条件 4个字节	

				#更新校验和
				sum = self.checksum(startCMD)
				startCMD[-4] = sum & 0xFF
				startCMD[-3] = (sum & 0xFF00) >> 8
				
				#构造报文尾
				startCMD[-1] = 0xAA
				startCMD[-2] = 0x55	
				
				return startCMD
				
			elif (config.cmd =='stop'):
				#构造命令
				stopCMD=bytearray([0xAA,0x55,0x26,0x00,0x00,0x00,0x00,0x07,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x07,0x00,0x55,0xAA])
				
				#更新箱号
				stopCMD[6] = config.boxid
				
				#更新通道号
				chnInt = config.chnnum//8
				chnRes = config.chnnum%8		
				stopCMD[8+chnInt] = 0x01<<chnRes
				
				#更新校验和
				sum = self.checksum(stopCMD)			
				stopCMD[-4] = sum & 0xFF
				stopCMD[-3] = (sum & 0xFF00) >> 8
				
				return stopCMD
			
			elif (config.cmd =='resume'):
				#构造命令
				resumeCMD=bytearray([0xAA,0x55,0x27,0x00,0x00,0x00,0x00,0x08,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x08,0x00,0x55,0xAA])
				#更新箱号
				resumeCMD[6] = config.boxid
				
				#更新暂停命令
				resumeCMD[8] = 0xFF #0x0暂停 0xff继续
				
				#更新通道号
				chnInt = config.chnnum//8
				chnRes = config.chnnum%8				
				resumeCMD[9+chnInt] = 0x1 << chnRes
				
				#更新校验和
				sum = self.checksum(resumeCMD)			
				resumeCMD[-4] = sum & 0xFF
				resumeCMD[-3] = (sum & 0xFF00) >> 8
				
				return resumeCMD
			
			elif (config.cmd =='pause'):
				#构造命令
				pauseCMD=bytearray([0xAA,0x55,0x27,0x00,0x00,0x00,0x00,0x08,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x08,0x00,0x55,0xAA])
				
				#更新箱号
				pauseCMD[6] = config.boxid
				
				#更新暂停命令
				pauseCMD[8] = 0 #暂停
				
				#更新通道号
				chnInt = config.chnnum//8
				chnRes = config.chnnum%8				
				pauseCMD[9+chnInt] = 0x1<<chnRes
				
				#更新校验和
				sum = self.checksum(pauseCMD)			
				pauseCMD[-4] = sum & 0xFF
				pauseCMD[-3] = (sum & 0xFF00) >> 8
				
				return pauseCMD
			
			elif (config.cmd =='readRealData'):
				#构造命令					
				readBoxRealDataCMD=bytearray([0xAA,0x55,0x0C,0x00,0x00,0x00,0x00,0x09,0x00,0x00,0x00,0x00,0x00,0x00,0x09,0x00,0x55,0xAA])
				#更新箱号
				readBoxRealDataCMD[6] = config.boxid
										
				#更新校验和
				sum = self.checksum(readBoxRealDataCMD)		
				readBoxRealDataCMD[-4] = sum & 0xFF
				readBoxRealDataCMD[-3] = (sum & 0xFF00) >> 8
				
				return readBoxRealDataCMD
				
			elif (config.cmd =='readDetailData'):
				#构造命令
				readBoxDetailDataCMD=bytearray([0xAA,0x55,0x0C,0x00,0x00,0x00,0x06,0x09,0x00,0x00,0x00,0x00,0x00,0x00,0x0F,0x00,0x55,0xAA])
				pass					
			elif (config.cmd =='readResultData'):
				#构造命令
				readBoxResultDataCMD=bytearray([0xAA,0x55,0x0C,0x00,0x00,0x00,0x06,0x09,0x00,0x00,0x00,0x00,0x00,0x00,0x0F,0x00,0x55,0xAA])
				pass
			else:
				pass
			
					
		elif config.type in ['H2','CH4','N2','CO2','AIR','H2O']:
			#print(config.cmd)
			if config.cmd == 'set':#AS+value+\r
				cmdSetGasData = bytearray([0x41,0x53])
				nextState = str(config.plan).encode(encoding='ascii')
				for i in nextState:
					cmdSetGasData.append(i)
				cmdSetGasData.append(0x0D)				
				#print(cmdSetGasData)				
				return cmdSetGasData
				
			elif config.cmd == 'read':
				cmdReadGasRealData = bytearray([0x41,0x0D]) #A\r				
				return cmdReadGasRealData

		elif config.type in ['T0','T1','T2','T3','T4']:
			cmdReadTempRealData = bytearray([0x01,0x03,0x00,0x00,0x00,0x08,0x44,0x0C])
			return cmdReadTempRealData		
					
	def sendCmdMessage(self, config):		
		signal.signal(signal.SIGINT, quit)
		signal.signal(signal.SIGTERM, quit)
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
			s.settimeout(config.timeout)
			s.connect((config.ip,config.port))	
			try:
				print('connect: ' + config.type + ': ' + config.ip + ':' + str(config.port) +' success')
				s.send(config.senddata)								
				try:
					time.sleep(config.waittime)			
					recvdata = s.recv(config.length)
					return recvdata
				except:#接收数据失败
					print('recv data timeout')
					return bytearray([0xdd])
			except: #读取数据失败
				print('send temReadCmd error')
				return bytearray([0xee])
			s.shutdown(2)
			s.close()
		except: #建立连接失败
			print('connect: ' + config.type + config.ip + ':' + str(config.port) +' failed')
			return bytearray([0xff])
	

	def mainProcess(self):
		config = myConfig()
		cellPlan = []
		while True:
			time.sleep(1)
			print('start listen')
			db = dbClass()
			cellsUnderHandle = db.getCellsUnderHandle() #获取待处理的电池测试组
			cellsComponetCOM = db.getCellsComponetCOM() #获取待处理电池组各组件的通信参数
			cellsTestPlan = db.getCellsTestPlan()		#获取待处理电池组各组件的测试方案

			ovenUnderHandle = db.getOvenUnderHandle() #获取待处理的炉子
			ovenPlan = db.getOvenTestPlan() #获取待处理电各炉子的测试方案
			
			lljUnderHandle = db.getLljUnderHandle() #获取待处理的流量计
			
			#炉子的主逻辑
			for iOven in range (len(ovenUnderHandle)):
				#温控器					
				if (ovenUnderHandle[i]['currOvenState']=='stop') and (ovenUnderHandle[i]['nextOvenState']=='start'):
					#构建炉子的报文
					#发送炉子报文
					#更新实时状态表ovendevicetable
					#插入历史数据表commonhistory
					pass
				elif (ovenUnderHandle[i]['currOvenState']=='start') and (ovenUnderHandle[i]['nextOvenState']=='pause'):
					#构建炉子的报文
					#发送炉子报文
					#更新实时状态表ovendevicetable
					pass
				elif (ovenUnderHandle[i]['currOvenState']=='start') and (ovenUnderHandle[i]['nextOvenState']=='start'):																					
					#读炉子的温度
					#存数据commonhistory
					#读流量计数据
					#存数据commonhistory
					pass
							
			#电子负载的主逻辑
			for i in range(len(cellsUnderHandle)):
				for j in range(len(cellsComponetCOM)):
					if cellsUnderHandle[i]['cellID_id']==cellsComponetCOM[j]['cellID']:						
						
						#H2流量控制器
						if cellsUnderHandle[i]['H2curr'] != cellsUnderHandle[i]['H2next']:
							#H2
							print('H2:set')										
							config.setConfig(	type = 'H2',
												cellid = cellsUnderHandle[i]['cellID_id'],
												ip = cellsComponetCOM[j]['mH2IP'], 
												port = cellsComponetCOM[j]['mH2Port'], 
												cmd = 'set',
												plan = cellsUnderHandle[i]['H2next'])
							config.senddata = self.buildCmdMessage(config)							
							#print("send:"+config.senddata.hex())
							config.recvdata = self.sendCmdMessage(config)							
							#print("recv:"+config.recvdata.hex())														
							self.updateCellGasState(config)
						else:
							pass
							#if cellsUnderHandle[i]['H2curr'] 
						
						'''	
						#N2流量控制器
						if cellsUnderHandle[i]['N2curr'] != cellsUnderHandle[i]['N2next']:							
							pass				
							
						#CH4流量控制器
						if cellsUnderHandle[i]['CH4curr'] != cellsUnderHandle[i]['CH4next']:
							pass

						#H2O流量控制器
						if cellsUnderHandle[i]['H2Ocurr'] != cellsUnderHandle[i]['H2Onext']:
							pass
							
						#CO2流量控制器
						if cellsUnderHandle[i]['CO2curr'] != cellsUnderHandle[i]['CO2next']:
							pass

						#AIR流量控制器
						if cellsUnderHandle[i]['AIRcurr'] != cellsUnderHandle[i]['AIRnext']:
							pass
						'''
						
						#流量计和温度计读数
						boxState = (cellsUnderHandle[i]['currState']=="start") and (cellsUnderHandle[i]['nextState']=="start")
						ovenState = (cellsUnderHandle[i]['currOvenState']=="start") and (cellsUnderHandle[i]['nextOvenState']=="start")
						
						if boxState or ovenState:
							#T1
							print('T1:readRealData')							
							config.setConfig(	type = 'T1',
												cellid = cellsUnderHandle[i]['cellID_id'],
												ip = cellsComponetCOM[j]['mT1IP'], 
												port = cellsComponetCOM[j]['mT1Port'],
												testid = cellsUnderHandle[i]['testID_id'],
												planid = cellsUnderHandle[i]['planID_id']
												)
							config.senddata = self.buildCmdMessage(config)							
							#print("send:"+config.senddata.hex())
							config.recvdata = self.sendCmdMessage(config)							
							#print("recv:"+config.recvdata.hex())							
							self.updateCellRealData(config)
							self.insertCommonHistoryData(config)
							
							#H2
							print('H2:readRealData')
							config.setConfig(	type = 'H2',
												cellid = cellsUnderHandle[i]['cellID_id'],
												ip = cellsComponetCOM[j]['mH2IP'], 
												port = cellsComponetCOM[j]['mH2Port'],												
												cmd = 'read',
												testid = cellsUnderHandle[i]['testID_id'],
												planid = cellsUnderHandle[i]['planID_id']
												)
							config.senddata = self.buildCmdMessage(config)							
							#print("send:"+config.senddata.hex())
							config.recvdata = self.sendCmdMessage(config)							
							#print("recv:"+config.recvdata.hex())							
							self.updateCellRealData(config)
							self.insertCommonHistoryData(config)
							
					
						
						
						#电子负载											
						if (cellsUnderHandle[i]['currState']=="start") and (cellsUnderHandle[i]['nextState']=="start"):
							#电子负载
							print('box:readRealData')
							
							config.setConfig(	type = 'box',
												cellid = cellsUnderHandle[i]['cellID_id'],
												ip = cellsComponetCOM[j]['eIP'], 
												port = cellsComponetCOM[j]['ePort'], 
												boxid = cellsUnderHandle[i]['boxID'],
												cmd = 'readRealData',
												chnnum = cellsUnderHandle[i]['chnNum'],																								
												waittime = 2,
												length = 4000)
							config.senddata = self.buildCmdMessage(config)							
							#print("send:"+config.senddata.hex())
							config.recvdata = self.sendCmdMessage(config)							
							#print("recv:"+config.recvdata.hex())							
							self.updateCellRealData(config)
																					
							
							
							
							#self.insertCellALLRealData(cellsUnderHandle[i]['testID_id'], boxDBData, tempDBData)
							
						elif (cellsUnderHandle[i]['currState']=="start") and (cellsUnderHandle[i]['nextState']=="pause"):
							#电子负载
							print('box:pause')
							config.setConfig(	type = 'box',
												cellid = cellsUnderHandle[i]['cellID_id'],
												ip = cellsComponetCOM[j]['eIP'], 
												port = cellsComponetCOM[j]['ePort'], 
												boxid = cellsUnderHandle[i]['boxID'],
												chnnum = cellsUnderHandle[i]['chnNum'],
												cmd = 'pause')
							config.senddata = self.buildCmdMessage(config)							
							#print("send:"+config.senddata.hex())
							config.recvdata = self.sendCmdMessage(config)							
							#print("recv:"+config.recvdata.hex())
							self.updateCellBoxState(config)	
							
						elif (cellsUnderHandle[i]['currState']=="start") and (cellsUnderHandle[i]['nextState']=="stop"):
							#电子负载
							print('box:stop')
							config.setConfig(	type = 'box',
												cellid = cellsUnderHandle[i]['cellID_id'],
												ip = cellsComponetCOM[j]['eIP'], 
												port = cellsComponetCOM[j]['ePort'], 
												boxid = cellsUnderHandle[i]['boxID'],
												chnnum = cellsUnderHandle[i]['chnNum'],
												cmd = 'stop')
							config.senddata = self.buildCmdMessage(config)							
							#print("send:"+config.senddata.hex())
							config.recvdata = self.sendCmdMessage(config)							
							#print("recv:"+config.recvdata.hex())
							self.updateCellBoxState(config)													
														
						elif (cellsUnderHandle[i]['currState']=="stop") and (cellsUnderHandle[i]['nextState']=="start"):							
							#查找测试方案
							for k in range(len(cellsTestPlan)):
								if cellsUnderHandle[i]['planID_id']==cellsTestPlan[k]['planID_id']:
									cellPlan.append(cellsTestPlan[k])
							
							#电子负载
							print('box:start')
							config.setConfig(	type = 'box',
												cellid = cellsUnderHandle[i]['cellID_id'],
												ip = cellsComponetCOM[j]['eIP'], 
												port = cellsComponetCOM[j]['ePort'], 
												boxid = cellsUnderHandle[i]['boxID'],
												chnnum = cellsUnderHandle[i]['chnNum'],
												cmd = 'start',
												plan = cellPlan,
												waittime = 2,
												length =4000)						
							config.senddata = self.buildCmdMessage(config)							
							#print("send:"+config.senddata.hex())
							config.recvdata = self.sendCmdMessage(config)							
							#print("recv:"+config.recvdata.hex())
							self.updateCellBoxState(config)	
																												
						elif (cellsUnderHandle[i]['currState']=="pause") and (cellsUnderHandle[i]['nextState']=="resume"):
							#电子负载
							print('box:resume')
							config.setConfig(	type = 'box',
												cellid = cellsUnderHandle[i]['cellID_id'],
												ip = cellsComponetCOM[j]['eIP'], 
												port = cellsComponetCOM[j]['ePort'], 
												boxid = cellsUnderHandle[i]['boxID'],
												chnnum = cellsUnderHandle[i]['chnNum'],
												cmd = 'resume')
							config.senddata = self.buildCmdMessage(config)							
							#print("send:"+config.senddata.hex())
							config.recvdata = self.sendCmdMessage(config)							
							#print("recv:"+config.recvdata.hex())
							self.updateCellBoxState(config)	
							
						elif (cellsUnderHandle[i]['currState']=="resume") and (cellsUnderHandle[i]['nextState']=="stop"):
							#电子负载
							print('box:stop')
							config.setConfig(	type = 'box',
												cellid = cellsUnderHandle[i]['cellID_id'],
												ip = cellsComponetCOM[j]['eIP'], 
												port = cellsComponetCOM[j]['ePort'], 
												boxid = cellsUnderHandle[i]['boxID'],
												chnnum = cellsUnderHandle[i]['chnNum'],
												cmd = 'stop')
							config.senddata = self.buildCmdMessage(config)							
							#print("send:"+config.senddata.hex())
							config.recvdata = self.sendCmdMessage(config)							
							#print("recv:"+config.recvdata.hex())
							self.updateCellBoxState(config)	
	
	def updateCellBoxState(self, config):	
		db = dbClass()
		newstate = config.cmd
		cellid = config.cellid
		data = config.recvdata
		DataDict={}
		
		if newstate=='start':
			if len(data)==46:
				if data[7]==0x06:
					DataDict['currState'] = 'start'
					db.updateCellRealData(cellid,DataDict)
		elif newstate=='pause':
			if len(data)==46:
				if data[7]==0x08:
					if (data[8]==0) and (data[9]==0):
						DataDict['currState'] = 'pause'
						db.updateCellRealData(cellid,DataDict)
		elif newstate=='resume':
			if len(data)==46:
				if data[7]==0x08:
					if (data[8]==0) and (data[9]==0):
						DataDict['currState'] = 'start'
						DataDict['nextState'] = 'start'
						db.updateCellRealData(cellid,DataDict)
		elif newstate=='stop':					
			if len(data)==46:
				if data[7]==0x07:
					if (data[8]==0) and (data[9]==0):
						DataDict['currState'] = 'stop'
						db.updateCellRealData(cellid,DataDict)

						
	def updateCellGasState(self, config):	
		db = dbClass()
		newstate = config.cmd
		cellid = config.cellid
		data = config.recvdata
		
		if ((data[0]==0x41) and data[-1]==0x0D):			#帧头帧尾校验			
			data=data.decode()
			data=data.split()
			if (len(data) == 7 and config.cmd =='set'):	 	#数据长度校验
				if config.type == 'H2':
					DataDict = {}
					DataDict['H2curr'] = config.plan																																					
					db.updateCellRealData(cellid, DataDict)
					return DataDict
				elif config.type == 'N2':
					pass
		else:
			pass
				
	def updateCellRealData(self,config):
		db = dbClass()
		cmd = config.cmd
		data = config.recvdata
		cellid = config.cellid
		boxid = config.boxid
		chnnum = config.chnnum
		
		if config.type == 'box':			
			if cmd == 'readRealData':
				if ((data[0]==0xAA) and (data[1]==0x55) and (data[-1]==0xAA) and (data[-2]==0x55)):   #帧头帧尾校验			
					if ((len(data) == data[2]+(data[3]<<8)+6) and len(data)==3471):					  #数据长度校验
						if data[6]==boxid:
							DataDict = {}
							i = chnnum				
							DataDict['chState']= data[11+i*54+1]
							DataDict['chStateCode']= (data[11+i*54+2]<<8) + data[11+i*54+3]
							DataDict['chMasterSlaveFlag']= data[11+i*54+4]
							DataDict['n'] = data[11+i*54+5]
							DataDict['k'] = (data[11+i*54+6]) +  (data[11+i*54+7]<<8)						
							DataDict['mode']= data[11+i*54+8]
							
							DataDict['tc']=(data[11+i*54+10]<<24) + (data[11+i*54+11]<<16) + (data[11+i*54+12]<<8) + (data[11+i*54+13])
							DataDict['ta']=(data[11+i*54+14]<<24) + (data[11+i*54+15]<<16) + (data[11+i*54+16]<<8) + (data[11+i*54+17])
							
							DataDict['u']= (data[11+i*54+19]<<24) + (data[11+i*54+20]<<16) + (data[11+i*54+21]<<8) + (data[11+i*54+22])
							DataDict['i']= (data[11+i*54+23]<<24) + (data[11+i*54+24]<<16) + (data[11+i*54+25]<<8) + (data[11+i*54+26])
							DataDict['q']= (data[11+i*54+27]<<24) + (data[11+i*54+28]<<16) + (data[11+i*54+29]<<8) + (data[11+i*54+30])
							DataDict['qA']=(data[11+i*54+31]<<24) + (data[11+i*54+32]<<16) + (data[11+i*54+33]<<8) + (data[11+i*54+34])
							DataDict['T']= (data[11+i*54+35]<<24) + (data[11+i*54+36]<<16) + (data[11+i*54+37]<<8) + (data[11+i*54+38])
							DataDict['r']= (data[11+i*54+39]<<24) + (data[11+i*54+40]<<16) + (data[11+i*54+41]<<8) + (data[11+i*54+42])	
							
							DataDict['detailDataFlag']= (data[11+i*54+43]<<8) + data[11+i*54+44]
							DataDict['resultDataFlag']= (data[11+i*54+45]<<8) + data[11+i*54+46]
							DataDict['overOutDataFlag']= (data[11+i*54+47]<<8) + data[11+i*54+48]
							DataDict['powerDownFlag']= (data[11+i*54+49]<<8) 
																					
							DataDict['celldata_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")														
							db.updateCellRealData(cellid, DataDict)
							return DataDict
							
			elif cmd == 'readDetailData':
				pass
			elif cmd == 'readResultData':
				pass
				
		elif config.type in ['H2','CH4','N2','CO2','AIR','H2O']:
			if ((data[0]==0x41) and data[-1]==0x0D):			#帧头帧尾校验			
				data=data.decode()
				data=data.split()
				if (len(data) == 7):				  				 	#数据长度校验
					if config.type == 'H2':
						DataDict = {}
						DataDict['qH2'] = float(data[4])
						DataDict['tH2']= datetime.now().strftime("%Y-%m-%d %H:%M:%S")																																		
						db.updateCellRealData(cellid, DataDict)
						return DataDict
					elif config.type == 'N2':
						pass
			else:
				pass		
		elif config.type in ['T0','T1','T2','T3','T4']:
			if config.type == 'T0':
				pass
			else:
				if ((data[0]==1) and (data[1]==0x03) and (data[2]==0x10)):			#帧头帧尾校验			
					if (len(data) == data[2]+5):				  				 	#数据长度校验				
						DataDict = {}
						DataDict['T1'] = ((data[3]<<8) + data[4])/10
						DataDict['T2'] = ((data[5]<<8) + data[6])/10
						DataDict['T3'] = ((data[7]<<8) + data[8])/10
						DataDict['T4'] = ((data[9]<<8) + data[10])/10
						DataDict['tT1']= datetime.now().strftime("%Y-%m-%d %H:%M:%S")																		
						DataDict['tT2']= datetime.now().strftime("%Y-%m-%d %H:%M:%S")																		
						DataDict['tT3']= datetime.now().strftime("%Y-%m-%d %H:%M:%S")																		
						DataDict['tT4']= datetime.now().strftime("%Y-%m-%d %H:%M:%S")																		
						db.updateCellRealData(cellid, DataDict)
						return DataDict			
				else:
					pass
	
	def insertCommonHistoryData(self, config):
		db = dbClass()
		DataDict = {}
		
	
	def insertCellALLRealData(self, testid, boxdata, tempdata):
		db = dbClass()
		DataDict = {}
		if boxdata:
			for key1 in boxdata:
				DataDict[key1] = boxdata[key1]
				
		if tempdata:
			for key2 in tempdata:
				DataDict[key2] = tempdata[key2]
		
		DataDict['testID_id'] = testid
		
		DataDict['boxID'] = 0
		DataDict['chnNum'] = 0
		DataDict['totalStepN'] = 2
		DataDict['s0'] = 0
		DataDict['currState'] = 'start'
		DataDict['nextState'] = 'start'
		
		DataDict['sH2'] = 0
		DataDict['qH2'] = 0
		DataDict['tH2'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		
		DataDict['sCH4'] = 0
		DataDict['qCH4'] = 0
		DataDict['tCH4'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		
		DataDict['sN2'] = 0
		DataDict['qN2'] = 0
		DataDict['tN2'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		
		DataDict['sCO2'] = 0
		DataDict['qCO2'] = 0
		DataDict['tCO2'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		
		DataDict['sCH4'] = 0
		DataDict['qCH4'] = 0
		DataDict['tCH4'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		
		DataDict['sAIR'] = 0
		DataDict['qAIR'] = 0
		DataDict['tAIR'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		
		DataDict['sH2O'] = 0
		DataDict['qH2O'] = 0
		DataDict['tH2O'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		
		DataDict['sRES'] = 0
		DataDict['qRES'] = 0
		DataDict['tRES'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		
		DataDict['sT1'] = 0
		DataDict['sT2'] = 0
		DataDict['sT3'] = 0
		DataDict['sT4'] = 0		
		
		db.insertCellALLRealData(DataDict)
		
if __name__ == '__main__':
	socketRun = socketConnect()
	socketRun.mainProcess()