import serial
import time


class MFC(object):
    port = []

    def __init__(self):
        self.port = serial.Serial(port='COM3', baudrate=57600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                                  stopbits=serial.STOPBITS_ONE)

    def sleep(self):
        time.sleep(0)  # 若过小的话，控制可能不会相应

    def read_data(self):
        data = self.port.read_until(terminator=bytearray([0x0d]))
        data = data[0:-1]  # 去掉最后的换行符
        return data

    def send_cmd(self, cmd):
        self.port.write(cmd)
        # print("done:" + str(cmd))
        # self.sleep()

    def request_data(self, name):
        cmd = bytearray([ord(name), 0x0d])
        self.send_cmd(cmd)
        return self.read_data()

    def set_value(self, name, value):
        self.sleep()
        value = str(value)
        cmd = [ord(name), ord('S')]
        for i in value:
            cmd.append(ord(i))
        cmd.append(0x0d)
        cmd = bytearray(cmd)
        self.send_cmd(cmd)
        self.read_data()
        self.sleep()

    def set_gastype(self, name, type):
        self.sleep()
        TYPE = ['Air', 'Ar', 'CH4', 'CO', 'CO2', 'C2H6', 'H2', 'He', 'N2', 'N2O', 'Ne', 'O2', 'C3H8', 'n-C4H10', 'C2H2',
                'C2H4', 'i-C2H10', 'Kr', 'Xe', 'SF6', 'C-25', 'C-10', 'C-8', 'C-2', 'C-75', 'A-75', 'A-25', 'A1025',
                'Star29', 'P-5']
        if type not in TYPE:
            print('no such type,default=N2')
            type = 8
        else:
            type = TYPE.index(type)
        type = str(type)
        cmd = [ord(name), ord('$'), ord('$')]
        for i in type:
            cmd.append(ord(i))
        cmd.append(0x0d)
        cmd = bytearray(cmd)
        self.send_cmd(cmd)
        self.read_data()
        self.sleep()

    def parse_data(self, data):
        d_list = data.split()
        result = {
            'DeviceName': d_list[0],
            'AbsolutePressure': float(d_list[1]),
            'Temperature': float(d_list[2]),
            'VolumeFlow': float(d_list[3]),
            'MassFlow': float(d_list[4]),
            'Setting': float(d_list[5]),
            'GasType': d_list[6]
        }
        return result


def readall(port):
    line = []
    while True:
        x = port.read(1)
        line.append(x)
        if x == b'\r':
            break
    return line
