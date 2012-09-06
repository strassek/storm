""" Keeping things as simple as possible for now 
channel setup is static
will need to be able to cooperate with other robovero
classes in the future.
also, it would be a good idea if this module could handle
arbitrary channel settings
"""

from robovero.lpc17xx_mcpwm import MCPWM_Init, MCPWM_CHANNEL_CFG_Type, \
                      MCPWM_ConfigChannel, MCPWM_DCMode, MCPWM_ACMode, \
                      MCPWM_Start, MCPWM_WriteToShadow, MCPWM_Stop,    \
                      MCPWM_CHANNEL_EDGE_MODE, MCPWM_CHANNEL_PASSIVE_HI
from robovero.arduino import pinMode, digitalWrite, P0_4, P0_5, P2_3, P2_4
from robovero.arduino import OUTPUT, LOW, HIGH

from robovero.extras import roboveroConfig
from robovero.LPC17xx import LPC_MCPWM
from robovero.lpc_types import FunctionalState
import sys

ENABLE = FunctionalState.ENABLE
DISABLE = FunctionalState.DISABLE

class MotorController():
    def __init__(self, periodValue = 900):
        self.periodValue = periodValue
        
        roboveroConfig()

        MCPWM_Init(LPC_MCPWM)

        self.channelsetup = MCPWM_CHANNEL_CFG_Type()
          
        self.channelsetup.channelType = MCPWM_CHANNEL_EDGE_MODE
        self.channelsetup.channelPolarity = MCPWM_CHANNEL_PASSIVE_HI
        self.channelsetup.channelDeadtimeEnable = DISABLE
        self.channelsetup.channelDeadtimeValue = 0
        self.channelsetup.channelUpdateEnable = ENABLE
        self.channelsetup.channelTimercounterValue = 0
        self.channelsetup.channelPeriodValue = periodValue
        self.channelsetup.channelPulsewidthValue = 900

        MCPWM_ConfigChannel(LPC_MCPWM, 0, self.channelsetup.ptr)
        MCPWM_ConfigChannel(LPC_MCPWM, 1, self.channelsetup.ptr)

        # Disable DC Mode
        MCPWM_DCMode(LPC_MCPWM, DISABLE, ENABLE, (0))

        # Disable AC Mode
        MCPWM_ACMode(LPC_MCPWM, DISABLE)

        # Enable channels 0 and 1
        MCPWM_Start(LPC_MCPWM, ENABLE, ENABLE, DISABLE)

	pinMode(P0_4, OUTPUT)
	pinMode(P0_5, OUTPUT)
	pinMode(P2_3, OUTPUT)
	pinMode(P2_4, OUTPUT)

    def set_speed(self, req_channel, req_speed):
        channel = int(req_channel)
        speed = int(req_speed)
        if channel not in range (2):
            sys.stdout.write("Skipping set_speed. Channel out of bounds.\n")
            return None
        if speed < 0 or speed > 100:
            sys.stdout.write("Skipping set_speed. New speed out of bounds.\n")
            return None

        self.channelsetup.channelPulsewidthValue = speed * self.periodValue / 100
        MCPWM_WriteToShadow(LPC_MCPWM, channel, self.channelsetup.ptr)

    def set_direction(self, req_channel, req_direction):
	channel = int(req_channel)
	direction = int(req_direction)

	if channel == 1:
		if direction == 0:
			digitalWrite(P0_4, HIGH)
			digitalWrite(P0_5, LOW)
		elif direction == 1:
			digitalWrite(P0_4, LOW)
			digitalWrite(P0_5, HIGH)		
		else:
			digitalWrite(P0_4, LOW)
			digitalWrite(P0_5, LOW)	
	if channel == 0:
		if direction == 0:
			digitalWrite(P2_3, HIGH)
			digitalWrite(P2_4, LOW)
		elif direction == 1:
			digitalWrite(P2_3, LOW)
			digitalWrite(P2_4, HIGH)		
		else:
			digitalWrite(P2_3, LOW)
			digitalWrite(P2_4, LOW)	
        
if __name__ == '__main__':
    motors = MotorController()

    try:
        while True:
            new_channel = raw_input("Channel: ") 
            new_speed = raw_input("Speed (%): ")
	    new_direction = raw_input("Direction: ")
            motors.set_speed(new_channel, new_speed)
	    motors.set_direction(new_channel, new_direction)   
    except:
        MCPWM_Stop(LPC_MCPWM, ENABLE, ENABLE, DISABLE)
        digitalWrite(P0_4, LOW)
	digitalWrite(P0_5, LOW)
	digitalWrite(P2_3, LOW)
	digitalWrite(P2_4, LOW)
        sys.stdout.write("You brode it.\n")

