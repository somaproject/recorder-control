#!/usr/bin/env python

from distutils.core import setup

setup(name='RecorderControl',
      version='1.0',
      description='Soma Recorder Control GUI', 
      author='Eric Jonas', 
      author_email='jonas@mit.edu', 
      url='http://soma.mit.edu',
      packages = ["somarecordercontrol",
                  "somarecordercontrol.proxy",
                  "somarecordercontrol.proxy.dbus",
                  "somarecordercontrol.proxy.mock"],       
      scripts=['soma-recorder-control'], 
      package_data = {"" : ["*.glade"]}
     )
