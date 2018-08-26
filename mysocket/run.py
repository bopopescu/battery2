#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
# @author:wx
#xindu

from socketClass import socketListen
from socketClient import socketConnect

def run_iot():

	socketRun = socketConnect("localhost", 3092)
	socketRun.connect()


if __name__ == '__main__':

	run_iot()




