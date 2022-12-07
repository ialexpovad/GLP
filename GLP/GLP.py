author = 'Alex Povod'
version = '0.0.1'

# Importing standart and mathematical modules
## Standart
import sys
import importlib
import typing
import os
import getpass
import re
import datetime

## Mathematical 
import sympy
import matplotlib
import numpy

# Importing PyQt mudules
from PyQt5.QtWidgets import (   QApplication, 
                                QMainWindow, 
                                QWidget, 
                                QStyle, 
                                QToolTip, 
                                QMenuBar,
                                QGridLayout,
                                QToolButton,
                                QSizePolicy
                                )
from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QTextCharFormat

# Importing theme module
try:
    from GLP import theme
except ModuleNotFoundError:
    import GLP


common_exceptions = (
                        TypeError , 
                        SyntaxError , 
                        sympy.SympifyError , 
                        sympy.parsing.sympy_parser.TokenError , 
                        re.error ,  
                        AttributeError , 
                        ValueError , 
                        NotImplementedError , 
                        Exception , 
                        RuntimeError , 
                        ImportError
                        )

def ExceptionOutput(exc_info = None, extraInfo = True):
    """
    Console output for exceptions\n
    Use in `except:`: Error = ExceptionOutput(sys.exc_info())\n
    Prints Time, ExceptionType, Filename+Line and (if extraInfo in not False) the exception description to the console\n
    Returns a string
    """
    try:
        if False:
            if exc_info == None:
                exc_info = True
            return NC(exc=exc_info)
        else:
            print(cTimeSStr(),":")
            if exc_info==None:
                exc_type, exc_obj, exc_tb = sys.exc_info()
            else:
                exc_type, exc_obj, exc_tb = exc_info
            fName = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            if extraInfo:
                print(exc_type, " in", fName, " line", exc_tb.tb_lineno ,": ", exc_obj)
            else:
                print(exc_type, " in", fName, " line", exc_tb.tb_lineno)
            return str(exc_type)+": "+str(exc_obj)
    except common_exceptions as inst:
        print("An exception occurred while trying to print an exception!")
        print(inst)


def cTimeSStr():
    """
    Returns the time (including seconds) as a string: %H:%M:%S
    """
    return str(datetime.datetime.now().strftime('%H:%M:%S'))


def App() -> QApplication:
    return QApplication.instance()


class GLPMainApp(QApplication):
    signalColourChanged = QtCore.pyqtSignal()
    def __init__(self, argv: typing.List[str]) -> None:
        super(GLPMainApp, self).__init__(argv)
        self.setOrganizationName = 'Alex Povod'
        self.setOrganizationDomain = 'https://github.com/ialexpovod/GLP'
        # self.setStyle("Windows")

        # Bar widget on MacOS
        self.setAttribute(QtCore.Qt.AA_DontUseNativeMenuBar) 
        # Set standart icon window
        self.setWindowIcon(QApplication.style().standardIcon(QStyle.SP_TitleBarContextHelpButton))

        # TODO: check whether the advanced mode is active
        # sys.excepthook =



        # Greeting user in Tab Widget 
        try:
            message = "Welcome " + getpass.getuser()
        except: # TODO: adding exception for no-user
            message = "Welcome"

        self.moduleVersion = "Python %s\n GLP %s " % (" %d.%d" % (sys.version_info.major, sys.version_info.minor),
                                                        version
                                                        )
        # Initilize font by default
        self.initFont()

        self.AppPalettes = {}
        self.colourSheme()

    def setMainWindow(self, win):
        self.MainWindow = win

    def initFont(self):
        self.defFont = QtGui.QFont()
        self.defFont.setFamily("Helvetica [Cronyx]")
        self.defFont.setPointSize(9)
        self.setFont(self.defFont)
    
    def colourSheme(self, colour = "Light"):
        '''
        This is method of class `GLPMainApp` applied a colour scheme, user-defined.
        # TODO: set description method...
        '''
        try:
            # TODO: Add except notinification
            try:
                importlib.reload(theme)
            except:
                pass    
            try:    
                spec = importlib.util.spec_from_file_location(  "CustomColourPalettes", 
                                                                os.path.join(self.GPLSettingsPath,
                                                                "CustomColourPalettes.py")
                                                                )
                CustomColours = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(CustomColours)
            except:
                # TODO: set Exception!
                pass    
            try:
                self._reColourSheme(*theme.Colours[colour]())
            except:
                try:
                    self._reColourSheme(*CustomColours.Colours[colour]())
                except:
                    self._reColourSheme(*self.AppPalettes[colour]())
        except:
            pass
    def _reColourSheme(self, Palette1, Palette2, Palette3, PenColours, NotificationColours, MiscColours):
        '''
        This is method is called by 'colourSheme' to apply the colour palette.
        '''
        self.Palette = Palette1 #TODO: Remove self.Palette
        self.Palette1 = Palette1
        self.Palette2 = Palette2
        self.Palette3 = Palette3
        self.PenColours = colourDict()
        self.PenColours.copyFromDict(PenColours)
        self.NotificationColours = colourDict()
        self.NotificationColours.copyFromDict(NotificationColours)
        self.MiscColours = colourDict()
        self.MiscColours.copyFromDict(MiscColours)
        Colour = self.Palette1.color(QtGui.QPalette.Active,QtGui.QPalette.Base)
        self.BG_Colour = (Colour.red()/255,Colour.green()/255,Colour.blue()/255)
        Colour = self.Palette1.color(QtGui.QPalette.Active,QtGui.QPalette.Text)
        self.TextColour = (Colour.red()/255,Colour.green()/255,Colour.blue()/255)
        self.colour_Pack = (self.Palette , self.BG_Colour , self.TextColour)        #TODO: remove variable colour...
        self.setPalette(self.Palette)
        QToolTip.setPalette(self.Palette)
        self._update_NCF() # TODO
        
        c=[]
        for v in self.PenColours.values():
            c.append(v.color().name(0))
        self.mplCycler = matplotlib.cycler(color=c) 
        matplotlib.rcParams['axes.prop_cycle'] = self.mplCycler

        for w in self.topLevelWidgets():
            for i in w.findChildren(MplWidget):
                i.SetColour(self.BG_Colour, self.TextColour, self.mplCycler)
            
        # self.r_Recolour()
        self.S_ColourChanged.emit()

