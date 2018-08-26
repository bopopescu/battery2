import serial
import serial.tools.list_ports
from time import sleep
from readall import MFC





p=MFC()

p.set_gastype('A','Air')
data=p.request_data('A')
print(p.parse_data(data))

p.set_value('A',1)
p.set_gastype('A','H2')


data=p.request_data('A')
print(p.parse_data(data))



p.set_value('A',0)
p.set_gastype('A','N2')

data=p.request_data('A')
print(p.parse_data(data))



