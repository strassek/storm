"""
Control interface for articulating the turret and firing missles 
"""

import usb.core
import time

class MotorController():
	"""
	Controls the basic motor functionality provided by the USB interface.
	"""

	def __init__(self):
		self.dev = usb.core.find(idVendor=0x2123, idProduct=0x1010)
		if self.dev is None:
			raise ValueError('Launcher not found.')
		if self.dev.is_kernel_driver_active(0) is True:
			 self.dev.detach_kernel_driver(0)
		self.dev.set_configuration()

	def up(self):
		"""Tilt the turret up"""

		self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x02,0x00,0x00,0x00,0x00,0x00,0x00]) 

	def down(self):
		"""Tilt the turret down"""

		self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00])

	def left(self):
		"""Rotate the turret left"""

		self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x04,0x00,0x00,0x00,0x00,0x00,0x00])

	def right(self):
		"""Rotate the turret right"""

		self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x08,0x00,0x00,0x00,0x00,0x00,0x00])

	def stop(self):
		"""Stop all movement"""
		
		self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x20,0x00,0x00,0x00,0x00,0x00,0x00])

	def fire(self):
		"""Advance barrel and fire a shot"""

		self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x10,0x00,0x00,0x00,0x00,0x00,0x00])
		# The launcher needs a few seconds to complete this action
		time.sleep(4)

class StormMotor(MotorController):
	"""
	Offers some abstractions and functionality that are useful when operating 
	the camera enabled storm launcher.
	"""
	def corrected_fire(self, delta_x=0.0, delta_y=0.0):
		"""Adjust the turret before firing and then return to initial position"""
		self.up()
		time.sleep(0.3)
		self.stop()
		self.fire()
		self.down()
		time.sleep(0.25)
		self.stop()
