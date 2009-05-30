
import sys
import os
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import gobject
import pdb
from proxy.mock.epoch import Epoch
from proxy.mock.manager import Manager
from treemodel import RecorderTreeModel
import datatab
import notesgui
import status
import util

class EpochProperty(object):
    """
    This is the class responsible for managing the epoch properties,
    recording, etc. 

    """
    
    def __init__(self, epochobject):
        self.epoch = epochobject
        gladefilename = "epoch-property.glade"
        gladefile = os.path.dirname(__file__) + "/" + gladefilename
        windowname = "notebookEpochProperty"
        self.wTree = gtk.glade.XML(gladefile, windowname)   
        self.prop = self.wTree.get_widget('notebookEpochProperty')

        self.wTree.signal_autoconnect(self)
        self.setupSessions()
        #signaldic = {"on_toggleRecord_toggled",
        self.epoch.sessionSignalCallback = self.updateSessions

        self.datatab = datatab.EpochDataTab(self.wTree.get_widget("treeviewDataSources"),
                                            self.epoch)
        
        self.buttonAddNote = self.wTree.get_widget("buttonAddNote")
        self.vboxNotes = self.wTree.get_widget('vboxExperimentNotes')

        self.dbusLabel = self.wTree.get_widget("labelDBUSObjectPath")
        self.dbusLabel.set_label(self.epoch.getPath())

        self.notesgui = notesgui.NotesGUI(self.vboxNotes,
                                          self.buttonAddNote,
                                          self.epoch)
        
        self.epoch.connect("renamed", self.nameChanged)

        self.epoch.connect("recordingstate", self.recordingStateChanged)

        self.hasRecorded = False
        self.updateName()
        self.timeoutSourceID = None
        
    def on_notebookEpochProperty_switch_page(self, notebook, page, pagenum):
        print "SWITCH PAGE", pagenum
        if pagenum == 1:
            if self.hasRecorded:
                status.Message("Cannot modify data sources once you have recorded into an epoch")
                

    def updateName(self):
        name = self.epoch.GetName()
        label = self.wTree.get_widget("labelEpochName")
        label.set_label("<big><big><big><big>%s</big></big></big></big>" % name)
        
    def nameChanged(self, widget, newname):
        self.updateName()

    def populate(self):
        """
        Fill out the widgets with the relevant values
        """
    def recordingStateChanged(self, widget, isRecording):
        """
        GUI updates for changes in recording state
        """
        
        if isRecording:
            self.wTree.get_widget("buttonRecord").props.sensitive = False
            self.wTree.get_widget("buttonStop").props.sensitive = True

            if self.timeoutSourceID != None:
                gobject.source_remove(self.timeoutSourceID)
            self.timeoutSourceID = gobject.timeout_add(1000, self.updateSessions)
        else:
            self.wTree.get_widget("buttonRecord").props.sensitive = True
            self.wTree.get_widget("buttonStop").props.sensitive = False

            if self.timeoutSourceID != None:
                gobject.source_remove(self.timeoutSourceID)
            self.timeoutSourceID = None

        
    def setupSessions(self):
        self.sessionstore = gtk.ListStore(int, int, str, int, str)
        
                
        treeview = self.wTree.get_widget("treeviewSessions")
        treeview.get_selection().set_mode(gtk.SELECTION_NONE)
        self.treeviewSessions = treeview
        treeview.set_model(self.sessionstore)

        # Session col
        sessioncol = gtk.TreeViewColumn("Session")

        cell = gtk.CellRendererText()
        sessioncol.pack_start(cell, True)
        sessioncol.add_attribute(cell, "text", 0)

        treeview.append_column(sessioncol)

        # Start TS col
        starttscol = gtk.TreeViewColumn("Start Timestamp")

        cell = gtk.CellRendererText()
        starttscol.pack_start(cell, True)
        starttscol.add_attribute(cell, "text", 1)

        treeview.append_column(starttscol)

        # Start  col
        starttimecol = gtk.TreeViewColumn("Start Time")

        cell = gtk.CellRendererText()
        starttimecol.pack_start(cell, True)
        starttimecol.add_attribute(cell, "text", 2)

        treeview.append_column(starttimecol)

        # Stop TS col
        stoptscol = gtk.TreeViewColumn("Stop Timestamp")

        cell = gtk.CellRendererText()
        stoptscol.pack_start(cell, True)
        stoptscol.add_attribute(cell, "text", 3)

        treeview.append_column(stoptscol)

        # Stop  col
        stoptimecol = gtk.TreeViewColumn("Stop Time")

        cell = gtk.CellRendererText()
        stoptimecol.pack_start(cell, True)
        stoptimecol.add_attribute(cell, "text", 4)

        treeview.append_column(stoptimecol)

        
        
        self.updateSessions()

    def updateSessions(self):
        self.sessionstore.clear()
        pos = 0
        for s in self.epoch.GetSessions():
            # convert session args to string
            l = list(s)
            l[1] = util.timestr(l[1])
            l[3] = util.timestr(l[3])
            l.insert(0, pos)
            pos += 1
            self.sessionstore.append(l)
        return True

    def on_buttonRecord_clicked(self, widget):
        # performs no gui manipulation, we wait
        # for the signal to do that

        self.epoch.StartRecording()

    def on_buttonStop_clicked(self, widget):
        # no gui manipulation
        self.epoch.StopRecording()
