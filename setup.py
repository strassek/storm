#!/usr/bin/env python

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

setup(
	name="storm",
	version="1.0",
	install_requires=[
		"pygame",
		"pyusb",
	],
	author="Kevin Strasser",
	author_email="kevstras@gmail.com",
	description="Dream Cheeky USB Missile Launcher Controller",
	long_description=open("README.md").read(),
	license="MIT/X11",
	url="http://github.com/strassek/storm",
	packages = find_packages()
	package_data = 
	scripts=['storm-panel'],
	data_files=[
		('/etc/storm', ['packaging/files/storm.conf']),
		('/etc/init.d', ['packaging/files/storm']),
	],
)
