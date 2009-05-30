#!/usr/bin/python
"""
Proxy object for DBUS Recorder interface

"""
import gobject
import dbus
import dbus.service
from experiment import Experiment

def getRecorder():
    """
    Return the recorder, perhaps by bus/object lookup?

    """

class Manager(gobject.GObject):

    __gsignals__ = { 'ExperimentAvailable': (gobject.SIGNAL_RUN_FIRST,
                                           gobject.TYPE_NONE,
                                           (gobject.TYPE_OBJECT,)), 
                     'StatsUpdate': (gobject.SIGNAL_RUN_FIRST,
                                     gobject.TYPE_NONE,
                                     tuple()) }


    def __init__(self, bus, remoteObject):
        gobject.GObject.__init__(self)
        self.bus = bus
        
        self.remoteObject = remoteObject

        self.dbusRecorderIface = dbus.Interface(remoteObject,
                                                "soma.recording.Manager")
        
        self.expcache = {}

        # initial setup -- populate the cache
        for conn in self.dbusRecorderIface.ListOpenExperiments():
            obj = self.bus.get_object(conn, "/soma/recording/experiment")
            
            exp = Experiment(self.bus, obj)
            self.expcache[conn] = obj

        self.timer_id = gobject.timeout_add(1000, self.updateTime)

        self.dbusRecorderIface.connect_to_signal("ExperimentAvailable",
                                                 self.expAvailableCallBack)
        
    def ListOpenExperiments(self):
        """
        Get the list of connections, return the objects
        """
        explist = self.dbusRecorderIface.ListOpenExperiments()
        # explist is a list of the filenames, we then look up locally

        for conn in explist:
            if conn not in self.expcache:
                print "Warning, conn", conn, "not in expcache"

        return [v for k, v in self.expcache.iteritems()]

    def ListAvailableExperiments(self):
        raise "NotImplemented"

    def OpenExperiment(self, name):
        """
        No return value because we use the signal
        """
        
        self.dbusRecorderIface.OpenExperiment(name) 

    def CreateExperiment(self, name):
        print "calling createExperiment" 
        self.dbusRecorderIface.CreateExperiment(name) 

    def expAvailableCallBack(self, connection):
        """
        Callback object, we simply reflect the dbus object
        
        """
        print "expAvailableCallBack(self, connection):" 
        print "Connection =", connection
        obj = self.bus.get_object(connection, "/soma/recording/experiment")

        # local cache?  FIXME

        exp = Experiment(self.bus, obj)

        self.expcache[connection]  = exp
        self.emit("experimentavailable", exp)


    def getConnectionPath(self):
        """
        Return a string representing this connection
        """
        return self.dbusRecorderIface.bus_name
        
    def GetStatistics(self):
        return self.dbusRecorderIface.GetStatistics()
        
    def updateTime(self):
        self.emit("statsupdate")
        
        return True
