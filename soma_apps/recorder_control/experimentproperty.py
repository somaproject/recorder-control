import sys
import os
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import pdb
from proxy.mock.epoch import Epoch
from treemodel import RecorderTreeModel
import datatab
import notesgui
import status


class ExperimentProperty(object):
    """
    The property interface for an experiment
    """

    def __init__(self, expobj):
        self.experiment = expobj

        gladefilename = "experiment-property.glade"
        gladefile = os.path.dirname(__file__) + "/" + gladefilename

        windowname = "notebookExperimentProperty"
        self.wTree = gtk.glade.XML(gladefile, windowname)
        self.wTree.signal_autoconnect(self)
        
        self.prop = self.wTree.get_widget('notebookExperimentProperty')

        
        #self.updateNotes()
        self.experimentLabel = self.wTree.get_widget("labelExperimentFilename")
        self.experimentLabel.props.label = "<big><big><big>%s</big></big></big>" % self.experiment.GetName()
        
        self.dbusLabel = self.wTree.get_widget("labelDBUSObjectPath")
        self.dbusLabel.set_label(expobj.getPath())

        self.buttonAddNote = self.wTree.get_widget("buttonAddNote")
        self.vboxNotes = self.wTree.get_widget('vboxExperimentNotes')

        self.notesgui = notesgui.NotesGUI(self.vboxNotes,
                                          self.buttonAddNote,
                                          self.experiment)
                                          
        
