import gobject
import time
import dbus
from notesinterface import *

class Session(object):

    def __init__(self, startts, starttime):
        self.startts = startts
        self.starttime = starttime
        self.stopts =  startts
        self.stoptime = starttime
        
    def toTuple(self):
        return (self.startts, self.starttime,
                self.stopts, self.stoptime)
    
class Epoch(gobject.GObject, NotesInterface):
    """
    The individual epoch 

    """
    
    __gsignals__ = { 'renamed': (gobject.SIGNAL_RUN_FIRST,
                                     gobject.TYPE_NONE,
                                     (gobject.TYPE_STRING,)),
                     'recordingstate': (gobject.SIGNAL_RUN_FIRST,
                                        gobject.TYPE_NONE,
                                        (gobject.TYPE_BOOLEAN,)),
                     'sinkchange': (gobject.SIGNAL_RUN_FIRST,
                                    gobject.TYPE_NONE,
                                    (gobject.TYPE_INT,)),
                     'notechange': (gobject.SIGNAL_RUN_FIRST,
                                    gobject.TYPE_NONE,
                                    (gobject.TYPE_INT, gobject.TYPE_INT))
                     }

    
    def __init__(self, parentExp, dbusobj):
        gobject.GObject.__init__(self)
        

        self.parentExp = parentExp
        self.dbusobject = dbusobj
        self.dbusEpoch = dbus.Interface(dbusobj,
                                      "soma.recording.Epoch")
        
##         self.dbusEpoch.connect_to_signal("renamed",
##                                          self.setName)
        self.dbusEpoch.connect_to_signal("recordingstate", 
                                         self.recordingStateChange)
        self.dbusEpoch.connect_to_signal("sinkchange",
                                         self.sinkChange)
    def sinkChange(self, tgt):
        print "proxy reemitting sinkchange", tgt
        self.emit("sinkchange", tgt)
        
    def getPath(self):
        return self.dbusEpoch.object_path

    def GetName(self):
        """
        Return the epoch name
        """
        return self.dbusEpoch.GetName()


    def StartRecording(self):
        """
        begin recording for this epoch
        Can steal recording from another epoch
        
        """
        return self.dbusEpoch.StartRecording()

    def StopRecording(self):
        """
        Stop the recording
        """
        return self.dbusEpoch.StopRecording()

    def GetRecordingState(self):
        return self.dbusEpoch.GetRecordingState()
    
    def setName(self, name):
        self.name = name
        self.emit("renamed", name)

    def recordingStateChange(self, isRecording):
        self.emit("recordingstate", isRecording)
        
    def EnableDataSink(self, src, typ):
        """
        src is the src #
        type is the type
        """
        print "dbus proxy enabling data sink", src, typ
        self.dbusEpoch.EnableDataSink(src, typ)
        
        
    def DisableDataSink(self, src, typ):
        """
        """
        self.dbusEpoch.DisableDataSink(src, typ)


    def GetDataSinks(self):
        """
        Returns a list of string tuples
        """
        return self.dbusEpoch.GetDataSinks()

        

    def GetDataSink(self,tgt):
        """
        Returns a list of string tuples
        """
        return self.dbusEpoch.GetDataSink(tgt)

        

    def SetDataName(self, src, name):
        """

        """
        self.dbusEpoch.SetDataName(src, name)

    def GetDataName(self, src):
        """

        """
        return self.dbusEpoch.GetDataName(src)
    

    def GetSinkSessionStats(self, src, typ, sessions):
        """
        The epochs stats... not entirely clear what these are yet! 

        """
        return self.dbusEpoch.GetDataName(src, typ, sessions)
        
    
    def GetSessions(self):
        """
        Get epoch recording sessions
        """

        # convert the sessions
        return self.dbusEpoch.GetSessions()

    def AddEventRXMask(self, enableEvent, cmdlist):
        """
        Recive the cartesian product of sources and commands
        
        """
        return self.dbusEpoch.AddEventRXMask(enableEvent, cmdlist)

    def GetEventRXMask(self, source, cmdlist):
        """
        returns a list of all the events that we receive

        """
        raise "notImplemented"
    
    def RemoveEventRXMask(self, source, cmdlist):
        """
        Remove the cartesian product of the event mask
        """
        raise "notImplemented"

    #--------------------------------------------------------
    # NOTES INTERFACE
    #--------------------------------------------------------
            
    def CreateNote(self, title, text):
        """

        Add a textual note; return the objref for the note, returns the
        id

        """
        print "create note", title, text

        self.notes.append((0, 0, title, text))
        
        
    def GetNotes(self):
        """
        Get all of the notes, which are tuples of (ts, time,  title, text)
        
        """
        return self.notes
    

