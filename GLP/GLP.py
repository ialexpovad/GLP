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
from time import time as timetime
import traceback


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
                                QFrame,
                                QSplitter,
                                QAbstractItemView,
                                QListWidget,
                                QListWidgetItem,
                                QStatusBar
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
            return NC(_exc = exc) # TODO: add natification
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
            message = "Welcome to " + getpass.getuser()
        except: # TODO: adding exception for no-user
            message = "Welcome"
        self.lastMessageText = message
        self.lastMessageToolTip = message
        self.lastMessageIcon = QtGui.QIcon()
        self.winNotif = None

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
            try:
                importlib.reload(theme)
            except:
                NC(2,"Could not reload AGeColour",exc=sys.exc_info(),
                    func="Main_App.Recolour",input=str(colour))
            try:    
                spec = importlib.util.spec_from_file_location(  "CustomColourPalettes", 
                                                                os.path.join(self.GPLSettingsPath,
                                                                "CustomColourPalettes.py")
                                                                )
                CustomColours = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(CustomColours)
            except:
                NC(4,"Could not load custom colours",exc=sys.exc_info(),
                    func="Main_App.Recolour",input=str(colour))
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
        """
        Default access: pressing the notification button
        Shows a window that lists all notifications and displays their details.
        """
        if self.winNotif == None:
            self.winNotif = windowNotification()# TODO: create subclass by QMainWindow 
        self.winNotif.show()
        self.processEvents()
        self.winNotif.positionReset()
        self.processEvents()
        self.winNotif.activateWindow()

