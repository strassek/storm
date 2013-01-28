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

from ConfigParser import ConfigParser
import os

class Config(ConfigParser):
    internal = {}
    filename = ''

    def __init__(self):
        ConfigParser.__init__(self)

    def load(self, fn):
        self.filename = fn
        self.read(fn)

    def save(self):
        with open(self.filename, 'w') as f:
            self.write(f)

    def get(self, section, val=None, default=None):
        if val is None:
            return self.internal[section]
        else:
            try:
                return ConfigParser.get(self, section, val)
            except:
                if default is not None:
                    return default
                raise

    def set(self, section, val, value=None):
        if value is None:
            self.internal[section] = val
        else:
            if not self.has_section(section):
                self.add_section(section)
            ConfigParser.set(self, section, val, value)

    def has_option(self, section, name):
        try:
            return ConfigParser.has_option(self, section, name)
        except:
            return False

    def getlist(self, section, option, separator=","):
        s = self.get(section, option).strip()
        if s:
            return [i.strip() for i in s.split(separator)]
        else:
            return []
