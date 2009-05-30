import gobject

from experiment import Experiment
import time

class Manager(gobject.GObject):
    __gsignals__ = { 'ExperimentAvailable': (gobject.SIGNAL_RUN_FIRST,
                                           gobject.TYPE_NONE,
                                           (gobject.TYPE_OBJECT,)), 
                     'StatsUpdate': (gobject.SIGNAL_RUN_FIRST,
                                     gobject.TYPE_NONE,
                                     tuple()) }

    def __init__(self):
        gobject.GObject.__init__(self)
        self.experiments = {}
        self.stats = {}
        self.stats["somaip"] = "127.0.0.1"
        self.stats["recorderip"] = "18.238.0.1"
        self.stats["time"] = str(time.time())
        self.stats["path"] = "/usr/local/bin/blah"
        self.stats["cwd"] = "/home/jonas"
        self.stats["user"] = "root"
        self.stats["dbuspath"] = "soma.Recorder"
        self.stats["diskfree"] = "127.8 GB"
        self.stats["version"] = "127.8 GB"

        self.timer_id = gobject.timeout_add(1000, self.updateTime)

    # ----------------------------------------------------------------
    # DBUS METHODS (proxy)
    # ----------------------------------------------------------------    
    def ListOpenExperiments(self):
        """
        Returns the list of all availabe open experiments,
        by connection
        """
        return self.experiments.values() # [v for k, v in self.experiments.iteritems()]
    
    def ListAvailableExperiments(self):
        """
        return the names of all available experiments, as strings
        that could be used by OpenExperiment
        """
    
    def OpenExperiment(self, name):
        """
        Open the named experiment and return the object name
        """
        
    def CreateExperiment(self, name):
        """
        create a new experiment and return
        the object name
        """
        if name in self.experiments:
            raise NameError, "name %s already names an open experiment" % name
        
        e = Experiment(self, str(name))
        self.experiments[name] = e
        self.emit('ExperimentAvailable', e)
        return e

    def GetStatistics(self):
        """

        Return generic information about this recorder, like
        running path, user-running-as, uptime,
        soma IP, host machine IP, DBUS location, etc.
        
        """


        return self.stats
                
    # ----------------------------------------------------------------
    # SUPPORT METHODS (proxy)
    # ----------------------------------------------------------------    

    def getConnectionPath(self):
        """
        Return a string representing this connection
        """

    # ----------------------------------------------------------------
    # Implementation specific
    # ----------------------------------------------------------------    
        
    def updateTime(self):
        self.stats["time"] =  str(time.time())
        self.emit("StatsUpdate")
        
        return True
