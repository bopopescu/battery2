# -*- coding: utf-8 -*-
from dbClass import dbClass
import threading
import socket
import signal
import base64
import time
import json
import binascii
from datetime import datetime

class socketListen(object):
	"""docstring for socketListen"""
	def __init__(self, port):
		self.port = port

	def listen(self):
		signal.signal(signal.SIGINT, quit)
		signal.signal(signal.SIGTERM, quit)
		# 创建一个socket
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

		s.bind(('0.0.0.0', self.port))
		s.listen(5)
		print('Waiting for connection...')

		while True:
			# 接受一个新连接:
			sock, addr = s.accept()
			print(addr,type(addr))
			# 创建新线程来处理TCP连接:
			t = threading.Thread(target=self.tcplink, args=(sock, addr))
			t.start()


	def tcplink(self,sock,addr):
		print('Accept new connection from %s:%s...' % addr)
		senddata='1234567890';
		sock.send(senddata.encode(encoding="utf-8"))
		while True:
			data = sock.recv(4000)
			
			if not data:
				break

			#print(data)

			#todo
			#报文校验长度等

			try:
				#jsondata = eval(data)
				t = threading.Thread(target=self.analysisJsonData, args=(data,addr,))
				t.start()
			except Exception as e:
				print(e)

		sock.close()
		print('Connection from %s:%s closed.' % addr)
		
	def analysisJsonData(self,data,addr):
		#print(data)	
		#print(type(data))
		if ((data[0]==0xAA) and (data[1]==0x55) and (data[-1]==0xAA) and (data[-2]==0x55)):   #帧头帧尾校验			
			if ((len(data) == data[2]+(data[3]<<8)+6) and len(data)==3471):					  #数据长度校验
				dataClass = dbClass()
				for i in range(64):					
					DataDict = {}
					cellID = i
					print(i)
					DataDict['cellID']= i
					DataDict['boxNum']= 0					
					DataDict['chnNum']= data[11+i*54]+1		
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
					
					DataDict['qH2']=0
					DataDict['qN2']=0
					DataDict['qCH4']=0
					DataDict['qAIR']=0
					DataDict['qH2O']=0
					DataDict['T1']=0
					DataDict['T2']=0
					DataDict['T3']=0
					DataDict['gasdata_time']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")					
					DataDict['celldata_time']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					#dataClass.insertCellDeviceTable(DataDict)
					dataClass.updateCellDeviceTable(cellID,DataDict);					