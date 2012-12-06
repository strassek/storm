from robovero.extras import roboveroConfig

from storm.bldc import MotorController
from storm.cam import VidServer
from storm.sensor import UltraSonic, IR

class Control():
    
    def __init__(self, config):
        roboveroConfig()
        self.motors = MotorController(config)
        self.cam = VidServer(config)
        self.ultrasonic_sensor = UltraSonic(config)
        self.ir_sensor = IR(config)

        self.target_altitude = config.getfloat("control", "target_altitude")
        self.left_clearance = config.getfloat("control", "left_clearance")
        self.right_clearance = config.getfloat("control", "right_clearance")
        self.pulse_hi = config.getint("control", "pulse_hi")
        self.pulse_low = config.getint("control", "pulse_low")
        self.pulse_arm = config.getint("control", "pulse_arm")
        self.left_channel = config.getint("control", "left_channel")
        self.right_channel = config.getint("control", "right_channel")
        self.bottom_channel = config.getint("control", "bottom_channel")

    def too_low(self):
        if self.ultrasonic_sensor.read_measurement() < self.target_altitude:
            return True
        else:
            return False

    def left_blocked(self):
        if self.ir_sensor.read_left() < self.left_clearance:
            return True
        else:
            return False

    def right_blocked(self):
        if self.ir_sensor.read_right() < self.right_clearance:
            return True
        else:
            return False

    def move_up(self):
        self.motors.set_pulse(self.bottom_channel, self.pulse_hi)

    def move_down(self):
        self.motors.set_pulse(self.bottom_channel, self.pulse_low)

    def move_forward(self):
        self.motors.set_pulse(self.left_channel, self.pulse_hi) 
        self.motors.set_pulse(self.right_channel, self.pulse_hi) 

	def move_back(self):
		pass

    def move_left(self):
        self.motors.set_pulse(self.left_channel, self.pulse_low) 
        self.motors.set_pulse(self.right_channel, self.pulse_hi) 
    
    def move_right(self):
        self.motors.set_pulse(self.left_channel, self.pulse_hi) 
        self.motors.set_pulse(self.right_channel, self.pulse_low) 

    def hover(self):
        self.motors.set_pulse(self.left_channel, self.pulse_low) 
        self.motors.set_pulse(self.right_channel, self.pulse_low) 

