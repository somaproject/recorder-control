from epoch import Epoch
import gobject
import notesinterface

class Experiment(gobject.GObject, notesinterface.Notes):
    __gsignals__ = { 'EpochCreate': (gobject.SIGNAL_RUN_FIRST,
                                      gobject.TYPE_NONE,
                                      (gobject.TYPE_OBJECT,)),
                     'NoteChange': (gobject.SIGNAL_RUN_FIRST,
                                    gobject.TYPE_NONE,
                                    (gobject.TYPE_INT, gobject.TYPE_INT))
                     'ReferenceTimeChange': (gobject.SIGNAL_RUN_FIRST,
                                             gobject.TYPE_NONE,
                                             (gobject.TYPE_UINT64,))
                     }

    
    def __init__(self, recorder, name):
        gobject.GObject.__init__(self)
        notesinterface.Notes.__init__(self)

        self.recorder = recorder
        self._epochsOrdered = []
        self._epochs = {}
        self._name = name
        self._datasources = []
        for i in xrange(64):
           self._datasources.append((i, True, [], "SOURCE%2.2d" % i))
        
        self.notes = []re

        self.properties = {"user" : "jonas",
                           "create" : "2008-01-01 22:33"}

        self._isRecording = False
        self.recordingEpoch = None

        self.ts = 1000
        self.time = 10000000
        self.referenceTime = 0
        
        
    def GetFileProperties(self):
        """
        Return a dict of string->string consisting of
        experiment (file) properties.

        """
        
        return self.properties
    
    def GetEpochs(self):
        """
        Returns the Epoch Objects for this experiment.
        
        """
        
        return self._epochsOrdered

    def GetName(self):
        return self._name

    def CreateEpoch(self, name):
        """
        Returns the created object. 
        """
        
        if name in self._epochs:
            raise "Epoch name already exists"
        
        e = Epoch(self, name)
        self._epochsOrdered.append(e)
        self._epochs[name] = e
        self.emit("EpochCreate", e)
        return e

    def RenameEpoch(self, epoch, name):
        """
        """
        print "Mock proxy Epoch rename called"
        
        for k, v in self._epochs.iteritems():
            if v == epoch:
                del self._epochs[k]
                epoch.setName(name)
                self._epochs[name] = epoch
                break

    def deleteEpoch(self, name):
        if name not in self._epochs:
            raise "Epoch name not found"
        e = self._epochs[name]
        self._epochs.erase(e)
        self._epochsOrdered.remove(e)
        
    def epochListUpdated():
        pass

    def getPath(self):
        return "mock object, no dbus path"

        
    def GetReferenceTimeStamp(self):
        return self.referenceTS
    

    def SetReferenceTimeStamp(self, ts):
        self.referenceTS = ts
        
        self.emit("ReferenceTimeChange", e)

    
    
