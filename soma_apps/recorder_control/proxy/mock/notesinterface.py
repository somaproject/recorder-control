import gobject

class Note(object):
    def __init__(self, NID):
        self.handle = NID
        self.createts = 0
        self.createtime =0
        self.modifyts = 0
        self.modifytime = 0
        self.name = ""
        self.text = ""
        self.tags = []

class Notes(object):
    def __init__(self):
        self.notes = []
        self.latestNoteHandle = 0
        self.notedict = {}
        
    def CreateNote(self):
        """

        Add a textual note; return the objref for the note, returns the
        id

        note that creating a note does not trigger a signal,
        but sving it does

        """
        self.latestNoteHandle += 1
        
        note = Note(self.latestNoteHandle)
        note.createts = self.ts
        note.createtime = self.time
        
        self.notes.append(note)

        return self.latestNoteHandle
        
    def GetNotes(self, handle):
        """
        Get all note handles
        
        """
        return [note.handle for note in self.notes]
    
    def GetNote(self, handle):
        """
        Get a note
        
        """
        for note in self.notes:
            if note.handle == handle:
                return note
        

    def SetNote(self, handle, name, notetext, taglist):
        for n in self.notes:
            if n.handle == handle:
                note = n
                break

        note.modifytime = self.time
        note.modifyts = self.ts
        note.text = notetext
        note.tags = taglist
        note.name = name
        
        self.emit("NoteChange", handle, len(self.notes))
        

    def DeleteNote(self, handle):
        
        self.emit("NoteChange", handle, len(self.notes))    
        raise "not Implemented", "foo" 


