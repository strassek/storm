#!/usr/bin/env python

# The following script will control the Dream Cheeky Storm & Thunder USB
# Missile Launchers.  There are a few projects for using older launchers
# in Linux, but I couldn't find any for this launcher, so... enjoy.

# Thunder: http://www.dreamcheeky.com/thunder-missile-launcher
# O.I.C Storm: http://www.dreamcheeky.com/storm-oic-missile-launcher

# wasd to aim. hold spacebar to fire.

from launcher.turret import MotorController
from launcher.camera import Camera
from sys import exit
import pygame
import time

if __name__ == '__main__':
	try:
		lc = MotorController()
	except ValueError as detail:
		exit(detail)

	cam = Camera("/dev/video1")
	cam.takeVideo()
	while True:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_d:
					lc.right()		
				elif event.key == pygame.K_a:
					lc.left()
				elif event.key == pygame.K_w:
					lc.up()
				elif event.key == pygame.K_s:
					lc.down()
				elif event.key == pygame.K_SPACE:
					lc.fire()
					print "BANG!"
				elif event.key == pygame.K_q:
					cam.closeCam()
					exit()
			elif event.type == pygame.QUIT:
				cam.closeCam()
				exit()
			else:
				lc.stop()
		cam.vstream.next_frame()
