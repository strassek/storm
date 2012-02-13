#!/usr/bin/env python

# The following script will control the Dream Cheeky Storm & Thunder USB
# Missile Launchers.  There are a few projects for using older launchers
# in Linux, but I couldn't find any for this launcher, so... enjoy.

# Thunder: http://www.dreamcheeky.com/thunder-missile-launcher
# O.I.C Storm: http://www.dreamcheeky.com/storm-oic-missile-launcher

# wasd to aim. hold spacebar to fire.

from launcher.turret import MotorController
from launcher.camera import VideoCapturePlayer
from sys import exit
import pygame
import time

if __name__ == '__main__':
	try:
		turret = MotorController()
	except ValueError as detail:
		exit(detail)

	pygame.init()
	pygame.camera.init()
	cam = VideoCapturePlayer()

	# Try to reduce some of the noise in the event queue
	pygame.event.set_allowed(None)
	pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

	while True:
		cam.get_and_flip()
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_d:
					turret.right()		
				elif event.key == pygame.K_a:
					turret.left()
				elif event.key == pygame.K_w:
					turret.up()
				elif event.key == pygame.K_s:
					turret.down()
				elif event.key == pygame.K_SPACE:
					turret.fire()
					print "BANG!"
				elif event.key == pygame.K_q:
					pygame.quit()
					exit()
			#elif event.type == pygame.QUIT:
			#	pygame.quit()
			#	exit()
			else:
				turret.stop()