class NC: # Notification Class
    """
    This is the basic notification class of AGeLib.  \n
    All notifications are stored and accessible via the Notification Window which is opened by pressing on Notification button of any (AWWF) window.   \n
    Notifications are used to communicate with the user and can be used for exception handling as they provide space for an entire bug report.   \n
    They contain the version number of all modules that are in MainApp.ModuleVersions and can extract all information from exceptions.   \n
    There are various levels of notifications: lvl: 0 = Nothing , 1 = Error , 2 = Warning , 3 = Notification , 4 = Advanced Mode Notification , 10 = Direct Notification  \n
    The notification sends itself automatically. If you want to modify the notification before it is send set ``send=False`` and call ``.send()`` after the modifications are done  \n
    The creation is very flexible. Here are a few examples:   \n
    ```python
    NC(10,"This message is directly displayed in the top bar and should be held very short and not contain any linebreaks (a single linebreak is ok in spacial cases)")
    NC("This creates a normal notification")
    NC(2,"This creates a warning")
    NC((2,"A tuple with level and message is also acceptable"))
    NC("This generates an error notification with the last caught exception",exc = sys.exc_info())
    NC("This notification includes the callstack",tb=True)
    ```
    Even this is valid: ``NC()`` (Though not recommended)   \n
    ``lvl=0`` can be useful if you want to create a notification in a function (with ``Notification = NC(lvl=0,send=False)``), fill it with information dynamically and return it for the caller.
    The caller can then send the Notification. If ``lvl=0`` the MainApp will ignore the notification thus the caller does not need to care whether the function actually had anything to notify the user about.   \n
    If you want to notify the user about exceptions ``exc`` should be ``True`` or ``sys.exc_info()``. If the exception should be logged but is usually not important set ``lvl=4``.
    If the exception is not critical but should be noted as it might lead to unwanted behaviour set ``lvl=2`` to warn the user.
    Exception notifications should set ``msg`` to give a short description that a regular user can understand (for example ``msg="The input could not be interpreted."`` or ``msg="Could not connect to the website."``).
    It is also useful to set ``input`` to log the input that lead to the error. This should also include any settings that were used.   \n
    Only ``lvl=int``,``time=datetime.datetime.now()``,``send=bool`` and ``exc=True or sys.exc_info()`` need a specific data type.
    Everything else will be stored (msg will be converted into a string before storing). The access methods will return a string (and cast all input to a string before saving)
    but the variables can still be accessed directly with the data type that was given to the init.  \n
    Please note that ``err`` and ``tb`` are ignored when ``exc != None`` as they will be extracted from the exception.  \n
    ``tb`` should be a string containing the callstack or ``True`` to generate a callstack
    """
    def __init__(self, lvl=None, msg=None, time=None, input=None, err=None, tb=None, exc=None, win=None, func=None, DplStr=None, send=True):
        """
        Creates a new notification object  \n
        The creation is very flexible. Here are a few examples:   \n
        ```python
        NC(10,"This message is directly displayed in the top bar and should be held short and without linebreaks")
        NC("This creates a normal notification")
        NC(2,"This creates a warning")
        NC((2,"A tuple with level and message is also acceptable"))
        NC("This generates an error notification with the last caught exception",exc = sys.exc_info())
        NC("This notification includes the callstack",tb=True)
        ```
        lvl: 0 = Nothing , 1 = Error , 2 = Warning , 3 = Notification , 4 = Advanced Mode Notification , 10 = Direct Notification  \n
        ``exc = True`` or ``sys.exc_info()``   \n
        ``tb`` should be a string containing the callstack or ``True`` to generate a callstack
        """
        self._time_time = timetime()
        self._init_Values()
        self._was_send = False
        try:
            self._time = datetime.datetime.now() if time == None else time
            self.Time = self._time.strftime('%H:%M:%S')
            self.DplStr = DplStr
            self.Window = win
            self.Function = func
            self.Input = input
            if exc != None:
                if exc == True:
                    self.exc_type, self.exc_obj, self.exc_tb = sys.exc_info()
                else:
                    self.exc_type, self.exc_obj, self.exc_tb = exc
                fName = os.path.split(self.exc_tb.tb_frame.f_code.co_filename)[1]
                if type(lvl)==str:
                    self.level = 1
                    self.Message = lvl 
                elif msg==None and type(lvl) == tuple:
                    self.level, self.Message = lvl[0], lvl[1]
                else:
                    self.level = 1 if lvl == None else lvl
                    self.Message = str(msg) if msg!=None else None
                self.ErrorTraceback = str(self.exc_type)+"  in "+str(fName)+"  line "+str(self.exc_tb.tb_lineno)+"\n\n"+str(traceback.format_exc())#[:-1]) # TODO: Use traceback.format_exc() to get full traceback or something like traceback.extract_stack()[:-1] ([:-1] removes the NC.__init__())
                print(self.Time,":")
                if len(str(self.exc_obj))<150:
                    self.Error = str(self.exc_type)+": "+str(self.exc_obj)
                    print(self.exc_type, " in", fName, " line", self.exc_tb.tb_lineno,": ", self.exc_obj)
                else:
                    self.Error = str(self.exc_type)
                    self.ErrorLongDesc = str(self.exc_obj)
                    print(self.exc_type, " in", fName, " line", self.exc_tb.tb_lineno)
            else:
                if type(lvl)==str:
                    self.level = 3
                    self.Message = lvl
                elif msg==None and type(lvl) == tuple:
                    self.level, self.Message = lvl[0], lvl[1]
                else:
                    self.level = 3 if lvl == None else lvl
                    self.Message = str(msg) if msg!=None else None
                self.Error = err
                if tb == True:
                    self.ErrorTraceback = ""
                    try:
                        for i in traceback.format_stack()[0:-1]:
                            self.ErrorTraceback += str(i)
                    except:
                        self.ErrorTraceback = "Could not extract callstack"
                else:
                    self.ErrorTraceback = tb
            self.GenerateLevelName()
            if send == True:
                self.send()
        except exceptions as inst:
            self._init_Values()
            print(str(datetime.datetime.now().strftime('%H:%M:%S')),": An exception occurred while trying to create a Notification")
            print(inst)
            self._time = datetime.datetime.now() if time == None else time
            self.Time = self._time.strftime('%H:%M:%S')
            self.Message = "An exception occurred while trying to create a Notification"
            self.exc_obj = inst
            self.Error = str(inst)
            self.GenerateLevelName()
            self.send(force=True)

    def _init_Values(self):
        self.exc_type, self.exc_obj, self.exc_tb = None,None,None
        self._time, self.Time, self.Error = None,None,None
        self.Window, self.ErrorTraceback, self.Function = None,None,None
        self.level, self.Level, self.Message = 1,"Notification level 1",None
        self.Input, self.ErrorLongDesc = None,None
        self.DplStr, self.TTStr = None,None
        self.icon = QtGui.QIcon()
        try:
            self.Flash = QApplication.instance().NCF_NONE
        except exceptions as inst:
            print(inst)
            self.Flash = None
        self.itemDict = {"Time:\n":self.Time,"Level: ":self.Level,"Message:\n":self.Message,
                        "Error:\n":self.Error,"Error Description:\n":self.ErrorLongDesc,"Error Traceback:\n":self.ErrorTraceback,
                        "Function:\n":self.Function,"Window:\n":self.Window,"Input:\n":self.Input}
  #---------- send, print ----------#
    def send(self,force=False):
        """
        Displays this notification (This method is thread save but this object should not be modified after using send)   \n
        A notification can only be send once. ``force=True`` allows to send an already send notification again
        """
        if force or not self._was_send:
            self._was_send = True
            QApplication.postEvent(QtCore.QThread.currentThread(), NotificationEvent(self))

    def print(self):
        """Prints this notification to the console"""
        print("\n",self.Level, "at",self.Time,"\nMessage:",self.Message)
        if self.Error != None:
            print("Error:",self.Error,"Traceback:",self.ErrorTraceback,"\n")
  #---------- items, unpack ----------#
    def items(self):
        """
        Returns self.itemDict.items()   \n
        self.itemDict contains all relevant data about this notification.  \n
        Please note that not all values are strings and should be converted before diplaying them.
        This allows ``if v!=None:`` to filter out all empty entries.    \n
        The keys already end with ``:\\n`` thus it is advised to simply use ``k+str(v)`` for formatting.  \n
        For an example how to use this method see the source code of ``NotificationInfoWidget``.
        """
        self.itemDict = {"Time:\n":self.Time,"Level: ":"({})\n{}".format(str(self.level),self.Level),"Message:\n":self.Message,
                        "Error:\n":self.Error,"Error Description:\n":self.ErrorLongDesc,"Error Traceback:\n":self.ErrorTraceback,
                        "Function:\n":self.Function,"Window:\n":self.Window,"Input:\n":self.Input,"Versions:\n":QApplication.instance().ModuleVersions}
        return self.itemDict.items()

    def unpack(self): #CLEANUP: remove unpack
        """DEPRECATED: Returns a tuple ``(int(level),str(Message),str(Time))``"""
        return (self.level, str(self.Message), self.Time)
  #---------- access variables ----------#
    def l(self, level=None):
        """
        Returns int(level)  \n
        An int can be given to change the level
        """
        if level != None:
            self.level = level
            self.GenerateLevelName()
        return self.level

    def m(self, message=None):
        """
        Returns str(Message)  \n
        A str can be given to change the Message
        """
        if message != None:
            self.Message = str(message)
        if self.Message == None and self.Error != None:
            return str(self.Error)
        else:
            return str(self.Message)
        
    def DPS(self, DplStr = None):
        """
        Returns str(DplStr)  \n
        DplStr is the string that is intended to be displayed directly   \n
        A str can be given to change the DplStr
        """
        if DplStr != None:
            self.DplStr = str(DplStr)
        elif self.DplStr == None:
            if self.level == 10:
                self.DplStr = self.m()
            else:
                self.DplStr = self.Level + " at " + self.t()
        return str(self.DplStr)
        
    def TTS(self, TTStr = None):
        """
        Returns str(TTStr)  \n
        TTStr is the string that is intended to be displayed as the tool tip   \n
        A str can be given to change the TTStr
        """
        if TTStr != None:
            self.TTStr = str(TTStr)
        elif self.TTStr == None:
            if self.level == 10:
                self.TTStr = self.Level + " at " + self.t()
            else:
                self.TTStr = self.m()
        return str(self.TTStr)

    def t(self, time=None):
        """
        Returns the time as %H:%M:%S  \n
        datetime.datetime.now() can be given to change the time
        """
        if time != None:
            self._time = time
            self.Time = self._time.strftime('%H:%M:%S')
        return self.Time

    def e(self, Error=None, ErrorTraceback=None):
        """
        Returns str(Error)  \n
        strings can be given to change the Error and ErrorTraceback
        """
        if Error != None:
            self.Error = str(Error)
        if ErrorTraceback != None:
            self.ErrorTraceback = str(ErrorTraceback)
        return str(self.Error)

    def tb(self, ErrorTraceback=None):
        """
        Returns str(ErrorTraceback)  \n
        A str can be given to change the ErrorTraceback
        """
        if ErrorTraceback != None:
            self.ErrorTraceback = str(ErrorTraceback)
        return str(self.ErrorTraceback)

    def f(self, func=None):
        """
        Returns str(Function)  \n
        A str can be given to change the Function  \n
        Function is the name of the function from which this notification originates
        """
        if func != None:
            self.Function = str(func)
        return str(self.Function)

    def w(self, win=None):
        """
        Returns str(Window)  \n
        A str can be given to change the Window  \n
        Window is the name of the window from which this notification originates
        """
        if win != None:
            self.Window = str(win)
        return str(self.Window)

    def i(self, input=None):
        """
        Returns str(Input)  \n
        A str can be given to change the Input  \n
        Input is the (user-)input that caused this notification
        """
        if input != None:
            self.Input = str(input)
        return str(self.Input)
  #---------- GenerateLevelName ----------#
    def GenerateLevelName(self):
        """
        Generates str(self.Level) from int(self.level)
        """
        try:
            if self.level == 0:
                self.Level = "Empty Notification"
                self.icon = QtGui.QIcon()
                self.Flash = QApplication.instance().NCF_NONE
            elif self.level == 1:
                self.Level = "Error"
                self.icon = QApplication.style().standardIcon(QStyle.SP_MessageBoxCritical)
                self.Flash = QApplication.instance().NCF_r
            elif self.level == 2:
                self.Level = "Warning"
                self.icon = QApplication.style().standardIcon(QStyle.SP_MessageBoxWarning)
                self.Flash = QApplication.instance().NCF_y
            elif self.level == 3:
                self.Level = "Notification"
                self.icon = QApplication.style().standardIcon(QStyle.SP_MessageBoxInformation)
                self.Flash = QApplication.instance().NCF_b
            elif self.level == 4:
                self.Level = "Advanced Mode Notification"
                self.icon = QApplication.style().standardIcon(QStyle.SP_MessageBoxInformation)
                self.Flash = QApplication.instance().NCF_b
            elif self.level == 10:
                self.Level = "Direct Notification"
                self.icon = QtGui.QIcon()
                self.Flash = QApplication.instance().NCF_NONE
            else:
                self.Level = "Notification level "+str(self.level)
                self.Flash = QApplication.instance().NCF_b
            return self.Level
        except exceptions as inst:
            print(inst)
            return "Could not generate Level Name"
    def __add__(self,other):
        if self.Error != None:
            return str(self.Error) + str(other)
        else:
            return str(self.Message) + str(other)

    def __radd__(self,other):
        if self.Error != None:
            return str(other) + str(self.Error)
        else:
            return str(other) + str(self.Message)

    def __call__(self):
        return str(self.Message)

    def __str__(self):
        if self.Error != None:
            if self.Message == None:
                return "Exception at "+str(self.Time)+":\n"+str(self.Error)
            else:
                return str(self.Level)+" at "+str(self.Time)+":\n"+str(self.Message)+"\n"+str(self.Error)
        else:
            return str(self.Level)+" at "+str(self.Time)+":\n"+str(self.Message)

