from robovero.arduino import analogRead, AD0_0, AD0_1, AD0_2, AD0_3, AD0_5, AD0_6, AD0_7

channel_to_pin = {
    0: AD0_0,
    1: AD0_1,
    2: AD0_2,
    3: AD0_3,
    5: AD0_5,
    6: AD0_6,
    7: AD0_7,
}

class UltraSonic():

    def __init__(self, config):
        
        log = config.get('log_facility')
        scale = config.getfloat('ultrasonic', 'scale')
        channel = config.getint('ultrasonic', 'channel')
        log.info("Initialized UltraSonic controller")

        self.log = log
        self.config = config
        self.scale = 1 / scale
        self.pin = channel_to_pin[channel]

    def read_raw(self):
        return analogRead(self.pin)

    def read_measurement(self):
        """In inches"""
        return (analogRead(self.pin) * self.scale)

class IR():
    def __init__(self, config):

        log = config.get('log_facility')
        channels = config.getlist('ir', 'channels')

        self.left_pin = channel_to_pin[int(channels[0])]
        self.right_pin = channel_to_pin[int(channels[1])]
        self.log = log

    def read_right(self):
        return analogRead(self.right_pin)

    def read_left(self):
        return analogRead(self.left_pin)
