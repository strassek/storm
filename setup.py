#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
	name="storm",
	version="1.0",
	install_requires=[
		"pygst",
		"pygtk",
	],
	author="Kevin Strasser",
	author_email="kevstras@gmail.com",
	long_description=open("README.md").read(),
	license="MIT",
	url="http://github.com/strassek/storm",
	packages = find_packages(),
	scripts=['storm-server', 'storm-client'],
	data_files=[
		('/etc/storm', ['packaging/files/storm.conf']),
		('/etc/init.d', ['packaging/files/storm']),
	],
)
