"""
Interface for the launcher's onboard webcam.
"""
import pygame
import Image
import sys
import time
import cv

class Camera:
	"""Contains device settings and allows the camera to take pictures and video"""
	def __init__(self, device = "/dev/video0", fps = 30, width = 640, height = 480):
		self.device = device
		self.setCamDevice(self.device)
		self.fps = fps
		self.width = width
		self.height = height
		self.vthread = None
		
	def setCamDevice(self, device):
		self.camera = None
		if device == "/dev/video0":
			self.camera = cv.CaptureFromCAM(0)
		if device == "/dev/video1":
			self.camera = cv.CaptureFromCAM(1)
		if device == "/dev/video2":
			self.camera = cv.CaptureFromCAM(2)
		if device == "/dev/video3":
			self.camera = cv.CaptureFromCAM(3)

	def setFPS(self, fps):
		self.fps = fps

	def setResolution(self, width, height):
		self.width = width
		self.height = height
		cv.SetCaptureProperty(self.camera, cv.CV_CAP_PROP_FRAME_WIDTH,width)
		cv.SetCaptureProperty(self.camera, cv.CV_CAP_PROP_FRAME_HEIGHT,height)


	def takePhoto(self):
		self.window = pygame.display.set_mode((self.width,self.height))
		pygame.display.set_caption("Storm | Photo")
		self.screen = pygame.display.get_surface()
		im = self.getImage()
		pg_img = pygame.image.frombuffer(im.tostring(), cv.GetSize(im), "RGB")
		self.screen.blit(pg_img, (0,0))
		pygame.display.flip()

	def takeVideo(self):
		self.vstream = VideoStream(self)

	def closeCam(self):
		pygame.display.quit()
		self.camera = None
		self.setCamDevice(self.device)

	def getImage(self):
		im = cv.QueryFrame(self.camera)
		return im
	
class VideoStream():
	"""Facilitates viewing the camera as a video stream"""
	def __init__(self, camera):
		self.camera = camera
		self.time = time.clock()
		self.camera.window = pygame.display.set_mode((self.camera.width,self.camera.height))
		pygame.display.set_caption("Storm | Video")
		self.camera.screen = pygame.display.get_surface()

	def next_frame(self):
		"""Refresh the frame with a new image from the camera."""
		if (time.clock() - self.time) < (1 / float(self.camera.fps)):
			return
		self.time = time.clock()
		im = self.camera.getImage()
		pg_img = pygame.image.frombuffer(im.tostring(), cv.GetSize(im), "RGB")
		self.camera.screen.blit(pg_img, (0,0))
		pygame.display.flip()
 
if __name__ == "__main__":
	cam = Camera()
	cam.takeVideo()
	while True:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					cam.closeCam()
					sys.exit()
		cam.vstream.next_frame()
