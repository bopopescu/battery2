import time


class Oven(object):
    addr = 0x01
    valDict = {"SV/SteP": 0x00, "HIAL": 0x01, "LoAL": 0x02, "dHAL": 0x03, "dLAL": 0x04, "dF": 0x05, "CtrL": 0x06,
               "M5": 0x07, "P": 0x08, "t": 0x09, "CtI": 0x0A, "Sn": 0x0B, "dIP": 0x0C, "dIL": 0x0D, "dIH": 0x0E,
               "ALP": 0x0F, "Sc": 0x10, "oPt": 0x11, "oPL": 0x12, "oPH": 0x13, "CF": 0x14, "r/h/s": 0x15, "Addr": 0x16,
               "dL": 0x17, "run": 0x18, "Loc": 0x19, "runtime": 0x56}

    def __init__(self,addr=0x01):
        self.addr=addr
        for i in range(0, 30):
            self.valDict["C" + str(i + 1)] = 0x1A + 0x02 * i
            self.valDict["t" + str(i + 1)] = 0x1B + 0x02 * i

    def buildcmdx(self, addr=0x00, mode="read", value=0x0000):
        if mode == "read":
            checksum = addr * 256 + 82 + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x52, addr,
                   0x00, 0x00,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        elif mode == "set":
            valueHI = (value & 0xff00) >> 8
            valueLO = (value & 0x00ff)
            checksum = addr * 256 + 67 + value + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x43, addr,
                   valueLO, valueHI,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        else:
            print("mode错误 只能为read/set")
            return None

    def buildcmd(self, name="SV", mode="read", value=0x0000):
        if name not in self.valDict.keys():
            print("没有该参数值")
            return None
        if mode == "read":
            checksum = self.valDict[name] * 256 + 82 + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x52, self.valDict[name],
                   0x00, 0x00,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        elif mode == "set":
            valueHI = (value & 0xff00) >> 8
            valueLO = (value & 0x00ff)
            checksum = self.valDict[name] * 256 + 67 + value + self.addr
            checksumLO = (checksum & 0x00ff)
            checksumHI = (checksum & 0xff00) >> 8
            cmd = [0x80 + self.addr, 0x80 + self.addr,
                   0x43, self.valDict[name],
                   valueLO, valueHI,
                   checksumLO, checksumHI]
            cmd = bytearray(cmd)
            return cmd
        else:
            print("mode错误 只能为read/set")
            return None


    def read_data(self):
        data = self.port.read_all()
        if len(data) != 10:
            print("接收数据长度不对！")
            return None
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

            data = {"PV": PV, "SV": SV, "MV": MV, "HIAL": HIAL, "LoAL": LoAL, "dHAL": dHAL, "dLAL": dLAL, "orAL": orAL,
                    "AL1": AL1, "AL2": AL2, "VALUE": value}
            return data
        else:
            print("接收数据的校验和错误！")
            return None


    def setPlan(self, steps):
        for i in range(0, len(steps)):
            step = steps[i]
            self.sendcmd(self.buildcmd(name="C" + str(i + 1), mode="set", value=step["T"] * 10),
                         waittime=10)  # 温度有1位小数点
            self.sendcmd(self.buildcmd(name="t" + str(i + 1), mode="set", value=step["time"]), waittime=10)  # 时间没有小数点
            print("progress:" + str(i + 1) + "/" + str(len(steps)))

    def startOven(self):
        data = self.sendcmd(self.buildcmd(name="r/h/s", mode="set", value=0), waittime=10)
        if data is not None:
            print("启动成功")

    def stopOven(self):
        data = self.sendcmd(self.buildcmd(name="r/h/s", mode="set", value=12), waittime=10)
        if data is not None:
            print("停止成功")

    def pauseOven(self):
        data = self.sendcmd(self.buildcmd(name="r/h/s", mode="set", value=4), waittime=10)
        if data is not None:
            print("暂停成功")

    def getRuntime(self):
        data = self.sendcmd(self.buildcmd(name="runtime", mode="read"))
        return data["VALUE"]

    def getStep(self):
        data = self.sendcmd(self.buildcmd(name="SV/SteP", mode="read"))
        return data["VALUE"]

    def getInfo(self):
        data = self.sendcmd(self.buildcmd(name="SV/SteP", mode="read"))
        return data


if __name__ == "__main__":
    oven = Oven()
    steps = [{"T": 20, "time": 2}, {"T": 200, "time": 3}, {"T": 200, "time": 2}, {"T": 300, "time": 3},
             {"T": 300, "time": 1}, {"T": 20, "time": -121}]
    oven.setPlan(steps)
    oven.startOven()
    # for keys in oven.valDict:
    #     data = oven.sendcmd(oven.buildcmd(name=keys, mode="read"))
    #     print(keys + ":" + str(data))