class colourDict(dict):
    """
    This class is used to store the special colours.
    It is used to ensure that a missing colour does not 
    cause a crash by returning the "Blue" colour.
    """
    def __getitem__(self, key):
        try:
            Colour = dict.__getitem__(self, key)
        except:
            for v in self.values():
                Colour = v
                break
        return Colour
    
    def copyFromDict(self, dict):
        for i,v in dict.items():
            self[i] = v

class MplWidget(QWidget):
    def __init__(self, parent=None):
        super(MplWidget, self).__init__(parent)
        self.background_Colour = QApplication.instance().BG_Colour
        self.TextColour = QApplication.instance().TextColour
        self.Cycler = QApplication.instance().mplCycler

    def SetColour(self,BG = None, FG = None, Cycler = None):
        if BG!=None:
            self.background_Colour = BG
        if FG!=None:
            self.TextColour = FG
        if type(Cycler)!=None:
            self.Cycler = Cycler
        self.HexcolourText = '#%02x%02x%02x' % (int(self.TextColour[0]*255),int(self.TextColour[1]*255),int(self.TextColour[2]*255))
        try:
            self.canvas.fig.set_facecolor(self.background_Colour)
            self.canvas.fig.set_edgecolor(self.background_Colour)
            self.canvas.ax.set_facecolor(self.background_Colour)
            self.canvas.ax.set_prop_cycle(self.Cycler)
        except common_exceptions:
            ExceptionOutput(sys.exc_info())
        try:
            self.canvas.draw()
        except common_exceptions:
            ExceptionOutput(sys.exc_info())

class GLPWindow(QMainWindow):
    def __init__(   self, parent: typing.Optional[QWidget] = None, flags: typing.Union[QtCore.Qt.WindowFlags, QtCore.Qt.WindowType] = None,
                    _include_QTopBar = True, _init_QTopBar = True, _include_QStatusBar=True, _fullScreen_HideBars = False
                ) -> None:
        super(GLPWindow, self).__init__(parent)
        # self.resize(600, 400)
        self._include_QTopBar = _include_QTopBar
        if _include_QTopBar:
            self._menuBar = QCustomMenuBar(self)
            self.setMenuBar(self._menuBar)
            self._topBar = QCustomTopBarWidget(self, _init_QTopBar)
            self._menuBar.setCornerWidget(self._topBar)
            self._menuBar.setContentsMargins(0,0,0,0)

            # TODO: set top bar on menu bar ...


class QCustomMenuBar(QMenuBar):
    '''
    Custom QMenuBar for this library.
    '''
    def __init__(self, parent = None) -> None:
        super(QCustomMenuBar, self).__init__(parent)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # applies cursor 'Hand'

