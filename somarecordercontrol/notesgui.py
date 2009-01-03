import gobject
import gtk

class NoteWidget(object):
    """
    A grab bag of GUI components that form a frame for editing a given
    note

    has an "edit mode" in which the various fields are editable

    
    """
    def __init__(self, noteifobj, notehandle, editmode=False):
        self.noteHandle = notehandle
        self.constructWidgets()
        
        self.setEditMode(editmode)
        self.noteifobj = noteifobj
        note = self.noteifobj.GetNote(notehandle)

        self.updateTimeLabel(note)

    def setEditMode(self, mode):
        self.editmode = mode

        self.timelabel.props.visible = True

        if self.editmode == False:
            self.titleentry.props.visible = False
            self.buttonbox.props.visible = False
            self.textview.props.editable = False
            self.textview.props.cursor_visible = False
            self.titlelabel.props.visible = True
            self.titletxtlabel.props.visible = False
            self.tagvaluelabel.props.visible = True
            self.tagentry.props.visible = False
        else:
            self.titleentry.props.visible = True
            self.buttonbox.props.visible = True
            self.textview.props.editable = True
            self.textview.props.cursor_visible =True
            self.titlelabel.props.visible = False
            self.titletxtlabel.props.visible = True
            self.tagvaluelabel.props.visible = False
            self.tagentry.props.visible = True
            
    def updateTimeLabel(self, note):
        timetext = "create ts: %d" % note.createts
        
        if note.modifyts == 0:
            timetext += " modify ts: %d" % note.modifyts
            
        self.timelabel.set_label(timetext)

    def updateData(self):
        """
        Update all the widgets
        does not impact visibility  /edit mode
        """
        note = self.noteifobj.GetNote(self.noteHandle)
        self.titleentry.set_text(note.name)
        self.titlelabel.set_label("<b><b>%s</b></b>" % note.name)

        # //
        formatstr = ""
        for s in note.tags:
            formatstr += s + " "
        formatstr = formatstr[:(len(formatstr)-1)]
                    
        self.tagentry.set_text(formatstr)
        self.tagvaluelabel.set_label(formatstr)
                
    def constructWidgets(self):
        
        self.frame = gtk.Frame()
        self.titleentry = gtk.Entry()
        self.titlelabel = gtk.Label()
        self.titlelabel.props.use_markup = True
        
        self.titlehbox = gtk.HBox()
        self.titletxtlabel = gtk.Label("Title:")
        self.titlehbox.pack_start(self.titletxtlabel)
        self.titlehbox.pack_start(self.titleentry)
        self.titlehbox.pack_start(self.titlelabel)

        self.timelabel = gtk.Label()
        
        self.titlehbox.pack_start(self.timelabel)
        
        self.frame.set_label_widget(self.titlehbox)
        
        self.textbuffer = gtk.TextBuffer(table=None)
        self.textview = gtk.TextView(self.textbuffer)
        self.textview.set_wrap_mode(gtk.WRAP_WORD)
        self.vbox = gtk.VBox()
        self.vbox.pack_start(self.textview)

        self.taghbox = gtk.HBox()
        self.taglabel = gtk.Label("<b>Tags:</b>")
        self.taglabel.props.use_markup = True
        
        self.tagentry = gtk.Entry()
        self.tagvaluelabel = gtk.Label()
        
        self.taghbox.pack_start(self.taglabel, False)
        self.taghbox.pack_start(self.tagentry)
        self.taghbox.pack_start(self.tagvaluelabel)

        self.vbox.pack_start(self.taghbox, False)
        self.buttonbox = gtk.HButtonBox()
        self.buttonbox.set_layout(gtk.BUTTONBOX_END)

        self.savebutton = gtk.Button(label="Save", stock=gtk.STOCK_SAVE)
        self.savebutton.connect('clicked', self.noteSave)
        
        self.cancelbutton = gtk.Button(label="Cancel", stock=gtk.STOCK_CANCEL)
        self.cancelbutton.connect('clicked', self.noteCancel)
        
        self.buttonbox.add(self.savebutton)
        self.buttonbox.add(self.cancelbutton)
        self.vbox.pack_start(self.buttonbox, False)

        self.frame.add(self.vbox)
        self.frame.show_all()


        self.setEditMode(False)
        
    def noteSave(self, widget):
        """
        save the current note state
        """

        note_title = self.titleentry.get_text()
        note_handle = self.noteHandle
        note_text = self.textbuffer.props.text
        note_tags_text = self.tagentry.get_text()

        # construct the tag array
        taglist = []
        for tstr in note_tags_text.split(" "):
            taglist.append(tstr)
        
        
        
        self.noteifobj.SetNote(note_handle, note_title, note_text,
                               taglist)
        
        self.setEditMode(False)
        
    def noteCancel(self, widget):
        """
        Cancel -- not quite clear what we should be doing
        
        """
        # how to tell if we're cancelling the add?
        
        self.setEditMode(False)
        
        
class NotesGUI(object):

    def __init__(self, notesvbox, addbutton, noteIFObj):
        """
        NoteIFobj is an object implementing the Notes interface

        It is possible for two people to edit, update, and save the same
        note at once. bThis is why we want
        to eventually have a "watch" and "not watch" mode
        
        """
        
        self.vboxNotes = notesvbox
        self.buttonAddNote = addbutton
        self.noteIFObj = noteIFObj
        self.buttonAddNote.connect('clicked', self.on_buttonAddNote_clicked)
        self.noteIFObj.connect("notechange", self.noteChangeCallback)
        
        self.vboxNotes.show_all()

        self.notes = {}
        
    def noteChangeCallback(self, widget,  notehandle, notecnt):
        """
        This is where new notes come from...
        
        """

        if notehandle in self.notes:

            self.notes[notehandle].updateData()
        else:
            notewidget = NoteWidget(self.noteIFObj, notehandle)
        
            self.vboxNotes.pack_start(notewidget.frame)
            self.notes[notehandle] = notewidget
        
    def on_buttonAddNote_clicked(self, widget):
        """
        Clicked when the "Add note" button is pressed

        Add note should set things up such that
          1. you can't add another note until this one is
             cancelled or saved
          
          2. when you save it, it is pushed ot the server and then we
        """
        notehandle = self.noteIFObj.CreateNote()

        notewidget = NoteWidget(self.noteIFObj, notehandle)
        
        self.vboxNotes.pack_start(notewidget.frame)
        self.notes[notehandle] = notewidget
        notewidget.setEditMode(True)
    
    def setNotesPending(self):
        """
        called to make the notes pending

        """
        self.vboxNotes.hide()

        # set the thing to be pending
        
        
    def updateNotes(self):
        """
        called to update the list of notes, ideally
        upon instantiation
        
        """

        for i in self.vboxNotes:
            self.vboxNotes.remove(i)

        self.notes.clear()
        
        for notehandle  in self.noteIFObj.GetNotes():
            notewidget = NoteWidget(self.noteIFObj, notehandle)
            self.vboxNotes.pack_start(notewidget.frame)
            self.notes[notehandle] = notewidget
        
            
