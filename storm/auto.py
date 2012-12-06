from threading import Thread
from time import sleep

class AutoPilot(Thread):
    
    def __init__(self, config):
        Thread.__init__(self)
        self.control = config.get("control_facility")
        self.running = True

    def run(self):
        while self.running: 
            if self.control.too_low():
                self.control.move_up()
            else:
                self.control.move_down()

            if self.control.left_blocked() and self.control.right_blocked():
                self.control.hover()
            elif self.control.left_blocked() and not self.control.right_blocked():
                self.control.move_right()
            elif not self.control.left_blocked() and self.control.right_blocked():
                self.control.move_left()
            else:
                self.control.move_forward()

            sleep(0.1)

    def stop(self):
        self.running = False

class AutoPilotManager():
    def __init__(self, config):
        self.config = config
        self.pilot_thread = AutoPilot(config)

    def start(self):
        self.pilot_thread.start()

    def stop(self):
        self.pilot_thread.stop()
        self.pilot_thread.join()
        del self.pilot_thread
        self.pilot_thread = AutoPilot(self.config)