class NotificationEvent(QtCore.QEvent):
    EVENT_TYPE = QtCore.QEvent.Type(QtCore.QEvent.registerEventType())
    def __init__(self, N):
        QtCore.QEvent.__init__(self, NotificationEvent.EVENT_TYPE)
        self.N = N


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
        self._fullScreen_HideBars = _fullScreen_HideBars
        self._include_QStatusBar = _include_QStatusBar
        self._init_QTopBar = _init_QTopBar
        self._include_QTopBar = _include_QTopBar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint,True)
        
        

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

        if _include_QTopBar:
            self.customQTopBar = QCustomTopBarWidget(self, _init_QTopBar)
            self.customQMenuBar = QCustomMenuBar(self)
            self.setMenuBar(self.customQMenuBar)
            self.customQMenuBar.setCornerWidget(self.customQTopBar)
            self.customQMenuBar.setContentsMargins(0,0,0,0)
        if _include_QStatusBar:
            self.customQStatusBar = QCustomStatusBar(self)
            self.customQStatusBar.setObjectName("QCustomStatusBar")
            self.setStatusBar(self.customQStatusBar)
            self.customQStatusBar.setSizeGripEnabled(False)
            self.windowTitleChanged.connect(self.customQStatusBar.setWindowTitle)
        
        self.doHideBar = False
        self.standardSize = (600, 300)

        
        
    def show(self):
        self.setTopBarVisible(True)
        super(GLPWindow, self).show()
        QApplication.instance().processEvents()
        if self.isFullScreen() or self.isMaximized():
            self.GPLWidget.hideFrame()
            self.customQTopBar.custMaxBtn.setText("□")
        else:
            self.GPLWidget.inFrame()
            self.customQTopBar.custMaxBtn.setText("□")
        if self.isFullScreen() and self._fullScreen_HideBars:
            self.setTopBarVisible(False)
    
    def setTopBarVisible(self, boolean):
        if not self.doHideBar:
            self.customQTopBar.setVisible(boolean)
            try:
                self.customQMenuBar.setVisible(boolean)
            except:
                # TODO: add notification
                pass
            try:
                self.customQStatusBar.setVisible(boolean)
            except:
                # TODO: add notification
                pass

    def positionReset(self):
        self.showNormal()
        QApplication.instance().processEvents()
        try:
            self.resize(*self.standardSize)
        except exceptions:
            self.resize(900, 600)
        QApplication.instance().processEvents()
        try:
            frameGm = self.frameGeometry()
            screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
            centerPoint = QApplication.desktop().screenGeometry(screen).center()
            frameGm.moveCenter(centerPoint)
            self.move(frameGm.topLeft())
        except exceptions:
            exception(sys.exc_info())
        QApplication.instance().processEvents()
        
    def showNormal(self):
            self.setTopBarVisible(True)
            self.GPLWidget.inFrame()
            self.customQTopBar.custMaxBtn.setText("□")
            super(GLPWindow, self).showNormal()


