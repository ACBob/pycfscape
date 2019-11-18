#Both a license for the file AND the about text.
About="""

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

from PyQt5.QtWidgets import qApp, QAction, QWidget, QApplication, QMainWindow, QTabWidget, QLineEdit, QGroupBox, QGridLayout, QLabel, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

import toml
import sys

class PYCFScapeOptionsWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.OptionsFile = open('./options.toml','r+')
        self.Options = toml.loads(self.OptionsFile.read())

        print(self.Options)

        self.Setup()
    def Setup(self):
        #Winow Information & Such
        self.setWindowTitle('PYCFScape')
        self.setMinimumSize(QSize(500,250))
        self.setWindowIcon(QIcon('./res/Icon64.ico'))

        #Setup Content Layout & Container
        self.GenericTabContentLayout = QGridLayout()
        self.AboutTabContentLayout = QGridLayout()

        #Setup Tabs
        self.Tabs = QTabWidget()
        self.GenericTab = QWidget()
        self.AboutTab = QWidget()
        self.Tabs.addTab(self.GenericTab,'Generic Options')
        self.Tabs.addTab(self.AboutTab,'About')
        
        #GenericTab Content
        self.PathEdit = QLineEdit(self.GenericTab)
        self.PathEdit.setText(self.Options['config']['path'])
        self.PathEditLabel = QLabel('Export Path')
        self.PathEditLabel.setAlignment(Qt.AlignLeft)

        self.PathEditSetButton = QPushButton('Set Path')
        self.PathEditSetButton.clicked.connect(self.SetPath)

        self.ApplyAndSaveButton = QPushButton('Apply and Save')
        self.ApplyAndSaveButton.clicked.connect(self.SaveOptions)

        #AboutTab Content
        self.AboutLabel = QLabel(About)
        self.AboutLabel.setAlignment(Qt.AlignLeft)

        #Place Everything
        self.GenericTabContentLayout.addWidget(self.PathEdit,0,1)
        self.GenericTabContentLayout.addWidget(self.PathEditLabel,0,0)
        self.GenericTabContentLayout.addWidget(self.PathEditSetButton,0,2)
        self.GenericTabContentLayout.addWidget(self.ApplyAndSaveButton,3,0)

        self.AboutTabContentLayout.addWidget(self.AboutLabel,0,0)

        #Sort out Layout placements and such.
        self.GenericTab.setLayout(self.GenericTabContentLayout)
        self.setCentralWidget(self.Tabs)

    def SetPath(self):
        self.Options['config']['path'] = self.PathEdit.text()
        print(self.Options)

    def SaveOptions(self):
        self.OptionsFile.seek(0)
        self.OptionsFile.write(toml.dumps(self.Options))
        self.OptionsFile.truncate()

if __name__ == '__main__':
    print("Debuggin Options")
    app = QApplication(sys.argv)
    Program = PYCFScapeOptionsWindow()
    Program.show()
    sys.exit(app.exec_())