class QCustomTopBarWidget(QWidget):
    '''
    Custom top bar.
    '''
    def __init__(   self, parent: typing.Optional['QWidget'] = None, flags: typing.Union[QtCore.Qt.WindowFlags, QtCore.Qt.WindowType] = None,
                    doInitialize =  False,
                    _includeMenu = False,
                    _includeFontSpinBox = False,
                    _includeErrorButton = False,
                    _includeAdCB = False
                ) -> None:

        super(QCustomTopBarWidget, self).__init__(parent)
        # Initialize positional arguments
        self._doInitialize = doInitialize
        self._includeMenu = _includeMenu
        self._includeFontSpinBox= _includeFontSpinBox
        self._includeAdCB = _includeAdCB
        self._includeErrorButton = _includeErrorButton
        # ... #
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # applies cursor 'Hand'

        if doInitialize:
            self.initialize()
        
    def initialize(self, _includeMenu = False, 
                        _includeFontSpinBox = False,
                    _includeErrorButton = False,
                    _includeAdCB = False
                    ):
        self._includeMenu = _includeMenu
        self._includeFontSpinBox= _includeFontSpinBox
        self._includeAdCB = _includeAdCB
        self._includeErrorButton = _includeErrorButton
        self.setObjectName("TopBarWidget")
        if self.layout() == None:
            self.gridLayout = QGridLayout(self)
            self.gridLayout.setContentsMargins(0, 0, 0, 0)
            self.gridLayout.setSpacing(0)
            self.gridLayout.setObjectName("gridLayout")
            #self.gridLayout.setSizeConstraint(QtWidgets.QGridLayout.SetNoConstraint)
            self.setLayout(self.gridLayout)


        # region "Close Buttton"
        # Button "Close" in top bar
        self.custCloseBtn = QToolButton(self)
        self.custCloseBtn.setObjectName("custCloseBtn")
        self.custCloseBtn.setAutoRaise(True)

        self.layout().addWidget(    self.custCloseBtn, 0, 108, 1, 1, 
                                    QtCore.Qt.AlignRight
                                    )
          
                         
        self.custCloseBtn.setFont( QtGui.QFont("Arial",weight=QtGui.QFont.Bold))
        self.custCloseBtn.setText("×")
        self.custCloseBtn.setToolTip("End the session")

        self.RedHighlightPalette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(155, 0, 0))  # Dark Red
        brush.setStyle(QtCore.Qt.SolidPattern)
        
        self.RedHighlightPalette.setBrush(QtGui.QPalette.All, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        
        self.RedHighlightPalette.setBrush(QtGui.QPalette.All, QtGui.QPalette.ButtonText, brush)
        
        self.custCloseBtn.installEventFilter(self)
        self.custCloseBtn.setAutoRaise(True)
        
        self.custCloseBtn.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)) # sensible size

        self.custCloseBtn.clicked.connect(self._toggleExit)

        # endregion


        # region "Maximize"
        # Button "maximize" in top bar
        self.custMaxBtn = QToolButton(self)
        self.custMaxBtn.setObjectName("custMaxBtn")
        self.custMaxBtn.installEventFilter(self)
        self.custMaxBtn.setAutoRaise(True)
        self.custMaxBtn.setToolTip("Maximize window")
        self.custMaxBtn.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)) # sensible size
        self.layout().addWidget(    self.custMaxBtn, 0, 107, 1, 1, 
                                    QtCore.Qt.AlignRight
                                    )
        self.custMaxBtn.setFont( QtGui.QFont("Arial",weight=QtGui.QFont.Bold))
        self.custMaxBtn.setText(u"🗖")
        self.custMaxBtn.clicked.connect(self._toggleMinMax)
        # endregion

        # region "Minimize"
        # Button "minimize" in top bar 
        self.custMinBtn = QToolButton(self)
        self.custMinBtn.setObjectName("custMinBtn")
        self.custMinBtn.installEventFilter(self)
        self.custMinBtn.setAutoRaise(True)
        self.custMinBtn.setToolTip("Minimize window")
        self.custMinBtn.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)) # sensible size
        self.layout().addWidget(    self.custMinBtn, 0, 106, 1, 1, 
                                    QtCore.Qt.AlignRight
                                    )
        self.custMinBtn.setFont( QtGui.QFont("Arial",weight=QtGui.QFont.Bold))
        self.custMinBtn.setText("_")
        # endregion
         
          
        # Region "Settings" button
        self.settingsBtn = QToolButton(self)
        self.settingsBtn.setObjectName("OptionsButton")
        self.layout().addWidget(self.settingsBtn, 0, 105, 1, 1, QtCore.Qt.AlignRight)
        self.settingsBtn.setText("⚙")
        self.settingsBtn.setToolTip("Open settings")
        self.settingsBtn.installEventFilter(self)
        self.settingsBtn.setAutoRaise(True)
        self.settingsBtn.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))


    def _toggleExit(self):
        print("Close window...")
        self.window().close()


    def _toggleMinMax(self):
        """
        Seted icons for buttons "maximize" and "minimize" in depened of size.
        """
        #  ⇳⇖⇗⇘⇙⇕⇔↔↕↖↗↘↙ 
        # ⇱⇲
        if not self.window().isFullScreen(): # If not window opening in full screen 
                                             # icon maximization by default - u"\U0001F5D6"
            if self.window().isMaximized():
                self.window().showNormal()
                self.custMaxBtn.setText(u"🗖") # 🗖
            else:
                self.window().setGeometry(
                                            Qt.QStyle.alignedRect(
                                                QtCore.Qt.LeftToRight,
                                                QtCore.Qt.AlignCenter,
                                                self.window().size(),
                                                QApplication.instance().desktop().availableGeometry(self.window())))
                self.window().showMaximized()
                self.custMaxBtn.setText(u"🗖")
        else:
            try:
                if self.window().LastOpenState == self.window().showMaximized:
                    self.custMaxBtn.setText(u"🗖")
                else:
                    self.custMaxBtn.setText(u"🗖")
                self.window().LastOpenState()
            except AttributeError:
                self.custMaxBtn.setText(u"🗖")
                self.window().showMaximized()








