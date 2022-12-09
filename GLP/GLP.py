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
                                QSizePolicy, 
                                QLabel,
                                QSpinBox,
                                QPushButton,
                                QFrame
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


exceptions = (
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

def exception(exc = None, _exinf = True):
    '''
    Console output for exceptions
    ...except: error = exception(sys.exc_info())
    ...
    Parrse: Prints Time, type of exception, Filename + Line and (if extraInfo in not False) the exception description to the console\n
    return: string
    '''
    try:
        if False:
            if exc == None:
                exc = True
            return natinification(_exc = exc) # TODO: add natification
        else:
            if exc == None:
                exc_type, exc_obj, exc_tb = sys.exc_info()
            else:
                exc_type, exc_obj, exc_tb = exc
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            if _exinf:
                # print(cTimeSStr(),":") # Returns the time (including seconds) as a string: %H:%M:%S
                print(str(datetime.datetime.now().strftime('%H:%M:%S'))
                             + ":", exc_type, "in", file_name, " line", exc_tb.tb_lineno,":", exc_obj)
            else:
                print(str(datetime.datetime.now().strftime('%H:%M:%S'))
                             + ':', exc_type, " in", file_name, " line", exc_tb.tb_lineno)
            return str(exc_type) + ": " + str(exc_obj)
    except exceptions as inst:
        print("An exception occurred while trying to print an exception!")
        print(inst)


def advancedMode() -> bool:
    '''
    TODO: adding description
    '''
    return QApplication.instance().admode



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
            message = "Welcome to" + getpass.getuser()
        except: # TODO: adding exception for no-user
            message = "Welcome"
        self.lastMessageText = message
        self.lastMessageToolTip = message
        self.lastMessageIcon = QtGui.QIcon()


        self.moduleVersion = "Python %s\n GLP %s " % (" %d.%d" % (sys.version_info.major, sys.version_info.minor),
                                                        version
                                                        )
        # Initilize font by default
        self.initFont()

        self.AppPalettes = {}
        self.colourSheme()

        self.admode = False

    def setMainWindow(self, win):
        self.MainWindow = win

    def initFont(self):
        self.defFont = QtGui.QFont()
        self.defFont.setFamily("Helvetica [Cronyx]")
        self.defFont.setPointSize(9)
        # self.defFont.setBold(True)
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
    def popUpWindowNotinification(self):
        '''
        
        '''
        print('Pressed!')


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
        except exceptions:
            exception(sys.exc_info())
        try:
            self.canvas.draw()
        except exceptions:
            exception(sys.exc_info())

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

        self.GPLWidget = customQFrameWidget(self)
        self.gridLayGPLWidget =  QGridLayout(self.GPLWidget)
        self.gridLayGPLWidget.setContentsMargins(0, 0, 0, 0)
        self.gridLayGPLWidget.setSpacing(0)
        self.gridLayGPLWidget.setObjectName("gridLayout")
        self.GPLWidget.setLayout(self.gridLayGPLWidget)
        
        self.centrWindowWidget = QMainWindow(self)
        self.gridLayGPLWidget.addWidget(self.centrWindowWidget,1,0)
        super(GLPWindow, self).setCentralWidget(self.GPLWidget)

        self.installEventFilter(self)


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
            self.initialize(_includeMenu, _includeFontSpinBox, _includeErrorButton, _includeAdCB)
        
    def initialize(self, _includeMenu           = False, 
                         _includeFontSpinBox    = False,
                         _includeErrorButton    = False,
                         _includeAdCB           = False
                    ):
        self._includeMenu           = _includeMenu
        self._includeFontSpinBox    = _includeFontSpinBox
        self._includeAdCB           = _includeAdCB
        self._includeErrorButton    = _includeErrorButton
        self.setObjectName("QCustomTopBarWidget")

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
          
                         
        self.custCloseBtn.setFont( QtGui.QFont("Arial", weight = QtGui.QFont.Bold))
        self.custCloseBtn.setText("x")
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
        self.custMaxBtn.setText(u"□") # TODO:add picture 
        self.custMaxBtn.clicked.connect(self._toggleMaximized)
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
        self.custMinBtn.setText("_") # TODO:add picture 
        self.custMinBtn.clicked.connect(self._toggleMinimized)
        # endregion
         
          
        # Region "Settings" button
        self.settingsBtn = QToolButton(self)
        self.settingsBtn.setObjectName("OptionsButton")
        self.layout().addWidget(self.settingsBtn, 0, 105, 1, 1, QtCore.Qt.AlignRight)
        self.settingsBtn.setText(u"⚙️") # TODO:add picture 
        self.settingsBtn.setToolTip("Open settings")
        self.settingsBtn.installEventFilter(self)
        self.settingsBtn.setAutoRaise(True)
        self.settingsBtn.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        # -> slot by clicked
        # self.settingsBtn.clicked.connect(app().showSettings) # TODO: add method opening settings app


        self.moveHand = QLabel(self)
        self.moveHand.setObjectName("moveHand")
        self.layout().addWidget(self.moveHand, 0, 104, 1, 1,QtCore.Qt.AlignRight)
        self.moveHand.setToolTip("Move")
        self.moveHand.setText(u"👆")
        self.moveHand.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        try:
            #self.window().menuBar().installEventFilter(self)
            if self._includeMenu:
                self.Menu = QToolButton(self)
                self.Menu.setObjectName("Menu")
                self.layout().addWidget(self.Menu, 0, 103, 1, 1,QtCore.Qt.AlignRight)
                self.Menu.setText(u"\u2630")
                self.Menu.setAutoRaise(True)
                self.Menu.setPopupMode(QToolButton.InstantPopup)
                self.Menu.setMenu(self.window().Menu)
                self.Menu.setSizePolicy(self.ButtonSizePolicy)
        except exceptions:
            exception(sys.exc_info())

        if self._includeFontSpinBox:
            self.fontSpinBox = QSpinBox(self)
            self.fontSpinBox.setObjectName("fontSpinBox")
            self.fontSpinBox.setMinimum(9)
            self.fontSpinBox.setMaximum(14)

            self.fontSpinBox.setProperty("value", self.font().pointSize())
            self.layout().addWidget(self.fontSpinBox, 0, 102, 1, 1,QtCore.Qt.AlignRight)
            self.fontSpinBox.valueChanged.connect(self.changedSizeOfFont)

        if _includeErrorButton:
            self.error_notification = QPushButton(self)
            self.error_notification.setObjectName("error_notification")
            self.error_notification.setText(QApplication.instance().lastMessageText)
            self.error_notification.setToolTip(QApplication.instance().lastMessageToolTip)
            self.error_notification.setIcon(QApplication.instance().lastMessageIcon)
            
            self.layout().addWidget(self.error_notification, 0, 101, 1, 1, QtCore.Qt.AlignRight)
            self.error_notification.installEventFilter(self)
            self.error_notification.clicked.connect(QApplication.instance().popUpWindowNotinification)

        # if self._includeAdCB:
        #     pass

        self.moving = False

    def _toggleExit(self):
        print("Close window...")
        self.window().close()


    def _toggleMaximized(self):
        """
        Seted icons for buttons "maximize" and "minimize" in depened of size.
        """
        #  ⇳⇖⇗⇘⇙⇕⇔↔↕↖↗↘↙
        # ⇱⇲
        if not self.window().isFullScreen(): # If not window opening in full screen 
                                             # icon maximization by default - u"\U0001F5D6"
            if self.window().isMaximized():
                self.window().showNormal()
                self.custMaxBtn.setText(u"□") # 🗖
            else:
                self.window().setGeometry(
                                            Qt.QStyle.alignedRect(
                                                QtCore.Qt.LeftToRight,
                                                QtCore.Qt.AlignCenter,
                                                self.window().size(),
                                                QApplication.instance().desktop().availableGeometry(self.window())))
                self.window().showMaximized()
                self.custMaxBtn.setText(u"□")
        else:
            try:
                if self.window().LastOpenState == self.window().showMaximized:
                    self.custMaxBtn.setText(u"□")
                else:
                    self.custMaxBtn.setText(u"□")
                self.window().LastOpenState()
            except AttributeError:
                self.custMaxBtn.setText(u"□")
                self.window().showMaximized()


    def _toggleMinimized(self): 
        '''
        Slot minimized window.
        '''
        self.window().showMinimized() # that's all

    def eventFilter(self, a0, a1) -> bool:
        if a1.type() == 10 or a1.type() == 11:
            if a0 == self.custCloseBtn:
                if a1.type() == QtCore.QEvent.Enter: # HoverMove
                    self.custCloseBtn.setPalette(self.RedHighlightPalette)
                elif a1.type() == QtCore.QEvent.Leave: # HoverLeave
                    self.custCloseBtn.setPalette(self.palette())
            elif a0 == self.custMaxBtn:
                if a1.type() == QtCore.QEvent.Enter:
                    self.custMaxBtn.setAutoRaise(False)
                elif a1.type() == QtCore.QEvent.Leave:
                    self.custMaxBtn.setAutoRaise(True)
            elif a0 == self.custMinBtn:
                if a1.type() == QtCore.QEvent.Enter:
                    self.custMinBtn.setAutoRaise(False)
                elif a1.type() == QtCore.QEvent.Leave:
                    self.custMinBtn.setAutoRaise(True)
        # elif self._includeErrorButton and a0 is self.error_notification and a1.type() == QtCore.QEvent.Enter:
        #     QToolTip.showText(QtGui.QCursor.pos(), self.error_notification.toolTip(), self.error_notification)
        return super(QCustomTopBarWidget, self).eventFilter(a0, a1)

    def changedSizeOfFont(self):
        '''
        Changing size of font
        '''
        
        try:
            QApplication.instance().SetFont(PointSize = self.fontSpinBox.value(), 
                                            source = self.window())
        except exceptions:
            exception(sys.exc_info())

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if a0.button() == QtCore.Qt.LeftButton:
            self.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            self.moveHand.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            self.moving = True; self.offset = a0.globalPos() - self.window().geometry().topLeft()
        return super().mousePressEvent(a0)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.moveHand.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        if a0.button() == QtCore.Qt.LeftButton:
            pos = self.window().pos()
            #if (pos.x() < 0):
            #    pos.setX(0)
            #    self.window().move(pos)
            if (pos.y() < 0):
                pos.setY(0)
                self.window().move(pos)
            # If the mouse is in a corner or on a side let the window fill this corner or side of the screen
            try:
                Tolerance = 5
                eventPos = a0.globalPos()
                screenNumber = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
                screen = QApplication.desktop().availableGeometry(screenNumber)
                Half_X = (screen.bottomRight().x()-screen.topLeft().x())/2+1
                Full_X = (screen.bottomRight().x()-screen.topLeft().x())+1
                Half_Y = (screen.bottomRight().y()-screen.topLeft().y())/2+1
                Full_Y = (screen.bottomRight().y()-screen.topLeft().y())+1
                BottomMax = screen.bottomLeft().y()
                RightMax = screen.bottomRight().x()
                TopMax = screen.topLeft().y()
                LeftMax = screen.topLeft().x()
                #if (pos.y() > BottomMax): # If Bottom Side gets removed this must be turned on to make it impossible for the window to get lost behind the task bar
                #    pos.setY(BottomMax-50)
                #    self.window().move(pos)
                # Top Left
                if eventPos.x() <= Tolerance + LeftMax and eventPos.y() <= Tolerance + TopMax:
                    self.window().resize(Half_X, Half_Y)
                    frameGm = self.window().frameGeometry()
                    frameGm.moveTopLeft(screen.topLeft())
                    self.window().move(frameGm.topLeft())
                # Bottom Left
                elif eventPos.x() <= Tolerance + LeftMax and eventPos.y() >= BottomMax-Tolerance:
                    self.window().resize(Half_X, Half_Y)
                    frameGm = self.window().frameGeometry()
                    frameGm.moveBottomLeft(screen.bottomLeft())
                    self.window().move(frameGm.topLeft())
                # Top Right
                elif eventPos.x() >= RightMax-Tolerance and eventPos.y() <= Tolerance + TopMax:
                    self.window().resize(Half_X, Half_Y)
                    frameGm = self.window().frameGeometry()
                    frameGm.moveTopRight(screen.topRight())
                    self.window().move(frameGm.topLeft())
                # Bottom Right
                elif eventPos.x() >= RightMax-Tolerance and eventPos.y() >= BottomMax-Tolerance:
                    self.window().resize(Half_X, Half_Y)
                    frameGm = self.window().frameGeometry()
                    frameGm.moveBottomRight(screen.bottomRight())
                    self.window().move(frameGm.topLeft())
                # Left Side
                elif eventPos.x() <= Tolerance + LeftMax:
                    self.window().resize(Half_X, Full_Y)
                    frameGm = self.window().frameGeometry()
                    frameGm.moveTopLeft(screen.topLeft())
                    self.window().move(frameGm.topLeft())
                # Right Side
                elif eventPos.x() >= RightMax-Tolerance:
                    self.window().resize(Half_X, Full_Y)
                    frameGm = self.window().frameGeometry()
                    frameGm.moveTopRight(screen.topRight())
                    self.window().move(frameGm.topLeft())
                # Top Side
                elif eventPos.y() <= Tolerance + TopMax:
                    if advancedMode(): # MAYBE: Make this behaviour for advanced mode toggable in the options if a user never wants this
                        self.window().resize(Full_X, Half_Y)
                        frameGm = self.window().frameGeometry()
                        frameGm.moveTopRight(screen.topRight())
                        self.window().move(frameGm.topLeft())
                    else:
                        self.window().showMaximized()
                # Bottom Side
                elif eventPos.y() >= BottomMax-Tolerance:
                    self.window().resize(Full_X, Half_Y)
                    frameGm = self.window().frameGeometry()
                    frameGm.moveBottomLeft(screen.bottomLeft())
                    self.window().move(frameGm.topLeft())
            except exceptions:
                pass # TODO: Add notification
        return super().mouseReleaseEvent(a0)

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.moving:
            if (self.window().isMaximized() or self.window().isFullScreen()): # If moving the window while in fullscreen or maximized make it normal first
                # TODO: Make normalizing the window relative to the previous and current window width to keep the cursor on the window regardless wether clicking right or left
                self.custMaxBtn.setText("□")
                corPos = self.window().geometry().topRight()
                self.window().showNormal()
                self.window().GPLWidget.inFrame() # TODO: fix
                QApplication.instance().processEvents()
                self.window().move(corPos - self.window().geometry().topRight()+self.window().geometry().topLeft())
                self.offset = a0.globalPos() - self.window().geometry().topLeft()
            self.window().move(a0.globalPos() - self.offset)
        return super().mouseMoveEvent(a0)

class customQFrameWidget(QFrame):
    '''
    TODO: add description
    '''
    def __init__(self, parent: typing.Optional[QWidget] = None, 
                flags: typing.Union[QtCore.Qt.WindowFlags, QtCore.Qt.WindowType] = None) -> None:
        super(customQFrameWidget, self).__init__(parent)
        self.enabledFrame = False

    def inFrame(self):
        self.enabledFrame = True
        self.setFrameStyle(self.Box | self.Sunken)
        self.setLineWidth(2)
        #self.setMidLineWidth(3)