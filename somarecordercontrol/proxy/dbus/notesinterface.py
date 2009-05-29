import dbus

class Note(object):
    def __init__(self, NID):
        self.handle = NID
        self.createts = 0
        self.createtime =0
        self.modifyts = 0
        self.modifytime = 0
        self.name = ""
        self.text = ""


class NotesInterface(object):
    #--------------------------------------------------------
    # NOTES INTERFACE
    #--------------------------------------------------------

    def __init__(self, dbusobj):
        """
        get and store the interface for the dbus obj
        """

        self.dbusNotes = dbus.Interface(dbusobj,
                                        "soma.recording.Notes")
        
    def CreateNote(self):
        """

        Add a textual note; return note handle

        """
        
    def GetNotes(self):
        """
        Get all of the note handles
        
        """
        return self.notes
    
    def GetNote(self, handle):
        """
        REturn a note object with the indicated handle
        """

    def SetNote(self, handle, name, notetext, taglist):
        """
        sets the note
        """

    def DeleteNote(self, handle):
        """
        Delete the note
        """
