#!/usr/bin/env python

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

setup(
	name="storm",
	version="0.1",
	install_requires=[
		"pygame",
		"pyusb",
	],
	author="Kevin Strasser",
	author_email="kevstras@gmail.com",
	description="USB Missile Launcher Controller",
	long_description=open("README.md").read(),
	license="MIT/X11",
	url="http://github.com/strassek/storm",
)
