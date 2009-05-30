import gobject
import time
from notesinterface import Note, Notes

class Session(object):

    def __init__(self, startts, starttime):
        self.startts = startts
        self.starttime = starttime
        self.stopts =  startts
        self.stoptime = starttime
        
    def toTuple(self):
        return (self.startts, self.starttime,
                self.stopts, self.stoptime)

class Epoch(gobject.GObject, Notes):
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

                     # not entirely happy with tihs signal -- first argument
                     # is the specific handle of the note that might have
                     # changed, second is total number of notes
                     'notechange': (gobject.SIGNAL_RUN_FIRST,
                                        gobject.TYPE_NONE,
                                        (gobject.TYPE_INT, gobject.TYPE_INT))
                     }

    def __init__(self, parent, name):
        gobject.GObject.__init__(self)
        Notes.__init__(self)
        
        self.name = name
        self.parent = parent
        self.timer_id = gobject.timeout_add(500, self.updateClock)
        self.ts = 0
        self.time = 0
        self.sessions = []
        self.recording = False

        self.sessionSignalCallback = None

        self.datasinks = set()
        self.datasinknames = {}
        
        for i in xrange(64):
           self.datasinknames[i] = "Source%0.2d" % i 
           
    def GetName(self):
        """
        Return the epoch name
        """
        return self.name

    def GetRecordingState(self):
        return self.recording

    def getPath(self):
        return "Mock Object:/no-path"

    def StartRecording(self):
        """
        begin recording for this epoch
        Can steal recording from another epoch
        
        """
        print "Epoch", self.name, "starting recording"
        self.sessions.append(Session(self.ts, time.time()))
        self.recording = True
        # This is a total hack
        if self.parent.recordingEpoch != self and self.parent.recordingEpoch != None:
            # we are currently recording into another epoch, so stop it!
            self.parent.recordingEpoch.StopRecording()

        self.parent.recordingEpoch = self
        self.parent.state = True
            
        self.emit("recordingstate", True)

    def StopRecording(self):
        """
        Stop the recording
        """
        print "Epoch", self.name, "stopping recording"
        self.recording = False
        if self.sessionSignalCallback != None:
            self.sessionSignalCallback()

        self.parent.recordingEpoch = None
        
        self.emit("recordingstate", False)
        

    
    def setName(self, name):
        self.name = name
        self.emit("renamed", name)
        


    def EnableDataSink(self, src, typ):
        """
        src is the src #
        type is the type
        """

        self.datasinks.add((src, typ))
        
        self.emit("sinkchange", src)


    def DisableDataSink(self, src, typ):
        """
        """
        self.datasinks.remove((src, typ))
        self.emit("sinkchange", src)
        

    def GetDataSinks(self):
        """
        Returns a list of string tuples
        """
        return list(self.datasinks)
        

    def GetDataSink(self, src):
        """
        Returns a list of ints, the enabled sinks for this data
        type
        
        """
        selsinks = [x[1] for x in self.datasinks if x[0] ==src]
        
        return selsinks
        

    def SetDataName(self, src, name):
        """

        """
        self.datasinknames[src] = name
        self.emit("sinkchange", src)


    def GetDataName(self, src):
        """

        """
        return self.datasinknames[src]
    

    def GetSinkSessionStats(self, src, typ, sessions):
        """
        The epochs stats... not entirely clear what these are yet! 

        """
        
    
    def GetSessions(self):
        """
        Get epoch recording sessions
        """

        # convert the sessions
        
        return [s.toTuple() for s in self.sessions]
    

    def AddEventRXMask(self, enableEvent, cmdlist):
        """
        Recive the cartesian product of sources and commands
        
        """

    def GetEventRXMask(self, source, cmdlist):
        """
        returns a list of all the events that we receive

        """
        
    def RemoveEventRXMask(self, source, cmdlist):
        """
        Remove the cartesian product of the event mask
        """
        
    def updateClock(self):
        self.ts += 25000
        if self.recording:
            self.sessions[-1].stoptime = time.time()
            self.sessions[-1].stopts= self.ts

        return True


