#!/usr/bin/env python

"""
Provides a control interface to the turret.
"""

import sys
import usb
import logging

class MotorController():
	"""
	Controls the basic motor functoinality provided by the USB interface.
	"""

	def __init__(self, log=sys.stdout, vendor=0x2123, product=0x1010):
		self._log = log
		devices_list = [ list(bus.devices) for bus in usb.busses() ]
		devices = sum(devices_list, [])
		
		for d in devices:
			if d.idVendor == vendor and d.idProduct == product:
				self._handle = handle = d.open()	

		try:
			handle.reset()
			handle.claimInterface(0)
		except NameError:
			self._log.error("Device not found.")
			sys.exit(2)
		except:
			handle.detachKernelDriver(0)
			handle.reset()
			handle.claimInterface(0)

	def send(self, command):
		self._handle.controlMsg(0x21, 0x09, [0x02, command], 0x0200)

	def down(self):
		self.send(0x01)

	def up(self):
		self.send(0x02)

	def left(self):
		self.send(0x04)

	def right(self):
		self.send(0x08)

	def fire(self):
		self.send(0x10)

	def stop(self):
		self.send(0x20)

