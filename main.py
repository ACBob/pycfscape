from PyQt5.QtWidgets import qApp, QAction, QMainWindow, QApplication, QWidget, QToolTip, QPushButton, QToolBar, QSplitter, QHBoxLayout
from PyQt5.QtWidgets import QFileDialog, QTextEdit, QDialog, QGridLayout, QGroupBox, QLabel, QFontDialog, QMessageBox, QStyleFactory, QFrame, QListView
from PyQt5.QtGui import QIcon, QFont, QStandardItemModel, QStandardItem
from PyQt5.QtCore import QSize, pyqtSlot, Qt

import sys

#VPK, So we can do our stuff!
import vpk

"""
pak = vpk.open('/media/owner/BigDevelopment/SourceDevelopmentPipeline/steamapps/common/Half-Life 2/hl2/hl2_pak_dir.vpk')

for filepath in pak:
    print(filepath)

reqFile = 'shader_cache.cfg'

pakfile = pak[reqFile]

paklines = pakfile.read()

print(paklines)

outFile = open('./{}'.format(reqFile),'wb')

outFile.write(paklines)

outFile.close() #WE MUST CLOSE the file for python to not shit itself.
"""

class PYCFScape(QMainWindow):

    def __init__(self):
        super().__init__()

        self.VPK = None
        self.VPKDir = ''

        self.Setup()

    def LoadVPK(self,file):
        print('Opening {}'.format(file))
        self.DirectoryModel.clear()

        try:
            self.VPK = vpk.open(file)
        except FileNotFoundError as E:
            self.ErrorBox(str(E),'File Doesn\'t Exist.')
            self.VPK = None
            self.VPKDir = ''
            return
        except ValueError as E:
            self.ErrorBox(str(E))
            self.VPK = None
            self.VPKDir = ''
            return

        self.VPKDir = file

        for filepath in self.VPK:
            #print(filepath)
            item = QStandardItem()
            item.setText(filepath)
            item.setCheckable(True)
            item.setEditable(False)

            self.DirectoryModel.appendRow(item)

    def ExportVPKFiles(self):
        print('Exporting files from {}'.format('VPK'))

        Directories = column(self.DirectoryModel,0)
        print(Directories)
        for Item in Directories:
            #print(Item)
            if Item.checkState():
                print(Item)
                self.ExportFile(Item.text())

        self.LoadVPK(self.VPKDir) #HACK! we currently DELETE everything in the list (have to) and then re-load it.
        

    def ExportFile(self,vpkfilepath,outputdir='./'):
        outFile = open('{}{}'.format(outputdir,vpkfilepath),'wb') #WB - Write, Bytes
        pakLines = self.VPK[vpkfilepath].read()
        outFile.write(pakLines)

    def OpenVPK(self):
        File = self.OpenDialog('Open VPK','Valve Pack Files (*.vpk)')
        if not File == '': self.LoadVPK(File)

    def Setup(self):
        #Winow Information & Such
        self.setWindowTitle('PYCFScape')
        self.setMinimumSize(QSize(750,500))

        #Setup Content Layout & Container
        self.Content = QGroupBox()
        self.ContentLayout = QGridLayout()

        #Setup UI Elements
        self.DirectoryList = QListView()
        self.ContentLayout.addWidget(self.DirectoryList,0,0)

        self.DirectoryModel = QStandardItemModel(self.DirectoryList)
        self.DirectoryList.setModel(self.DirectoryModel)
        self.DirectoryModel.itemChanged.connect(self.on_dir_item_changed)
        
        #Setup Actions
        self.OpenAction = QAction('&Open...',self)
        self.OpenAction.setShortcut('Ctrl+O')
        self.OpenAction.setStatusTip('Open VPK')
        self.OpenAction.triggered.connect(self.OpenVPK)

        self.ExportAction = QAction('&Export...',self)
        self.ExportAction.setShortcut('Ctrl+E')
        self.ExportAction.setStatusTip('Export Chosen Files')
        self.ExportAction.triggered.connect(self.ExportVPKFiles)



        self.Menu = self.menuBar()
        self.FileMenu = self.Menu.addMenu('&File')
        self.FileMenu.addAction(self.OpenAction)
        self.FileMenu.addAction(self.ExportAction)
        
        #Sort out Layout placements and such.
        self.Content.setLayout(self.ContentLayout)
        self.setCentralWidget(self.Content)
        

        #Show ourselves
        self.show()

    def on_dir_item_changed(self,item):

        if not item.checkState():
            return

        print(item)


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


def column(ItemModel, c): #Utility to get row from QStandardItemModel
    tempModel = ItemModel
    return tempModel.takeColumn(c)
    


def main():
    app = QApplication(sys.argv)
    Program = PYCFScape()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
