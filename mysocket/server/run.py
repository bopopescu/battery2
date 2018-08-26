#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
# @author:wx
#xindu

from socketClass import socketListen


def run_iot():

	socketRun = socketListen(3092)
	socketRun.listen()


if __name__ == '__main__':

	run_iot()




