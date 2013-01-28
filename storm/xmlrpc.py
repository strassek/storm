# Copyright (C) 2007 Free Software Foundation, Inc.
# This file contains code that is adapted from Ajenti.
# Written by Eugeny Pankov, 2010-2011.
#
# Ajenti is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; only
# version 3 of the License.
#
# Ajenti is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this file; if not, see <http://www.gnu.org/licenses/>

import sys
import os
import time
import logging

from SimpleXMLRPCServer import SimpleXMLRPCServer
from storm.config import Config
from storm.control import Control
from storm.auto import AutoPilotManager
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

    dformatter = logging.Formatter('%(asctime)s %(levelname)-8s %(module)s.%(funcName)s(): %(message)s')
    stdout.setFormatter(dformatter)

    log.addHandler(stdout)

    return log

def run_server(log_level=logging.INFO, config_file=''):
    log = make_log(debug=log_level==logging.DEBUG, log_level=log_level)

    log.info('Storm %s' % version)

    config = Config()
    if config_file:
        log.info('Using config file %s' % config_file)
        config.read(config_file)
    else:
        log.info('Using default settings')

    config.set('log_facility', log)
    
    control = Control(config)
    config.set('control_facility', control)

    autopilot = AutoPilotManager(config)

    host = config.get('xmlrpc','bind_host')
    port = config.getint('xmlrpc','bind_port')
    log.info('xmlrpc listening on %s:%d' % (host, port))

    server = SimpleXMLRPCServer((host, port), logRequests=False, allow_none=True)
    server.register_function(control.motors.set_pulse, "set_pulse")
    server.register_function(control.cam.play, "cam_play")
    server.register_function(control.cam.pause, "cam_pause")
    server.register_function(autopilot.start, "autopilot_run")
    server.register_function(autopilot.stop, "autopilot_stop")
    server.register_function(control.move_forward, "move_forward")
    server.register_function(control.move_left, "move_left")
    server.register_function(control.move_right, "move_right")
    server.register_function(control.move_up, "move_up")
    server.register_function(control.move_down, "move_down")
    server.register_function(control.hover, "hover")

    log.info('Starting server')
    server.serve_forever()

