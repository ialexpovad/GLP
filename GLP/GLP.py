author = 'Alex Povod'
version = '0.0.1'

# Importing standart and mathematical modules
## Standart
import sys
import time
import datetime
import typing
import os
import getpass

## Mathematical 
import sympy
import numpy
import matplotlib

# Importing PyQt mudules
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
# from PyQt5 import Q

def App() -> QApplication:
    return QApplication.instance()

class GLPMainApp(QApplication):
    def __init__(self, argv: typing.List[str]) -> None:
        super(GLPMainApp, self).__init__(argv)
        self.setOrganizationName = 'Alex Povod'
        self.setOrganizationDomain = 'https://github.com/ialexpovod/GLP'
        
        # Greeting user in Tab Widget 
        try:
            message = "Welcome " + getpass.getuser()
        except: # TODO: adding exception for no-user
            message = "Welcome"

        self.moduleVersion = "Python %s\n GLP %s " % (" %d.%d" % (sys.version_info.major, sys.version_info.minor),
                                                        version
                                                        )
            
class GLPWindow(QMainWindow):
    def __init__(self, parent: typing.Optional[QWidget] = None, flags: typing.Union[QtCore.Qt.WindowFlags, QtCore.Qt.WindowType] = None) -> None:
        super(GLPWindow, self).__init__(parent)
        self.resize(800, 600)