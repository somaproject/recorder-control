#!/usr/bin/python
"""
Soma configuration interface

Miscellaneous soma configuration information

Ideally we would directly query soma for all of this information

but this is some sort of proxy?

I'm not entirely sure here


Event type->src mapping is perhaps something that we want here?


"""


Events = {0 : "Timer",
          1 : "SystemControl",
          2 : "BootStore",
          3 : "NetControl",
          4 : "Ethernet",
          5 : "SystemStatus",
          6 : "JTAG",
          7 : "DSP00", 
          8 : "DSP01"
          }

class Configuration(object):

    def __init__(self):


        self.datasources = range(0, 31)


configuration = Configuration()
