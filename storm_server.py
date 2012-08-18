#!/usr/bin/env python

# The following script will control the Dream Cheeky Storm & Thunder USB
# Missile Launchers.  There are a few projects for using older launchers
# in Linux, but I couldn't find any for this launcher, so... enjoy.

# Thunder: http://www.dreamcheeky.com/thunder-missile-launcher
# O.I.C Storm: http://www.dreamcheeky.com/storm-oic-missile-launcher

# wasd to aim. hold spacebar to fire.

from SimpleXMLRPCServer import SimpleXMLRPCServer
from launcher.turret import MotorController
#from launcher.camera import VideoCapturePlayer
import pygame
import time
import sys

def quit()
	sys.exit()

if __name__ == "__main__":
	turret = MotorController()
	server = SimpleXMLRPCServer(("localhost", 8000))
	print "Listening on port 8000..."
	server.register_function(turret.up, "up")
	server.register_function(turret.down, "down")
	server.register_function(turret.left, "left")
	server.register_function(turret.right, "right")
	server.register_function(turret.fire, "fire")
	server.register_function(turret.stop, "stop")
	server.register_function(quit, "quit")
	server.serve_forever()
