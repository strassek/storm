#!/usr/bin/env python

# The following script will control the Dream Cheeky Storm & Thunder USB
# Missile Launchers.  There are a few projects for using older launchers
# in Linux, but I couldn't find any for this launcher, so... enjoy.

# Thunder: http://www.dreamcheeky.com/thunder-missile-launcher
# O.I.C Storm: http://www.dreamcheeky.com/storm-oic-missile-launcher

# wasd to aim. hold spacebar to fire.

import sys
import os
import time
import logging

from SimpleXMLRPCServer import SimpleXMLRPCServer
from storm.pwm_motors import MotorController
from ConfigParser import SafeConfigParser
from storm import version

from datetime import datetime

class DebugHandler(logging.StreamHandler):
    def __init__(self):
        self.capturing = False
        self.buffer = ''

    def start(self):
        self.capturing = True

    def stop(self):
        self.capturing = False

    def handle(self, record):
        if self.capturing:
            self.buffer += self.formatter.format(record) + '\n'

class ConsoleHandler(logging.StreamHandler):
    def __init__(self, stream, debug):
        self.debug = debug
        logging.StreamHandler.__init__(self, stream)

    def handle(self, record):
        if not self.stream.isatty():
            return logging.StreamHandler.handle(self, record)

        s = ''
        d = datetime.fromtimestamp(record.created)
        s += d.strftime("\033[37m%d.%m.%Y %H:%M \033[0m")
        if self.debug:
            s += ('%s:%s'%(record.filename,record.lineno)).ljust(30)
        l = ''
        if record.levelname == 'DEBUG':
            l = '\033[37mDEBUG\033[0m '
        if record.levelname == 'INFO':
            l = '\033[32mINFO\033[0m '
        if record.levelname == 'WARNING':
            l = '\033[33mWARN\033[0m '
        if record.levelname == 'ERROR':
            l = '\033[31mERROR\033[0m '
        s += l.ljust(9)
        s += record.msg
        s += '\n'
        self.stream.write(s)
	
def make_log(debug=False, log_level=logging.INFO):
    log = logging.getLogger('storm')
    log.setLevel(logging.DEBUG)

    stdout = ConsoleHandler(sys.stdout, debug)
    stdout.setLevel(log_level)

    log.blackbox = DebugHandler()
    log.blackbox.setLevel(logging.DEBUG)
    dformatter = logging.Formatter('%(asctime)s %(levelname)-8s %(module)s.%(funcName)s(): %(message)s')
    log.blackbox.setFormatter(dformatter)
    stdout.setFormatter(dformatter)
    log.addHandler(log.blackbox)

    log.addHandler(stdout)

    return log

def run_server(log_level=logging.INFO, config_file=''):
    log = make_log(debug=log_level==logging.DEBUG, log_level=log_level)

    log.info('Storm %s' % version)

    config = SafeConfigParser()
    if config_file:
        log.info('Using config file %s' % config_file)
        config.read(config_file)
    else:
        log.info('Using default settings')

	
    motors = MotorController(log)

    host = config.get('storm','bind_host')
    port = config.getint('storm','bind_port')
    log.info('Listening on %s:%d' % (host, port))

    server = SimpleXMLRPCServer((host, port), logRequests=False, allow_none=True)
    server.register_function(motors.set_speed, "set_speed")
    server.register_function(motors.set_direction, "set_direction")

    log.info('Starting server')
    server.serve_forever()

