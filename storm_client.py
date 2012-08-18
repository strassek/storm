#!/usr/bin/env python

# The following script will control the Dream Cheeky Storm & Thunder USB
# Missile Launchers.  There are a few projects for using older launchers
# in Linux, but I couldn't find any for this launcher, so... enjoy.

# Thunder: http://www.dreamcheeky.com/thunder-missile-launcher
# O.I.C Storm: http://www.dreamcheeky.com/storm-oic-missile-launcher

# wasd to aim. hold spacebar to fire.

#from launcher.turret import MotorController
#from launcher.camera import VideoCapturePlayer
import xmlrpclib
import pygame
import time
import sys

if __name__ == '__main__':
	
	# select what camera to use
	if len(sys.argv) == 2:
		host = eval(sys.argv[1])
		port = eval(sys.argv[2])

	pygame.init()

	# Try to reduce some of the noise in the event queue
	pygame.event.set_allowed(None)
	pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

	proxy = xmlrpclib.ServerProxy("http://localhost:8000/")

	while True:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_d:
					proxy.right()		
				elif event.key == pygame.K_a:
					proxy.left()
				elif event.key == pygame.K_w:
					proxy.up()
				elif event.key == pygame.K_s:
					proxy.down()
				elif event.key == pygame.K_SPACE:
					proxy.fire()
				elif event.key == pygame.K_q:
					proxy.quit()
					exit()
			else:
				proxy.stop()

