"""Set position of servo 1 (PWM1) to an angle provided by the user.

You must have an RC servo connected to PWM1 for this example. Otherwise, you
can observe the control signal with an oscilloscope or logic analyzer.
"""

from robovero.LPC17xx import LPC_PWM1
from robovero.lpc17xx_pwm import PWM_TC_MODE_OPT, \
					PWM_MATCH_UPDATE_OPT, PWM_MATCHCFG_Type, \
					PWM_MatchUpdate, PWM_ConfigMatch, PWM_ChannelCmd, \
					PWM_ResetCounter, PWM_CounterCmd, PWM_Cmd
from robovero.extras import roboveroConfig, initMatch
from robovero.lpc_types import FunctionalState

from robovero.arduino import analogWrite, PWM1

# Entry Point
roboveroConfig()

def getServoAngle(raw_angle):
	"""Get an angle and calculate new duty cycle.
	"""
	try:
		angle = int(raw_angle)
		if angle < 0 or angle > 180:
			raise InputError
	except:
		return None
	match_value = 1100 + (angle*500/180)
	return match_value

class MotorController():

	def __init__(self, log, period=20000):
		"""Set up PWM at 50Hz.
		"""
		self.log = log

		# Set the period to 20000us = 20ms = 50Hz
		initMatch(0, period)

		PWM_ResetCounter(LPC_PWM1)
		PWM_CounterCmd(LPC_PWM1, FunctionalState.ENABLE)
		PWM_Cmd(LPC_PWM1, FunctionalState.ENABLE)

		self.channels = []
		self.log.info("Initialized BLDC motor controller.")	

	def add_channel(self, raw_channel, init_pulse = 1500):
		"""Add PWM channel with a 1.5ms pulse.
		"""
		try:
			channel = int(raw_channel)
			if channel < 1 or channel > 5:
				raise InputError
		except:
			self.log.warning("%s is an invalid channel." % raw_channel)
			return None 
		
		# Check if channel has already been added
		if channel in self.channels:
			self.log.warning("Channel %d has already been initialized." % channel)
			return None

		self.channels.append(channel)

		initMatch(channel, init_pulse)
		PWM_ChannelCmd(LPC_PWM1, channel, FunctionalState.ENABLE)
		#TODO: might need counter commands here. check this first.

		self.log.info("Initializing BLDC pwm channel %d." % channel)

	def set_pulse(self, channel, raw_pulse):
		
		if channel not in self.channels:
			self.log.warning("%s is invalid or is not an initialized channel." % channel)
			return None
		
		try:
			pulse = int(raw_pulse)
			if pulse < 0:
				raise InputError
		except:
			self.log.warning("%s is an invalid pulse." % raw_pulse)
			return None
		
		PWM_MatchUpdate(LPC_PWM1, channel, pulse, PWM_MATCH_UPDATE_OPT.PWM_MATCH_UPDATE_NOW)

