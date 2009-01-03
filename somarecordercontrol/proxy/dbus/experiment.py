#!/usr/bin/python
"""
Proxy object for DBUS Recorder interface

"""
import gobject
import dbus
import dbus.service
from epoch import Epoch
from note import Note
from notesinterface import *

class Experiment(gobject.GObject, NotesInterface):

    # signals?

    __gsignals__ = { 'epochcreate': (gobject.SIGNAL_RUN_FIRST,
                                     gobject.TYPE_NONE,
                                     (gobject.TYPE_OBJECT,)),
                     'notechange': (gobject.SIGNAL_RUN_FIRST,
                                    gobject.TYPE_NONE,
                                    (gobject.TYPE_INT, gobject.TYPE_INT))
                     }
    
    def __init__(self, bus, dbusobj):
        gobject.GObject.__init__(self)
        NotesInterface.__init__(self, dbusobj)
        
        self.bus = bus
        self.dbusobj = dbusobj
        self.dbusExperimentIface = dbus.Interface(dbusobj,
                                                  "soma.recording.Experiment")
        
        self.epochObjCache = {}
        
        epaths = self.dbusExperimentIface.GetEpochs()

        
    def GetFileProperties(self):
        """
        Return a dict of string->string consisting of
        experiment (file) properties.

        """
        
        return self.properties
    
    def GetEpochs(self):
        """
        Returns the Epoch Objects for this experiment, in the
        CANONICAL ORDER
        
        """
        # get the epoch objects for all of the returned paths
        print "YO: Getting epochs"
        epaths = self.dbusExperimentIface.GetEpochs()
        print "done"
        # performs an implict sync
        objs = []
                
        for epath in epaths:
            if epath not in self.epochObjCache.keys():
                eobj = self.bus.get_object(self.dbusExperimentIface.bus_name,
                                           eobjpath)
                
                e = Epoch(self, eobj)
                
                self.epochObjCache[eobjpath] = e
                objs.append(e)
            else:
                objs.append(self.epochObjCache[epath])
        
        return objs


    def GetName(self):
        return self.dbusExperimentIface.GetName()

    
    def CreateEpoch(self, name):
        """
        May throw exception, indicating name already exists
        """
        print "proxy.dbus.Experiment::CreateEpoch"
        eobjpath = self.dbusExperimentIface.CreateEpoch(name)
        eobj = self.bus.get_object(self.dbusobj.bus_name,
                                   eobjpath)
        
        e = Epoch(self, eobj)

        self.epochObjCache[eobjpath] = e
        
        self.emit("epochcreate", e)
        
        return e

    def RenameEpoch(self, epoch, name):
        self.dbusExperimentIface.RenameEpoch(epoch.dbusobject.object_path,
                                             name)
        epoch.setName(name)
        
    def deleteEpoch(self, name):
        if name not in self.epochs:
            raise "Epoch name not found"
        e = self.epochs[name]
        self.epochs.erase(e)
        self.epochsOrdered.remove(e)
        
    def setRecording(self, isRecording):
        self.state = isRecording
    
    def epochListUpdated():
        pass

    def getPath(self):
        return self.dbusobj.object_path


        
    
