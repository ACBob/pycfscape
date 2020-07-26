
import vpk

import wx
import sys
import datetime #Used for the log

#Flip this to use a faked VPK structure / Actually work as program
DEBUG = True

#TODO: Move to seperate file?
class StdoutAbsorber(object):
    def __init__(self):
        self.stdout = sys.stdout
        self.content = []
        #TODO: Log to file?

    def write(self, message):
        self.content.append(message)
        self.stdout.write(message)

class PYCFScapeFrame(wx.Frame):

    def __init__(self):
        super().__init__(parent=None, title="PYCFScape")

        self.split = wx.SplitterWindow(self)

        self.vpk_tree = wx.TreeCtrl(self.split)
        self.logger = wx.TextCtrl(self.split, style=wx.TE_MULTILINE|wx.TE_READONLY)

        self.split.SplitHorizontally(self.vpk_tree, self.logger)

        if DEBUG:
            self.log("Debug mode enabled.")
            self.log("As a result, creating test items...")

            #TODO: Not sure if this actually helps us test anything beyond trying out Wx...

            self.vpk_root = self.vpk_tree.AddRoot("NotAReal.vpk")
            self.testfolder_a = self.vpk_tree.AppendItem(self.vpk_root,"TestFolder_A")
            self.testfolder_a_foo = self.vpk_tree.AppendItem(self.testfolder_a,"foo.txt")
            self.testfolder_a_bar = self.vpk_tree.AppendItem(self.testfolder_a,"bar.txt")
            self.baz = self.vpk_tree.AppendItem(self.vpk_root,"baz.txt")
            self.qux = self.vpk_tree.AppendItem(self.vpk_root,"qux.txt")

            self.log("Test Items Created")

        #We're done setting up, Show!
        self.Show()

    def log(self, message):
        message = str(datetime.datetime.now().time()) + ") " + message
        print(message)
        self.logger.SetValue('\n'.join(sys.stdout.content))

if __name__ == "__main__":
    sys.stdout = StdoutAbsorber()

    app = wx.App()
    root_frame = PYCFScapeFrame()
    app.MainLoop()