class QCustomMenuBar(QMenuBar):
    '''
    Custom QMenuBar for this library.
    '''
    def __init__(self, parent = None) -> None:
        super(QCustomMenuBar, self).__init__(parent)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # applies cursor 'Hand'
        self.moving = False
        self.offset = 0
        self.setMouseTracking(True)

    def mousePressEvent(self,event):
        if event.button() == QtCore.Qt.LeftButton and self.actionAt(event.pos())==None and self.moving == False and self.activeAction()==None:
            self.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            self.moving = True
            self.offset = event.globalPos()-self.window().geometry().topLeft()
            self.window().GPLWidget.moving = False
            event.accept()
        else:
            self.moving = False
        super(QCustomMenuBar, self).mousePressEvent(event)

    def mouseReleaseEvent(self,event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.window().GPLWidget.moving = False
        if event.button() == QtCore.Qt.LeftButton and self.moving:
            self.moving = False
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
                eventPos = event.globalPos()
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
                    if advancedMode():
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
                NC( exc=sys.exc_info(),
                    win=self.window().windowTitle(),
                    func="QCustomMenuBar.mouseReleaseEvent")
        else:
            self.moving = False
            super(QCustomMenuBar, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self,event):
        if self.moving:
            event.accept()
            self.window().GPLWidget.moving = False
            if (self.window().isMaximized() or self.window().isFullScreen()): # If moving the window while in fullscreen or maximized make it normal first
                try:
                    self.window().TopBar.MaximizeButton.setText("□")
                except exceptions:
                    pass
                corPos = self.window().geometry().topRight()
                self.window().showNormal()
                self.window().GPLwidget.inFrame()
                QApplication.instance().processEvents()
                self.window().move(corPos-self.window().geometry().topRight() + 
                                self.window().geometry().topLeft())
                self.offset = event.globalPos()-self.window().geometry().topLeft()
            self.window().move(event.globalPos()-self.offset)
        else:
            if self.actionAt(event.pos()) != None:
                self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            else:
                self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            super(QCustomMenuBar, self).mouseMoveEvent(event)

class QCustomStatusBar(QStatusBar):
    def __init__(self, parent=None):
        super(QCustomStatusBar, self).__init__(parent)
        self.nameWindow = QLabel(self)
        self.addPermanentWidget(self.nameWindow)

    def setWindowTitle(self, WindowTitle):
        WindowTitle = WindowTitle + " "
        self.nameWindow.setText(WindowTitle)

class QCustomTopBarWidget(QWidget):

    '''
    Custom top bar.
    '''
    def __init__(   self, parent= None, doInitialize =  False, _includeMenu = False, _includeFontSpinBox = False, _includeErrorButton = False,  _includeAdCB = False
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
        darkRedBrush = QtGui.QBrush(QtGui.QColor(139, 0, 0))  # Dark Red
        darkRedBrush.setStyle(QtCore.Qt.SolidPattern)
        
        self.RedHighlightPalette.setBrush(QtGui.QPalette.All, QtGui.QPalette.Button, darkRedBrush)
        darkRedBrush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        darkRedBrush.setStyle(QtCore.Qt.SolidPattern)
        self.RedHighlightPalette.setBrush(QtGui.QPalette.All, QtGui.QPalette.ButtonText, darkRedBrush)

        
        self.BlueHighLightPallete = QtGui.QPalette()
        darkBlueBrush = QtGui.QBrush(QtGui.QColor(0,0,139))
        darkBlueBrush.setStyle(QtCore.Qt.SolidPattern)
        self.BlueHighLightPallete.setBrush(QtGui.QPalette.All, QtGui.QPalette.Button, darkBlueBrush)
        darkBlueBrush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        darkBlueBrush.setStyle(QtCore.Qt.SolidPattern)
        self.BlueHighLightPallete.setBrush(QtGui.QPalette.All, QtGui.QPalette.ButtonText, darkBlueBrush)

        self.GreenHighLightPallete = QtGui.QPalette()
        darkGreenBrush = QtGui.QBrush(QtGui.QColor(21,71,52))
        darkGreenBrush.setStyle(QtCore.Qt.SolidPattern)
        self.GreenHighLightPallete.setBrush(QtGui.QPalette.All, QtGui.QPalette.Button, darkGreenBrush)
        darkGreenBrush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        darkGreenBrush.setStyle(QtCore.Qt.SolidPattern)
        self.GreenHighLightPallete.setBrush(QtGui.QPalette.All, QtGui.QPalette.ButtonText, darkGreenBrush)

        

        
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
        # http://qtdocs.narod.ru/4.1.0/doc/html/qevent.html
        if a1.type() == 10 or a1.type() == 11: # 11 - The mouse pointer leaves the widget area.
                                               # 10 - The mouse pointer enters the widget area.     
            if a0 == self.custCloseBtn:
                if a1.type() == QtCore.QEvent.Enter: # HoverMove
                    self.custCloseBtn.setPalette(self.RedHighlightPalette)
                elif a1.type() == QtCore.QEvent.Leave: # HoverLeave
                    self.custCloseBtn.setPalette(self.palette())
            elif a0 == self.custMaxBtn:
                if a1.type() == QtCore.QEvent.Enter:
                    self.custMaxBtn.setAutoRaise(False)
                    self.custMaxBtn.setPalette(self.BlueHighLightPallete)
                elif a1.type() == QtCore.QEvent.Leave:
                    self.custMaxBtn.setAutoRaise(True)
                    self.custMaxBtn.setPalette(self.palette())
            elif a0 == self.custMinBtn:
                if a1.type() == QtCore.QEvent.Enter:
                    self.custMinBtn.setAutoRaise(False)
                    self.custMinBtn.setPalette(self.GreenHighLightPallete)
                elif a1.type() == QtCore.QEvent.Leave:
                    self.custMinBtn.setAutoRaise(True)
                    self.custMinBtn.setPalette(self.palette())
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
        # TODO: resizable and movable main window without title bar



    def inFrame(self):
        '''
        TODO: ...
        '''
        self.enabledFrame = True
        self.setFrameStyle(self.Box | self.Sunken)
        self.setLineWidth(1)
        #self.setMidLineWidth(1)

    def hideFrame(self):
        '''
        TODO: ...
        '''
        self.enabledFrame = False
        self.setFrameStyle(self.Box | self.Sunken)
        self.setLineWidth(1)
        #self.setMidLineWidth(1)



class windowNotification(GLPWindow):
    '''
    Class is window that lists all notifications and displays their details.
    '''
    def __init__(self, parent: typing.Optional[QWidget] = None, flags: typing.Union[QtCore.Qt.WindowFlags, QtCore.Qt.WindowType] = None) -> None:
        try:    
            super(windowNotification, self).__init__(parent)
            self.setWindowTitle("windowNotification")
            self.standardSize = (600, 300)
            self.resize(*self.standardSize)
            self.setWindowIcon(QApplication.style().standardIcon(QStyle.SP_MessageBoxInformation))
            
            self.centralwidget = QWidget(self)
            self.centralwidget.setAutoFillBackground(True)
            self.centralwidget.setObjectName("centralwidget")
            self.gridLayout = QGridLayout(self.centralwidget)
            self.gridLayout.setObjectName("gridLayout")
            
            # TODO: fix
            self.NotificationsWidget = NotificationsWidget(self)
            self.NotificationsWidget.setObjectName("NotificationsWidget")
            self.gridLayout.addWidget(self.NotificationsWidget, 0, 0)
            
            self.setCentralWidget(self.centralwidget)
            
            self.setAutoFillBackground(True)
        except exceptions:
            exception(sys.exc_info())

class NotificationsWidget(QSplitter):
    """
    This widget displays all notifications and allows (read)access to their details. \n
    All previous notifications are automatically loaded and all new notifications are automatically added
    """
    def __init__(self, parent=None):
        super(NotificationsWidget, self).__init__(parent)
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(20)
        #sizePolicy.setHeightForWidth(self.Splitter.sizePolicy().hasHeightForWidth())
        #self.Splitter.setSizePolicy(sizePolicy)
        self.setOrientation(QtCore.Qt.Horizontal)
        self.NotificationList = NotificationListWidget(self)
        self.NotificationInfo = NotificationInfoWidget(self)
        self.NotificationList.setObjectName("NotificationList")
        self.NotificationInfo.setObjectName("NotificationInfo")
        
        App().S_New_Notification.connect(self.AddNotification)
        for i in App().Notification_List:
            self.AddNotification(i)
        
        self.NotificationList.currentItemChanged.connect(self.NotificationInfo.ShowNotificationDetails)

    def AddNotification(self,Notification):
        try:
            item = QListWidgetItem()
            item.setText(str(Notification))
            item.setData(100,Notification)
            item.setIcon(Notification.icon)
            
            self.NotificationList.addItem(item)
            self.NotificationList.scrollToBottom()
        except exceptions:
            Error = exception(sys.exc_info())
            text = "Could not add notification: "+Error
            item = QListWidgetItem()
            item.setText(text)
            item.setData(100, NC(1,"Could not add notification",err=Error,func=str(self.objectName())+".(NotificationsWidget).AddNotification",win=self.window().windowTitle()))
            
            self.NotificationList.addItem(item)
            self.NotificationList.scrollToBottom()

class ListWidget(QListWidget):
    """
    The base class for list widgets of AGeLib. \n
    QtGui.QKeySequence.Copy has been reimplemented to allow copying of multiple items. (Text of items is separated by linebreaks.) \n
    The scrollmode is set to ScrollPerPixel and the selectionmode is set to ExtendedSelection.
    """
    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.installEventFilter(self)

    def keyPressEvent(self,event):
        try:
            if event == QtGui.QKeySequence.Copy:
                SelectedItems = self.selectedItems()
                if len(SelectedItems)>1:
                    string = ""
                    for i in SelectedItems:
                        string += i.text()
                        string += "\n"
                    Qt.QApplication.clipboard().setText(string)
                    event.accept()
                    return
            super(ListWidget, self).keyPressEvent(event)
        except exceptions:
            NC(lvl=2,exc=sys.exc_info(),win=self.window().windowTitle(),func=str(self.objectName())+".(ListWidget).keyPressEvent",input=str(event))
            super(ListWidget, self).keyPressEvent(event)

class NotificationListWidget(ListWidget):
    """
    This widget is used by NotificationsWidget to display all notifications.
    """
    def __init__(self, parent=None):
        super(NotificationListWidget, self).__init__(parent)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setAlternatingRowColors(True)

class NotificationInfoWidget(ListWidget): #TODO: Add a button to copy the details of the current notification to the clipboard with a tooltip that explains how to send it to the developer
    """
    This widget is used by NotificationsWidget to display the details of the currently selected notification.
    """
    def __init__(self, parent=None):
        super(NotificationInfoWidget, self).__init__(parent)
        self.setAlternatingRowColors(True)
        self.installEventFilter(self)
        
        item = QListWidgetItem()
        item.setText("For more information select a notification")
        self.addItem(item)


