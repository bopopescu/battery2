#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from dbClass import dbClass
from ovenControl import Oven
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
    def setConfig(self, type=None, cellid=None, ip=None, port=None, addr=None, boxid=None, chnnum=None, cmd=None,
                  plan=None, timeout=1, waittime=0.2, length=100, senddata=None, recvdata=None, testid=None,
                  planid=None, gastype=None):
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
        self.addr = addr
        self.senddata = senddata
        self.recvdata = recvdata
        self.testid = testid
        self.planid = planid
        self.gastype = gastype


class socketConnect(object):
    def checksum(self, data):
        sum = 0
        length = data[2] + (data[3] << 8)
        for i in range(length - 2):
            sum = sum + data[4 + i]
        return sum

    def buildCmdMessage(self, config):

        if (config.type == 'box'):
            if (config.cmd == 'start'):
                # 构造命令
                totalStep = len(config.plan)
                length = totalStep * 40 + 309 + 98
                startCMD = bytearray()
                for i in range(length):
                    startCMD.append(0x0)

                # 构造报文头
                startCMD[0] = 0xAA
                startCMD[1] = 0x55
                startCMD[2] = (length - 6) & 0xFF
                startCMD[3] = ((length - 6) & 0xFF00) >> 8
                startCMD[4] = 0x92
                startCMD[5] = 0

                # 更新箱号
                startCMD[6] = config.boxid

                # 命令号
                startCMD[7] = 0x06

                # 更新通道号
                chnInt = config.chnnum // 8
                chnRes = config.chnnum % 8
                startCMD[8 + chnInt] = 0x01 << chnRes  # Q1

                # 测试方案ID号
                nowTime = datetime.now()
                startCMD[40] = nowTime.year - 2000  # year
                startCMD[41] = nowTime.month  # month
                startCMD[42] = nowTime.day  # day
                startCMD[43] = 0  # boxid
                startCMD[44] = 0  # chnnum
                startCMD[45] = 0x0F  # seq

                # 启动时间
                startCMD[46] = nowTime.year - 2000  # year
                startCMD[47] = nowTime.month  # month
                startCMD[48] = nowTime.day  # day
                startCMD[49] = nowTime.hour  # hour
                startCMD[50] = nowTime.minute  # min
                startCMD[51] = nowTime.second  # sec

                # 测试过程编程
                startCMD[304] = totalStep

                for j in range(totalStep):
                    startCMD[305 + 40 * j] = j + 1  # 当前工步号从1开始
                    if config.plan[j]['mode'] == '静置':  # 00 71 B1 18
                        startCMD[305 + 40 * j + 1] = 0x01  # 工作模式
                        startCMD[305 + 40 * j + 2] = 0  # (config.plan[j]['tTH']&0xFF000000)>>24	#主参数 4个字节
                        startCMD[305 + 40 * j + 3] = 0x71  # (config.plan[j]['tTH']&0xFF0000)>>16	#主参数 4个字节
                        startCMD[305 + 40 * j + 4] = 0xB1  # (config.plan[j]['tTH']&0xFF00)>>8		#主参数 4个字节
                        startCMD[305 + 40 * j + 5] = 0x18  # (config.plan[j]['tTH']&0xFF)			#主参数 4个字节

                        startCMD[305 + 40 * j + 6] = 0  # 副参数 4个字节
                        startCMD[305 + 40 * j + 7] = 0  # 副参数 4个字节
                        startCMD[305 + 40 * j + 8] = 0  # 副参数 4个字节
                        startCMD[305 + 40 * j + 9] = 1  # 副参数 4个字节

                        startCMD[305 + 40 * j + 10] = 0x11  # 限制条件1
                        startCMD[305 + 40 * j + 11] = (config.plan[j]['tTH'] & 0xFF000000) >> 24  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 12] = (config.plan[j]['tTH'] & 0xFF0000) >> 16  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 13] = (config.plan[j]['tTH'] & 0xFF00) >> 8  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 14] = (config.plan[j]['tTH'] & 0xFF)  # 限制条件 4个字节

                        startCMD[305 + 40 * j + 15] = 0xF1  # 限制条件2
                        startCMD[305 + 40 * j + 16] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 17] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 18] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 19] = 0  # 限制条件 4个字节

                        startCMD[305 + 40 * j + 20] = 0xF1  # 限制条件3
                        startCMD[305 + 40 * j + 21] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 22] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 23] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 24] = 0  # 限制条件 4个字节

                        startCMD[305 + 40 * j + 25] = 0xF1  # 限制条件4
                        startCMD[305 + 40 * j + 26] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 27] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 28] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 29] = 0  # 限制条件 4个字节

                        startCMD[305 + 40 * j + 30] = 0xF1  # 限制条件5
                        startCMD[305 + 40 * j + 31] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 32] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 33] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 34] = 0  # 限制条件 4个字节

                        startCMD[305 + 40 * j + 35] = 0x11  # 记录条件
                        startCMD[305 + 40 * j + 36] = 0  # 记录条件 4个字节
                        startCMD[305 + 40 * j + 37] = 0  # 记录条件 4个字节
                        startCMD[305 + 40 * j + 38] = 0xEA  # 记录条件 4个字节
                        startCMD[305 + 40 * j + 39] = 0x60  # 记录条件 4个字节

                    elif config.plan[j]['mode'] == '恒流充电':
                        startCMD[305 + 40 * j + 1] = 0x02  # 工作模式
                        startCMD[305 + 40 * j + 2] = (config.plan[j]['i'] & 0xFF000000) >> 24  # 主参数 4个字节
                        startCMD[305 + 40 * j + 3] = (config.plan[j]['i'] & 0xFF0000) >> 16  # 主参数 4个字节
                        startCMD[305 + 40 * j + 4] = (config.plan[j]['i'] & 0xFF00) >> 8  # 主参数 4个字节
                        startCMD[305 + 40 * j + 5] = (config.plan[j]['i'] & 0xFF)  # 主参数 4个字节

                        startCMD[305 + 40 * j + 6] = 0  # 副参数 4个字节
                        startCMD[305 + 40 * j + 7] = 0  # 副参数 4个字节
                        startCMD[305 + 40 * j + 8] = 0  # 副参数 4个字节
                        startCMD[305 + 40 * j + 9] = 1  # 副参数 4个字节

                        startCMD[305 + 40 * j + 10] = 0x22  # 限制条件
                        startCMD[305 + 40 * j + 11] = (config.plan[j]['uTH'] & 0xFF000000) >> 24  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 12] = (config.plan[j]['uTH'] & 0xFF0000) >> 16  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 13] = (config.plan[j]['uTH'] & 0xFF00) >> 8  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 14] = (config.plan[j]['uTH'] & 0xFF)  # 限制条件 4个字节

                        startCMD[305 + 40 * j + 15] = 0xF1  # 限制条件2
                        startCMD[305 + 40 * j + 16] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 17] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 18] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 19] = 0  # 限制条件 4个字节

                        startCMD[305 + 40 * j + 20] = 0xF1  # 限制条件3
                        startCMD[305 + 40 * j + 21] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 22] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 23] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 24] = 0  # 限制条件 4个字节

                        startCMD[305 + 40 * j + 25] = 0xF1  # 限制条件4
                        startCMD[305 + 40 * j + 26] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 27] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 28] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 29] = 0  # 限制条件 4个字节

                        startCMD[305 + 40 * j + 30] = 0xF1  # 限制条件5
                        startCMD[305 + 40 * j + 31] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 32] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 33] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 34] = 0  # 限制条件 4个字节

                        startCMD[305 + 40 * j + 35] = 0x11  # 记录条件
                        startCMD[305 + 40 * j + 36] = 0  # 记录条件 4个字节
                        startCMD[305 + 40 * j + 37] = 0  # 记录条件 4个字节
                        startCMD[305 + 40 * j + 38] = 0xEA  # 记录条件 4个字节
                        startCMD[305 + 40 * j + 39] = 0x60  # 记录条件 4个字节

                    elif config.plan[j]['mode'] == '恒流放电':
                        pass

                    elif config.plan[j]['mode'] == '恒压充电':
                        startCMD[305 + 40 * j + 1] = 0x04  # 工作模式
                        startCMD[305 + 40 * j + 2] = (config.plan[j]['u'] & 0xFF000000) >> 24  # 主参数 4个字节
                        startCMD[305 + 40 * j + 3] = (config.plan[j]['u'] & 0xFF0000) >> 16  # 主参数 4个字节
                        startCMD[305 + 40 * j + 4] = (config.plan[j]['u'] & 0xFF00) >> 8  # 主参数 4个字节
                        startCMD[305 + 40 * j + 5] = (config.plan[j]['u'] & 0xFF)  # 主参数 4个字节

                        startCMD[305 + 40 * j + 6] = 0  # 副参数 4个字节
                        startCMD[305 + 40 * j + 7] = 0  # 副参数 4个字节
                        startCMD[305 + 40 * j + 8] = 0  # 副参数 4个字节
                        startCMD[305 + 40 * j + 9] = 1  # 副参数 4个字节

                        startCMD[305 + 40 * j + 10] = 0x33  # 限制条件
                        startCMD[305 + 40 * j + 11] = (config.plan[j]['iTH'] & 0xFF000000) >> 24  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 12] = (config.plan[j]['iTH'] & 0xFF0000) >> 16  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 13] = (config.plan[j]['iTH'] & 0xFF00) >> 8  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 14] = (config.plan[j]['iTH'] & 0xFF)  # 限制条件 4个字节

                        startCMD[305 + 40 * j + 15] = 0xF1  # 限制条件2
                        startCMD[305 + 40 * j + 16] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 17] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 18] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 19] = 0  # 限制条件 4个字节

                        startCMD[305 + 40 * j + 20] = 0xF1  # 限制条件3
                        startCMD[305 + 40 * j + 21] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 22] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 23] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 24] = 0  # 限制条件 4个字节

                        startCMD[305 + 40 * j + 25] = 0xF1  # 限制条件4
                        startCMD[305 + 40 * j + 26] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 27] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 28] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 29] = 0  # 限制条件 4个字节

                        startCMD[305 + 40 * j + 30] = 0xF1  # 限制条件5
                        startCMD[305 + 40 * j + 31] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 32] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 33] = 0  # 限制条件 4个字节
                        startCMD[305 + 40 * j + 34] = 0  # 限制条件 4个字节

                        startCMD[305 + 40 * j + 35] = 0x11  # 记录条件
                        startCMD[305 + 40 * j + 36] = 0  # 记录条件 4个字节
                        startCMD[305 + 40 * j + 37] = 0  # 记录条件 4个字节
                        startCMD[305 + 40 * j + 38] = 0xEA  # 记录条件 4个字节
                        startCMD[305 + 40 * j + 39] = 0x60  # 记录条件 4个字节

                    elif config.plan[j]['mode'] == '恒压放电':
                        pass
                    elif config.plan[j]['mode'] == '恒压限流充电':
                        pass
                    elif config.plan[j]['mode'] == '恒压限流放电':
                        pass
                    elif config.plan[j]['mode'] == '恒阻放电':
                        pass
                    elif config.plan[j]['mode'] == '恒功率放电':
                        pass
                    elif config.plan[j]['mode'] == '恒功率充电':
                        pass
                    elif config.plan[j]['mode'] == '循环':
                        pass
                    elif config.plan[j]['mode'] == '跳转':
                        pass
                    elif config.plan[j]['mode'] == '电压采样':
                        pass

                # 总的记录条件
                startCMD[305 + 40 * totalStep] = 0  # 记录条件
                startCMD[305 + 40 * totalStep + 1] = 0  # 记录条件 4个字节
                startCMD[305 + 40 * totalStep + 2] = 0  # 记录条件 4个字节
                startCMD[305 + 40 * totalStep + 3] = 0  # 记录条件 4个字节

                # 更新校验和
                sum = self.checksum(startCMD)
                startCMD[-4] = sum & 0xFF
                startCMD[-3] = (sum & 0xFF00) >> 8

                # 构造报文尾
                startCMD[-1] = 0xAA
                startCMD[-2] = 0x55

                return startCMD

            elif (config.cmd == 'stop'):
                # 构造命令
                stopCMD = bytearray(
                    [0xAA, 0x55, 0x26, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x55, 0xAA])

                # 更新箱号
                stopCMD[6] = config.boxid

                # 更新通道号
                chnInt = config.chnnum // 8
                chnRes = config.chnnum % 8
                stopCMD[8 + chnInt] = 0x01 << chnRes

                # 更新校验和
                sum = self.checksum(stopCMD)
                stopCMD[-4] = sum & 0xFF
                stopCMD[-3] = (sum & 0xFF00) >> 8

                return stopCMD

            elif (config.cmd == 'resume'):
                # 构造命令
                resumeCMD = bytearray(
                    [0xAA, 0x55, 0x27, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x55, 0xAA])
                # 更新箱号
                resumeCMD[6] = config.boxid

                # 更新暂停命令
                resumeCMD[8] = 0xFF  # 0x0暂停 0xff继续

                # 更新通道号
                chnInt = config.chnnum // 8
                chnRes = config.chnnum % 8
                resumeCMD[9 + chnInt] = 0x1 << chnRes

                # 更新校验和
                sum = self.checksum(resumeCMD)
                resumeCMD[-4] = sum & 0xFF
                resumeCMD[-3] = (sum & 0xFF00) >> 8

                return resumeCMD

            elif (config.cmd == 'pause'):
                # 构造命令
                pauseCMD = bytearray(
                    [0xAA, 0x55, 0x27, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x55, 0xAA])

                # 更新箱号
                pauseCMD[6] = config.boxid

                # 更新暂停命令
                pauseCMD[8] = 0  # 暂停

                # 更新通道号
                chnInt = config.chnnum // 8
                chnRes = config.chnnum % 8
                pauseCMD[9 + chnInt] = 0x1 << chnRes

                # 更新校验和
                sum = self.checksum(pauseCMD)
                pauseCMD[-4] = sum & 0xFF
                pauseCMD[-3] = (sum & 0xFF00) >> 8

                return pauseCMD

            elif (config.cmd == 'read'):
                # 构造命令
                readBoxRealDataCMD = bytearray(
                    [0xAA, 0x55, 0x0C, 0x00, 0x00, 0x00, 0x00, 0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x09, 0x00,
                     0x55, 0xAA])
                # 更新箱号
                readBoxRealDataCMD[6] = int(config.boxid) % 10000

                # 更新校验和
                sum = self.checksum(readBoxRealDataCMD)
                readBoxRealDataCMD[-4] = sum & 0xFF
                readBoxRealDataCMD[-3] = (sum & 0xFF00) >> 8

                return readBoxRealDataCMD

            else:
                print("BulidCMD_BOX: unknown config.cmd")
                return None

        elif (config.type == 'oven'):
            o = Oven(addr=config.addr)
            if config.cmd == "start":
                cmd = o.buildcmd("r/h/s", "set", 0)
                return cmd

            elif config.cmd == "stop":
                cmd = o.buildcmd("r/h/s", "set", 12)
                return cmd

            elif config.cmd == "resume":
                cmd = o.buildcmd("r/h/s", "set", 0)
                return cmd

            elif config.cmd == "pause":
                cmd = o.buildcmd("r/h/s", "set", 4)
                return cmd

            elif config.cmd == "read":
                cmd = o.buildcmd("SV/SteP", "read")
                return cmd

            elif config.cmd == "setplan":
                i = 1
                cmd_list = []
                for step in config.plan:
                    cmd_list.append(o.buildcmd("C" + str(i), "set", int(step["T"] * 10)))
                    cmd_list.append(o.buildcmd("t" + str(i), "set", int(step["time"])))
                return cmd_list

            else:
                print("BulidCMD_OVEN: unknown config.cmd")
                return None


        elif (config.type == 'gas'):
            if config.cmd == 'set':  # 'addr'+'S'+'value'+'\r'
                cmdSetGasData = bytearray([ord(config.addr), 0x53])
                nextState = str(config.plan).encode(encoding='ascii')
                for i in nextState:
                    cmdSetGasData.append(i)
                cmdSetGasData.append(0x0D)
                return cmdSetGasData
            elif config.cmd == 'read':
                cmdReadGasRealData = bytearray([ord(config.addr), 0x0D])  # A\r
                return cmdReadGasRealData
            else:
                print("BulidCMD_GAS: unknown config.cmd")
                return None

        elif config.type == 'wdj':
            cmdReadTempRealData = bytearray([0x01, 0x03, 0x00, 0x00, 0x00, 0x08, 0x44, 0x0C])
            return cmdReadTempRealData
        else:
            print("BulidCMD: unknown config.type")
            return None

    def sendCmdMessage(self, config):
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.settimeout(config.timeout)
            s.connect((config.ip, config.port))
            try:
                print('connect: ' + config.type + ': ' + config.ip + ':' + str(config.port) + ' success')
                s.send(config.senddata)
                try:
                    time.sleep(config.waittime)
                    recvdata = s.recv(config.length)
                    return recvdata
                except:  # 接收数据失败
                    print('recv data timeout')
                    return bytearray([0xdd])
            except:  # 读取数据失败
                print('send temReadCmd error')
                return bytearray([0xee])
            s.shutdown(2)
            s.close()
        except:  # 建立连接失败
            print('connect: ' + config.type + config.ip + ':' + str(config.port) + ' failed')
            return bytearray([0xff])

    def mainProcess(self):
        config = myConfig()
        cellPlan = []
        while True:
            time.sleep(1)
            print('start listen')
            db = dbClass()
            # 1.查询数据库，提取出需要进行操作的电炉子，即现有状态不等于下一个状态，并对其下发相应的控制命令
            # 2.查询数据库，提取出需要进行操作的电池，即现有状态不等于下一个状态，并对其下发相应的控制命令
            # 3.查询数据库，提取需要进行操作的流量计，即现有状态不等于下一个状态，并对其下发相应的控制命令
            # 4.查询bigtestinfotable，提取出正在运行执行的Test对应的电池、电炉、流量计、温度计
            # 5.查询数据，更新实时数据表与历史数据表

            ovenUnderHandle = db.getOvenUnderHandle()  # 获取待处理的炉子
            cellsUnderHandle = db.getCellsUnderHandle()  # 获取待处理的电池测试组
            lljUnderHandle = db.getLljUnderHandle()  # 获取待处理的流量计
            # 炉子控制的主逻辑
            for i in ovenUnderHandle:
                # 温控器
                if i['currState'] == 'stop' and i['nextState'] == 'start':
                    # 首先设置方案
                    ovenPlan = db.getOvenTestPlan(i)
                    config.setConfig(type="oven", ip=i["IP"], port=["PortNum"], cmd="setplan", plan=ovenPlan,
                                     addr=i["Addr"])
                    senddata = self.buildCmdMessage(config)
                    for j in senddata:
                        config.senddata = j
                        config.recvdata = self.sendCmdMessage(config)
                    # 然后启动电炉
                    config.setConfig(type="oven", ip=i["IP"], port=i["PortNum"], cmd="start", plan=ovenPlan,
                                     addr=i["Addr"])
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessage(config)
                    self.updateOvenState(config, i["ID"])

                elif i['currState'] == 'start' and i['nextState'] == 'pause':
                    config.setConfig(type="oven", ip=i["IP"], port=["PortNum"], cmd="pause", addr=i["Addr"])
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessage(config)
                    self.updateOvenState(config, i["ID"])

                elif i['currState'] == 'start' and i['nextState'] == 'stop':
                    config.setConfig(type="oven", ip=i["IP"], port=["PortNum"], cmd="stop", addr=i["Addr"])
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessage(config)
                    self.updateOvenState(config, i["ID"])

                elif i['currState'] == 'pause' and i['nextState'] == 'start':
                    config.setConfig(type="oven", ip=i["IP"], port=["PortNum"], cmd="resume", addr=i["Addr"])
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessage(config)
                    self.updateOvenState(config, i["ID"])

                elif i['currState'] == 'pause' and i['nextState'] == 'stop':
                    config.setConfig(type="oven", ip=i["IP"], port=["PortNum"], cmd="stop", addr=i["Addr"])
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessage(config)
                    self.updateOvenState(config, i["ID"])

            # 流量计主逻辑
            for i in lljUnderHandle:
                config.setConfig(type="gas", ip=i["IP"], port=["PortNum"], cmd="set", addr=i['Addr'],
                                 plan=i["nextState"])
                config.senddata = self.buildCmdMessage(config)
                config.recvdata = self.sendCmdMessage(config)
                self.updateGasState(config, i["type"], i["ID"])

            # 电子负载控制的主逻辑
            for i in cellsUnderHandle:

                COM = (db.getCellsComponetCOM(i))[0]
                if (i['currState'] == "start") and (i['nextState'] == "pause"):
                    print('box:pause')
                    config.setConfig(type='box',
                                     cellid=i['cellID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     boxid=i['boxID_id'],
                                     chnnum=i['chnNum'],
                                     cmd='pause')
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessage(config)
                    self.updateCellBoxState(config)

                elif (i['nextState'] == "stop"):
                    print('box:stop')
                    config.setConfig(type='box',
                                     cellid=i['cellID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     boxid=i['boxID_id'],
                                     chnnum=i['chnNum'],
                                     cmd='stop')
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessage(config)
                    self.updateCellBoxState(config)

                elif (i['currState'] == "stop") and (i['nextState'] == "start"):
                    cellplan = db.getCellsTestPlan(i)
                    # 电子负载
                    print('box:start')
                    config.setConfig(type='box',
                                     cellid=i['cellID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     boxid=i['boxID_id'],
                                     chnnum=i['chnNum'],
                                     cmd='start',
                                     plan=cellplan,
                                     waittime=2,
                                     length=4000)
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessage(config)
                    self.updateCellBoxState(config)

                elif (i['currState'] == "pause") and (i['nextState'] == "resume"):
                    print('box:resume')
                    config.setConfig(type='box',
                                     cellid=i['cellID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     boxid=i['boxID_id'],
                                     chnnum=i['chnNum'],
                                     cmd='resume')
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessage(config)
                    self.updateCellBoxState(config)

            # 以上程序执行完之后，所有的控制命令均已处理，接下来处理读数命令
            # 首先获取正在进行的父测试，可以得知该测试所对应的设备信息，然后逐个查询
            testUnderHandle = db.getUncompleteBigTest()
            for i in testUnderHandle:
                # 依次读取各组件的信息，并更新数据表，最后插入历史数据表
                AllData = {}
                if i["boxID_id"] is not None:
                    print('box:readRealData')
                    COM = db.getCellsComponetCOM({"cellID_id": i['cellID_id']})[0]
                    config.setConfig(type='box',
                                     cellid=i['cellID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     boxid=i['boxID_id'],
                                     cmd='read',
                                     chnnum=i['chnNum'],
                                     waittime=2,
                                     length=4000)
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessage(config)
                    datadict=self.updateCellRealData(config)
                    AllData.update(datadict if datadict is not None else {})

                if i["AIRID_id"] is not None:
                    print('AIR:readRealData')
                    COM = db.getGasCOM('AIR', i)[0]
                    config.setConfig(type='gas',
                                     cellid=i['cellID_id'],
                                     chnnum=i['chnNum'],
                                     boxid=i['boxID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     addr=COM['Addr'],
                                     cmd='read',
                                     gastype="AIR"
                                     )
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessage(config)
                    datadict = self.updateCellRealData(config)
                    AllData.update(datadict if datadict is not None else {})

                if i["H2ID_id"] is not None:
                    print('H2:readRealData')
                    COM = db.getGasCOM('H2', i)[0]
                    config.setConfig(type='gas',
                                     ip=COM['IP'],
                                     cellid=i['cellID_id'],
                                     chnnum=i['chnNum'],
                                     boxid=i['boxID_id'],
                                     port=COM['PortNum'],
                                     addr=COM['Addr'],
                                     cmd='read',
                                     gastype="H2"
                                     )
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessage(config)
                    datadict = self.updateCellRealData(config)
                    AllData.update(datadict if datadict is not None else {})

                if i["N2ID_id"] is not None:
                    print('N2:readRealData')
                    COM = db.getGasCOM('N2', i)[0]
                    config.setConfig(type='gas',
                                     cellid=i['cellID_id'],
                                     chnnum=i['chnNum'],
                                     boxid=i['boxID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     addr=COM['Addr'],
                                     cmd='read',
                                     gastype="N2"
                                     )
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessage(config)
                    datadict = self.updateCellRealData(config)
                    AllData.update(datadict if datadict is not None else {})

                if i["CH4ID_id"] is not None:
                    print('CH4:readRealData')
                    COM = db.getGasCOM('CH4', i)[0]
                    config.setConfig(type='gas',
                                     cellid=i['cellID_id'],
                                     chnnum=i['chnNum'],
                                     boxid=i['boxID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     addr=COM['Addr'],
                                     cmd='read',
                                     gastype="CH4"
                                     )
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessage(config)
                    datadict = self.updateCellRealData(config)
                    AllData.update(datadict if datadict is not None else {})

                if i["CO2ID_id"] is not None:
                    print('CO2:readRealData')
                    COM = db.getGasCOM('CO2', i)[0]
                    config.setConfig(type='gas',
                                     cellid=i['cellID_id'],
                                     chnnum=i['chnNum'],
                                     boxid=i['boxID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     addr=COM['Addr'],
                                     cmd='read',
                                     gastype="CO2"
                                     )
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessage(config)
                    datadict = self.updateCellRealData(config)
                    AllData.update(datadict if datadict is not None else {})

                if i["H2OID_id"] is not None:
                    print('H2O:readRealData')
                    COM = db.getGasCOM('H2O', i)[0]
                    config.setConfig(type='gas',
                                     cellid=i['cellID_id'],
                                     chnnum=i['chnNum'],
                                     boxid=i['boxID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     addr=COM['Addr'],
                                     cmd='read',
                                     gastype="H2O"
                                     )
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessage(config)
                    datadict = self.updateCellRealData(config)
                    AllData.update(datadict if datadict is not None else {})

                if i["ovenID_id"] is not None:
                    print('oven:readRealData')
                    COM = db.getOvenCOM(i)[0]
                    config.setConfig(type='oven',
                                     cellid=i['cellID_id'],
                                     chnnum=i['chnNum'],
                                     boxid=i['boxID_id'],
                                     ip=COM['IP'],
                                     port=COM['PortNum'],
                                     addr=COM['Addr'],
                                     cmd='read'
                                     )
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessage(config)
                    datadict = self.updateCellRealData(config)
                    AllData.update(datadict if datadict is not None else {})

                if i["wdjID_id"] is not None:
                    print('wdj:readRealData')
                    COM = db.getWdjCOM(i)[0]
                    config.setConfig(type='wdj',
                                     ip=COM['IP'],
                                     cellid=i['cellID_id'],
                                     chnnum=i['chnNum'],
                                     boxid=i['boxID_id'],
                                     port=COM['PortNum'],
                                     addr=COM['Addr'],
                                     cmd='read'
                                     )
                    config.senddata = self.buildCmdMessage(config)
                    config.recvdata = self.sendCmdMessage(config)
                    datadict = self.updateCellRealData(config)
                    AllData.update(datadict if datadict is not None else {})
                testid = db.getTestIDfromCell(i["cellID_id"])[0]["testID_id"]
                AllData.update({
                    "bigTestID_id": i["id"],
                    "testID_id": testid,
                })
                self.insertHistoryData(AllData)

    def updateCellBoxState(self, config):
        db = dbClass()
        newstate = config.cmd
        cellid = config.cellid
        data = config.recvdata
        DataDict = {}

        if newstate == 'start':
            if len(data) == 46:
                if data[7] == 0x06:
                    DataDict['currState'] = 'start'
                    db.updateCellRealData(cellid, DataDict)
        elif newstate == 'pause':
            if len(data) == 46:
                if data[7] == 0x08:
                    if (data[8] == 0) and (data[9] == 0):
                        DataDict['currState'] = 'pause'
                        db.updateCellRealData(cellid, DataDict)
        elif newstate == 'resume':
            if len(data) == 46:
                if data[7] == 0x08:
                    if (data[8] == 0) and (data[9] == 0):
                        DataDict['currState'] = 'start'
                        DataDict['nextState'] = 'start'
                        db.updateCellRealData(cellid, DataDict)
        elif newstate == 'stop':
            if len(data) == 46:
                if data[7] == 0x07:
                    if (data[8] == 0) and (data[9] == 0):
                        DataDict['currState'] = 'stop'
                        db.updateCellRealData(cellid, DataDict)

    def updateGasState(self, config, gastype, MFCid):
        db = dbClass()
        data = config.recvdata
        if ((data[0] == ord(config.addr)) and data[-1] == 0x0D):  # 帧头帧尾校验
            data = data.decode()
            data = data.split()
            if (len(data) == 7 and config.cmd == 'set'):  # 数据长度校验
                DataDict = {}
                DataDict['currState'] = config.plan
                db.updateGasTable(gastype, DataDict, MFCid)
                return DataDict
        else:
            print("update gas state: wrong frame")
            return None

    def updateOvenState(self, config, Ovenid):
        db = dbClass()
        data = config.recvdata
        if len(data) == 10:  # 帧长校验
            DataDict = {}
            DataDict['currState'] = config.cmd
            db.updateOvenTable(DataDict, Ovenid)
            return DataDict
        else:
            print("update oven state: wrong frame")
            return None

    def updateCellRealData(self, config):
        db = dbClass()
        cmd = config.cmd
        data = config.recvdata
        cellid = config.cellid
        boxid = config.boxid
        chnnum = config.chnnum

        if config.type == 'box':
            if cmd == 'read':
                if ((data[0] == 0xAA) and (data[1] == 0x55) and (data[-1] == 0xAA) and (data[-2] == 0x55)):  # 帧头帧尾校验
                    if ((len(data) == data[2] + (data[3] << 8) + 6) and len(data) == 3471):  # 数据长度校验
                        if data[6] == boxid:
                            DataDict = {}
                            i = chnnum
                            DataDict['chState'] = data[11 + i * 54 + 1]
                            DataDict['chStateCode'] = (data[11 + i * 54 + 2] << 8) + data[11 + i * 54 + 3]
                            DataDict['chMasterSlaveFlag'] = data[11 + i * 54 + 4]
                            DataDict['n'] = data[11 + i * 54 + 5]
                            DataDict['k'] = (data[11 + i * 54 + 6]) + (data[11 + i * 54 + 7] << 8)
                            DataDict['mode'] = data[11 + i * 54 + 8]

                            DataDict['tc'] = (data[11 + i * 54 + 10] << 24) + (data[11 + i * 54 + 11] << 16) + (
                                    data[11 + i * 54 + 12] << 8) + (data[11 + i * 54 + 13])
                            DataDict['ta'] = (data[11 + i * 54 + 14] << 24) + (data[11 + i * 54 + 15] << 16) + (
                                    data[11 + i * 54 + 16] << 8) + (data[11 + i * 54 + 17])

                            DataDict['u'] = (data[11 + i * 54 + 19] << 24) + (data[11 + i * 54 + 20] << 16) + (
                                    data[11 + i * 54 + 21] << 8) + (data[11 + i * 54 + 22])
                            DataDict['i'] = (data[11 + i * 54 + 23] << 24) + (data[11 + i * 54 + 24] << 16) + (
                                    data[11 + i * 54 + 25] << 8) + (data[11 + i * 54 + 26])
                            DataDict['q'] = (data[11 + i * 54 + 27] << 24) + (data[11 + i * 54 + 28] << 16) + (
                                    data[11 + i * 54 + 29] << 8) + (data[11 + i * 54 + 30])
                            DataDict['qA'] = (data[11 + i * 54 + 31] << 24) + (data[11 + i * 54 + 32] << 16) + (
                                    data[11 + i * 54 + 33] << 8) + (data[11 + i * 54 + 34])
                            DataDict['T'] = (data[11 + i * 54 + 35] << 24) + (data[11 + i * 54 + 36] << 16) + (
                                    data[11 + i * 54 + 37] << 8) + (data[11 + i * 54 + 38])
                            DataDict['r'] = (data[11 + i * 54 + 39] << 24) + (data[11 + i * 54 + 40] << 16) + (
                                    data[11 + i * 54 + 41] << 8) + (data[11 + i * 54 + 42])

                            DataDict['detailDataFlag'] = (data[11 + i * 54 + 43] << 8) + data[11 + i * 54 + 44]
                            DataDict['resultDataFlag'] = (data[11 + i * 54 + 45] << 8) + data[11 + i * 54 + 46]
                            DataDict['overOutDataFlag'] = (data[11 + i * 54 + 47] << 8) + data[11 + i * 54 + 48]
                            DataDict['powerDownFlag'] = (data[11 + i * 54 + 49] << 8)

                            DataDict['celldata_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            db.updateCellRealData(cellid, DataDict)
                            return DataDict

            elif cmd == 'readDetailData':
                pass
            elif cmd == 'readResultData':
                pass
        elif config.type == "gas":
            if ((data[0] == ord(config.addr)) and data[-1] == 0x0D):  # 帧头帧尾校验
                data = data.decode()
                data = data.split()
                if (len(data) == 7):  # 数据长度校验
                    GasDataDict = {}
                    if config.gastype == 'H2':
                        GasDataDict['qH2'] = float(data[4])
                        GasDataDict['tH2'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        db.updateCellRealData(cellid, GasDataDict)
                        return GasDataDict
                    elif config.gastype == 'N2':
                        GasDataDict['qN2'] = float(data[4])
                        GasDataDict['tN2'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        db.updateCellRealData(cellid, GasDataDict)
                        return GasDataDict
                    elif config.gastype == 'CO2':
                        GasDataDict['qCO2'] = float(data[4])
                        GasDataDict['tCO2'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        db.updateCellRealData(cellid, GasDataDict)
                        return GasDataDict
                    elif config.gastype == 'CH4':
                        GasDataDict['qCH4'] = float(data[4])
                        GasDataDict['tCH4'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        db.updateCellRealData(cellid, GasDataDict)
                        return GasDataDict
                    elif config.gastype == 'AIR':
                        GasDataDict['qAIR'] = float(data[4])
                        GasDataDict['tAIR'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        db.updateCellRealData(cellid, GasDataDict)
                        return GasDataDict
                    elif config.gastype == 'H2O':
                        GasDataDict['qH2O'] = float(data[4])
                        GasDataDict['tH2O'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        db.updateCellRealData(cellid, GasDataDict)
                        return GasDataDict
            else:
                print("update_cell_data_gas: wrong frame")
                return None
        elif config.type == "oven":
            if len(data) == 10:  # 帧长校验
                PV = data[0] + (data[1] << 8)
                SV = data[2] + (data[3] << 8)
                MV = data[4] + (data[5] << 8)
                value = data[6] + (data[7] << 8)
                checksum = PV + SV + MV + value + self.addr
                checksumLO = checksum & 0xff
                checksumHI = (checksum & 0xff00) >> 8
                if data[8] == checksumLO and data[9] == checksumHI:
                    PV = PV if PV < 0x8000 else -(((~PV) & 0xffff) + 1)
                    SV = SV if SV < 0x8000 else -(((~SV) & 0xffff) + 1)
                    MV = data[4] if data[4] < 0x80 else ~data[4]
                    value = value if value < 0x8000 else -(((~value) & 0xffff) + 1)
                    ALARM = data[5]
                    HIAL = bool(ALARM & 0x01)
                    LoAL = bool(ALARM & 0x02)
                    dHAL = bool(ALARM & 0x04)
                    dLAL = bool(ALARM & 0x08)
                    orAL = bool(ALARM & 0x10)
                    AL1 = not bool(ALARM & 0x20)
                    AL2 = not bool(ALARM & 0x40)
                    OvenDataDict = {"T0": PV / 10}
                    OvenDataDict['tT0'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    db.updateCellRealData(cellid, OvenDataDict)
                    return OvenDataDict
                else:
                    print("update_cell_data_oven: wrong frame")
                    return None
            else:
                print("update_cell_data_oven: wrong frame")
                return None
        elif config.type == "wdj":
            if ((data[0] == 1) and (data[1] == 0x03) and (data[2] == 0x10)):  # 帧头帧尾校验
                if (len(data) == data[2] + 5):  # 数据长度校验
                    wdjDataDict = {}
                    wdjDataDict['T1'] = ((data[3] << 8) + data[4]) / 10
                    wdjDataDict['T2'] = ((data[5] << 8) + data[6]) / 10
                    wdjDataDict['T3'] = ((data[7] << 8) + data[8]) / 10
                    wdjDataDict['T4'] = ((data[9] << 8) + data[10]) / 10
                    wdjDataDict['tT1'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    wdjDataDict['tT2'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    wdjDataDict['tT3'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    wdjDataDict['tT4'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    db.updateCellRealData(cellid, wdjDataDict)
                    return wdjDataDict
            else:
                print("update_cell_data_wdj: wrong frame")
                return None

    def insertHistoryData(self, data):
        db = dbClass()
        db.insertHistoryData(data)


if __name__ == '__main__':
    socketRun = socketConnect()
    socketRun.mainProcess()
