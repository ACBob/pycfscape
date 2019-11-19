"""

The Giant Penis License (GPL)
Copyright (c) 2019 ACBob

                ▄▄██▄██▄▄
              ▄█    █    █▄
             ▄█           █▄
             █             █
            █               █
            █               █
            █               █
            █               █
             █▄     █     ▄█
              █    ▄▄▄    █
              █           █
              █           █
              █           █
              █           █
              █           █
              █           █
              █           █
              █           █
              █           █
              █           █
              █           █
              █           █
        ▄████▄█           █▄████▄
      ▄█                         █▄
     █                             █
    █                               █
    █                               █
    █                               █
    █             ▄▄█▄▄             █
     █           █     █           █
      █▄       ▄█       █▄       ▄█
        █▄▄▄▄▄█           █▄▄▄▄▄█

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from PyQt5.QtWidgets import qApp, QAction, QMainWindow, QApplication, QWidget, QToolTip, QPushButton, QToolBar, QSplitter, QHBoxLayout
from PyQt5.QtWidgets import QFileDialog, QTextEdit, QDialog, QGridLayout, QGroupBox, QLabel, QFontDialog, QMessageBox, QStyleFactory, QFrame, QTreeView
from PyQt5.QtGui import QIcon, QFont, QStandardItemModel, QStandardItem
from PyQt5.QtCore import QSize, pyqtSlot, Qt

import sys
import os

#VPK, So we can do our stuff!
import vpk

import pathtodir #Stackoverflow helped me. This time *I* asked the question.
import json

import options

class VPKItem(QStandardItem):

    def __init__(self,info,ItemType=''):
        super().__init__()
        self.PathInfo = info
        self.VPKItemType = ItemType
        self.VPKChildren = []

    def setType(self,Type):
        self.VPKItemType = Type

    def appendRow(self,thing):
        super().appendRow(thing)
        self.VPKChildren.append(thing)

class PYCFScape(QMainWindow):

    def __init__(self):
        super().__init__()

        self.VPK = None
        self.VPKDir = ''
        self.ExportItems = []

        self.OptionsMenu = options.PYCFScapeOptionsWindow()

        self.Setup()

    def LoadVPK(self,file):
        print('Opening {}'.format(file))
        self.DirectoryModel.clear()
        self.ExportItems = []
        self.VPK = None

        try:
            self.VPK = vpk.open(file)
        except FileNotFoundError as E:
            self.ErrorBox(str(E),'File Doesn\'t Exist.')
            return
        except ValueError as E:
            self.ErrorBox(str(E))
            return

        self.VPKDir = file

        self.HandleVPK(self.VPK)

    def ExportVPKFiles(self):
        print('Exporting files from {}'.format('VPK'))

        for Item in self.ExportItems:
            self.ExportFile(Item.PathInfo)

    def ExportFile(self,file):
        outputdir = self.OptionsMenu.Options['config']['path']
        if not os.path.isdir('{}{}'.format(outputdir,'/'.join(file.split('/')[:-1]))):
            print("path {} doesn't exist.".format(file))
            os.makedirs('{}{}'.format(outputdir,'/'.join(file.split('/')[:-1])))
        print(file)
        outFile = open('{}{}'.format(outputdir,file[1:]),'wb') #WB - Write, Bytes
        pakLines = self.VPK.get_file(file[1:]).read()
        outFile.write(pakLines)
        outFile.close()

    def OpenVPK(self):
        File = self.OpenDialog('Open VPK','Valve Pack Files (*.vpk)')
        if not File == '': self.LoadVPK(File)

    def Setup(self):
        #Winow Information & Such
        self.setWindowTitle('PYCFScape')
        self.setMinimumSize(QSize(750,500))
        self.setWindowIcon(QIcon('./res/Icon64.ico'))

        #Setup Content Layout & Container
        self.Content = QGroupBox()
        self.ContentLayout = QGridLayout()

        #Setup UI Elements
        self.DirectoryList = QTreeView()
        self.DirectoryList.setAlternatingRowColors(True)

        self.ContentLayout.addWidget(self.DirectoryList,0,0)

        self.DirectoryModel = QStandardItemModel(self.DirectoryList)
        self.DirectoryList.setModel(self.DirectoryModel)
        
        #Setup Actions
        self.OpenAction = QAction('&Open...',self)
        self.OpenAction.setShortcut('Ctrl+O')
        self.OpenAction.setStatusTip('Open VPK')
        self.OpenAction.triggered.connect(self.OpenVPK)

        self.ExportAction = QAction('&Export...',self)
        self.ExportAction.setShortcut('Ctrl+E')
        self.ExportAction.setStatusTip('Export Chosen Files')
        self.ExportAction.triggered.connect(self.ExportVPKFiles)

        self.OptionsAction = QAction("&Config")
        self.OptionsAction.setStatusTip('Change some things')
        self.OptionsAction.triggered.connect(self.OptionsMenu.show)


        self.Menu = self.menuBar()
        self.FileMenu = self.Menu.addMenu('&File')
        self.FileMenu.addAction(self.OpenAction)
        self.FileMenu.addAction(self.ExportAction)
        self.EditMenu = self.Menu.addMenu('&Edit')
        self.EditMenu.addAction(self.OptionsAction)
        
        #Sort out Layout placements and such.
        self.Content.setLayout(self.ContentLayout)
        self.setCentralWidget(self.Content)


        self.DirectoryModel.itemChanged.connect(self.VPKItemClicked)

        #Show ourselves
        self.show()

    def HandleVPK(self,paths):
        dictPaths = pathtodir.get_path_dict(paths)
        self.DirectoryMagic(dictPaths)

    def VPKItemClicked(self,item):
        #print(item.parent()) 
        if item.VPKItemType == 'File':
            if item.checkState():
                self.ExportItems.append(item)
            else:
                self.ExportItems.remove(item)
        elif item.VPKItemType == 'Dir':
            if item.checkState():
                for Item in item.VPKChildren:
                    Item.setCheckState(2)
                    self.ExportItems.append(Item)
                item.setCheckState(2)
            else:
                
                for Item in item.VPKChildren:
                    Item.setCheckState(0)
                    self.ExportItems.remove(Item)
                

    def DirectoryMagic(self,path,parent=None,wPath=''):
        #A Magic function that uses R E C U R S I O N!

        for thing in path:

            wwPath = wPath+'/{}'.format(thing)

            #Create our Item variable
            thingItem = VPKItem(wwPath)
            thingItem.setText(thing)

            thingItem.setEditable(False)
            thingItem.setIcon(QIcon.fromTheme('document'))

            thingItem.setCheckable(True)
            
            if type(path[thing]) == dict: #If it's a dictionary, it's a folder.
                thingItem.setIcon(QIcon.fromTheme('folder-new'))
                self.DirectoryMagic(path[thing],thingItem,wwPath)
                thingItem.setType('Dir')
            else:
                thingItem.setType('File')
            if not parent: self.DirectoryModel.appendRow(thingItem)
            else: parent.appendRow(thingItem)

    def AddFile(self,filePath):
        path, file = os.path.split(filePath)
        pathFolders = path.split('/')

        Magic(filePath)

    def ErrorBox(self,text="Message..",title="Error"):
        box = QMessageBox()
        box.setIcon(QMessageBox.Critical)
        box.setText(text)
        box.setWindowTitle(title)
        box.setStandardButtons(QMessageBox.Ok)

        return box.exec()
    
    def OpenDialog(self,title="Open File",files="All Files (*)"):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, title, "", files, options=options)

        return filename

def main():
    app = QApplication(sys.argv)
    Program = PYCFScape()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
