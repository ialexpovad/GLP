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
import time
import string
from packaging.version import parse as versionParser


## Mathematical 
import matplotlib
import numpy




# Importing PyQt mudules
from PyQt5.QtWidgets import (QApplication, 
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
                                QStatusBar,
                                QTextEdit,
                                QMessageBox,
                                QFontComboBox,
                                QTabWidget,
                                QTableWidget,
                                QColorDialog,
                                QComboBox,
                                QInputDialog,
                                QCheckBox)
                                
from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QTextCharFormat

# Importing theme module
try:
    from GLP import theme
    from GLP import notify
except ModuleNotFoundError:
    import GLP

exceptions = (
                        TypeError , 
                        SyntaxError , 
                        re.error ,
                        AttributeError, 
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
            return Notification(_exc = exc) # TODO: add natification
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


def cTimeFullStr(separator = None):
    """
    Returns the date and time as a string\n
    If given uses `separator` to separate the values\n
    %Y.%m.%d-%H:%M:%S or separator.join(['%Y','%m','%d','%H','%M','%S'])
    """
    if separator == None:
        return str(datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S'))
    else:
        TheFormat = separator.join(['%Y','%m','%d','%H','%M','%S'])
        return str(datetime.datetime.now().strftime(TheFormat))

AltModifier = QtCore.Qt.AltModifier
ControlModifier = QtCore.Qt.ControlModifier
GroupSwitchModifier = QtCore.Qt.GroupSwitchModifier
ShiftModifier = QtCore.Qt.ShiftModifier
MetaModifier = QtCore.Qt.MetaModifier


class GLPMainApp(QApplication):
    signalColourChanged = QtCore.pyqtSignal()
    signalAdvancedModeChanged = QtCore.pyqtSignal(bool)
    signalFontChanged = QtCore.pyqtSignal()

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
        sys.excepthook = trap_exc_during_debug


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

        self.MainWindow             = None
        self.NotificationWindow     = None
        self.exec_Window            = None
        self.optionWindow           = None
        self.AppPalettes            = {}

        self.installEventFilter(self)
        # TODO: add about to quit

        # TODO: add advanced mode! (boolean)

        self.Notification_List = []


    def setMainWindow(self, win):
        self.MainWindow = win
    
    def eventFilter(self, source, event):
        if event.type() == 6 and self.enableHotkeys: # QtCore.QEvent.KeyPress
            if event.key() == QtCore.Qt.Key_F12:
                if self.GPathOK:
                    name = self.applicationName()
                    nameValid = ""
                    for i in name:
                        if i in string.ascii_letters + string.digits + "~ -_.":
                            nameValid += i
                    nameValid = nameValid.replace(" ","")
                    Filename = nameValid + "-" + cTimeFullStr("-") + ".png"
                    Filename = os.path.join(self.ScreenshotFolderPath,Filename)
                    try:
                        try:
                            WID = source.window().winId()
                            screen = source.window().screen()
                        except:
                            WID = source.winId()
                            screen = source.screen()
                        screen.grabWindow(WID).save(Filename)
                        print(Filename)
                    except:
                        notify.Notify(msg = "Could not save Screenshot", exc=sys.exc_info(), func = "GLPMainApp.eventFilter", input=Filename)
                    else:
                        notify.Notify(3,"Screenshot of currently active window saved as:\n" + Filename, func = "GLPMainApp.eventFilter", input=Filename)
                else:
                    print("Could not save Screenshot: Could not validate save location")
                    notify.Notify(1, "Could not save Screenshot: Could not validate save location",func="GLPMainApp.eventFilter", input=self.GPath)
                return True
            if event.modifiers() == ControlModifier:
                if event.key() == QtCore.Qt.Key_0: # FEATURE: HelpWindow: Inform the User that this feature exists. Make Help window that is opened with F1
                    for w in self.topLevelWidgets():
                        if w.isVisible():
                            w.positionReset()
                    return True
                if event.key() == QtCore.Qt.Key_T:
                    self.Show_exec_Window()
                    return True
            if event.modifiers() == AltModifier:
                if event.key() == QtCore.Qt.Key_A:
                    self.ToggleAdvancedMode(not self.admode)
                    return True
                elif event.key() == QtCore.Qt.Key_O:
                    self.Show_Options()
                    return True
        elif event.type() == notify.NotificationEvent.EVENT_TYPE:
            self._NotifyUser(event.N)
            return True
        return super(GLPMainApp, self).eventFilter(source, event)

    def ToggleAdvancedMode(self, checked):
        try:
            self.admode = checked
            for w in self.topLevelWidgets():
                for i in w.findChildren(QCustomTopBarWidget):
                    if i._includeAdCB:
                        i.AdvancedCB.setChecked(self.admode)
            self.signalAdvancedModeChanged.emit(self.admode)
        except:
            notify.Notify(1,"Exception while toggling advanced mode",
                            exc=sys.exc_info(),func="GLPMain.ToggleAdvancedMode",
                            input="{}: {}".format(str(type(checked)),str(checked)))


    def _MakePath(self):
        self.GPathOK = False
        self.GPath = False
        self.GSettingsPath = False
        self.ScreenshotFolderPath = False
        try:
            self.GPath = os.path.join(os.path.expanduser("~"),"GLP")
            os.makedirs(self.GPath,exist_ok=True)
            #
            self.GSettingsPath = os.path.join(self.GPath,"Settings")#ProgramFiles
            os.makedirs(self.GSettingsPath,exist_ok=True)
            FileName = os.path.join(self.GSettingsPath,"CustomColourPalettes.py")
            with open(FileName,'a',encoding="utf-8") as text_file:
                pass
            if os.stat(FileName).st_size == 0:
                with open(FileName,'w',encoding="utf-8") as text_file:
                    text_file.write(r"Colours={}")
            # Create Screenshots folder
            self.ScreenshotFolderPath = os.path.join(self.GPath,"Screenshots")
            os.makedirs(self.ScreenshotFolderPath,exist_ok=True)
            #
            self.ProgramFilesFolderPath = os.path.join(self.GPath,"ProgramFiles")
            os.makedirs(self.ProgramFilesFolderPath,exist_ok = True)
            self.GPathOK = True
        except:
            notify.Notify(1,"Could not create/validate GLP folder", exc=sys.exc_info())
        try:
            # TODO: ...
            pass
        except:
            notify.Notify(1,"Could not create/validate program specific folders", exc=sys.exc_info())

    def setNotificationWindow(self):
        """
        Shows a window that lists all notifications and displays their details.
        Default access: pressing the notification button
        """
        if self.NotificationWindow == None:
            self.NotificationWindow = Notification_Window()
        self.NotificationWindow.show()
        self.processEvents()
        self.NotificationWindow.positionReset()
        self.processEvents()
        self.NotificationWindow.activateWindow()

    def set_exec_Window(self):
        """
        Shows a window that can execute code within the program. (This window is very useful for debugging) \n
        Default shortcut (applicationwide): ctrl+T
        """
        if self.exec_Window == None:
            self.exec_Window = exec_Window()
        self.exec_Window.show()
        self.processEvents()
        self.exec_Window.positionReset()
        self.processEvents()
        self.exec_Window.activateWindow()

    
    def r_init_Options(self):
        self.optionWindow = Options_Window()

    def Show_Options(self):

        self.optionWindow.show()
        self.optionWindow.activateWindow()


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
                notify.Notify(2,"Could not reload theme",exc=sys.exc_info(),
                    func="Main_App.Recolour",input=str(colour))
            try:    
                spec = importlib.util.spec_from_file_location(  "CustomColourPalettes", 
                                                                os.path.join(self.GPLSettingsPath,
                                                                "CustomColourPalettes.py")
                                                                )
                CustomColours = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(CustomColours)
            except:
                notify.Notify(4,"Could not load custom colours",exc=sys.exc_info(),
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
    
    def SetFont(self, Family = None, PointSize = 0, source = None, emitSignal = True):
        if type(Family) == QtGui.QFont:
            if PointSize == 0:
                PointSize = Family.pointSize()
            Family = Family.family()
            self.FontFamily = Family
        elif Family == None:
            Family = self.FontFamily
        else:
            self.FontFamily = Family
        if type(PointSize) == str:
            PointSize = int(PointSize)
        if PointSize < 5:
            try:
                PointSize = source.TopBar.Font_Size_spinBox.value()
            except exceptions:
                try:
                    notify.Notify(  msg = "Could not read Font_Size_spinBox.value()", 
                                    exc = sys.exc_info(),
                                    func = "GLPMainApp.SetFont",
                                    win = source.windowTitle())
                except exceptions:
                    notify.Notify(  msg = "Could not read Font_Size_spinBox.value()",
                                    exc=sys.exc_info(),
                                    func="GLPMainApp.SetFont")
                PointSize = 9

        if type(PointSize) != int:
            print(type(PointSize)," is an invalid type for font size (",PointSize,")")
            try:
                notify.Notify(  msg="{} is an invalid type for font size ({})".format(str(type(PointSize)),str(PointSize)),
                                exc = sys.exc_info(),
                                func="GLPMainApp.SetFont",
                                win = source.windowTitle())
            except:
                notify.Notify(  msg = "{} is an invalid type for font size ({})".format(str(type(PointSize)),str(PointSize)),
                                exc=sys.exc_info(),
                                func="GLPMainApp.SetFont")
            PointSize = 9
                
        for w in self.topLevelWidgets():
            for i in w.findChildren(QCustomTopBarWidget):
                try:
                    if i.IncludeFontSpinBox:
                        # setValue emits ValueChanged and thus calls ChangeFontSize if the new Value is different from the old one.
                        # If the new Value is the same it is NOT emitted.
                        # To ensure that this behaves correctly either way the signals are blocked while changing the Value.
                        i.Font_Size_spinBox.blockSignals(True)
                        i.Font_Size_spinBox.setValue(PointSize)
                        i.Font_Size_spinBox.blockSignals(False)
                except exceptions:
                    exception(sys.exc_info())
        
        font = QtGui.QFont()
        font.setFamily(Family)
        font.setPointSize(PointSize)
        self.setFont(font)
        for w in self.topLevelWidgets():
            for i in w.findChildren(QCustomTopBarWidget):
                try:
                    if type(i.parentWidget()) == QCustomMenuBar:
                        i.setMinimumHeight(i.parentWidget().minimumHeight())
                    elif type(i.parentWidget()) == QTabWidget:
                        i.setMinimumHeight(i.parentWidget().tabBar().minimumHeight())
                except exceptions:
                    exception(sys.exc_info())
        # Always keep Statusbar Font small
        font = QtGui.QFont()
        font.setFamily(Family)
        font.setPointSize(9)
        for w in self.topLevelWidgets():
            for i in w.findChildren(QStatusBar):
                try:
                    i.setFont(font)
                except exceptions:
                    exception(sys.exc_info())
        if emitSignal:
            self.signalFontChanged.emit()

    def _init_NCF(self): 
        self.NCF_NONE = QtCore.QPropertyAnimation(self)
        
        self.NCF_r = QtCore.QPropertyAnimation(self,b'FLASH_colour')
        self.NCF_r.setDuration(1000)
        self.NCF_r.setLoopCount(1)
        #self.NCF_r.finished.connect(self._NCF_Finished)
        
        self.NCF_y = QtCore.QPropertyAnimation(self,b'FLASH_colour')
        self.NCF_y.setDuration(1000)
        self.NCF_y.setLoopCount(1)
        #self.NCF_y.finished.connect(self._NCF_Finished)
        
        self.NCF_g = QtCore.QPropertyAnimation(self,b'FLASH_colour')
        self.NCF_g.setDuration(1000)
        self.NCF_g.setLoopCount(1)
        #self.NCF_g.finished.connect(self._NCF_Finished)
        
        self.NCF_b = QtCore.QPropertyAnimation(self,b'FLASH_colour')
        self.NCF_b.setDuration(1000)
        self.NCF_b.setLoopCount(1)
        #self.NCF_b.finished.connect(self._NCF_Finished)

    def _update_NCF(self):
        self.NCF_r.setStartValue(self.Palette.color(QtGui.QPalette.Window))
        self.NCF_r.setEndValue(self.Palette.color(QtGui.QPalette.Window))
        self.NCF_r.setKeyValueAt(0.5, self.NotificationColours["Error"].color())
        
        self.NCF_y.setStartValue(self.Palette.color(QtGui.QPalette.Window))
        self.NCF_y.setEndValue(self.Palette.color(QtGui.QPalette.Window))
        self.NCF_y.setKeyValueAt(0.5, self.NotificationColours["Warning"].color())
        
        self.NCF_g.setStartValue(self.Palette.color(QtGui.QPalette.Window))
        self.NCF_g.setEndValue(self.Palette.color(QtGui.QPalette.Window))
        self.NCF_g.setKeyValueAt(0.5, self.NotificationColours["Message"].color())
        
        self.NCF_b.setStartValue(self.Palette.color(QtGui.QPalette.Window))
        self.NCF_b.setEndValue(self.Palette.color(QtGui.QPalette.Window))
        self.NCF_b.setKeyValueAt(0.5, self.NotificationColours["Notification"].color())

    def _set_FLASH_colour(self, col): # Handles changes to the Property FLASH_colour
        palette = self.Palette
        palette.setColor(QtGui.QPalette.Window, col)
        self.setPalette(palette)
    FLASH_colour = QtCore.pyqtProperty(QtGui.QColor, fset=_set_FLASH_colour) # Defines the Property FLASH_colour
    
    #def _NCF_Finished(self):
    #    """
    #    This method is called when a notification flash animation is finished. \n
    #    """
    #    pass#self.TopBar_Error_Label.setFrameShape(QtWidgets.QFrame.NoFrame)

    def _NotifyUser(self, N):
        if N.l() == 0:
            return
        elif N.l()!=4 or self.advanced_mode:
            Error_Text_TT,icon = self._ListVeryRecentNotifications(N)
            self.LastNotificationText = N.DPS()
            self.LastNotificationToolTip = Error_Text_TT
            self.LastNotificationIcon = icon
            for w in self.topLevelWidgets():
                for i in w.findChildren(QCustomTopBarWidget):
                    if i.IncludeErrorButton:
                        i.Error_Label.setText(N.DPS())
                        i.Error_Label.setToolTip(Error_Text_TT)
                        i.Error_Label.setIcon(icon)
            if (not N.Flash == self.NCF_NONE) and (not N.Flash == None):
                N.Flash.start()
        
        self.Notification_List.append(N)
        self.S_New_Notification.emit(N)
        for w in self.topLevelWidgets():
            for i in w.findChildren(QCustomTopBarWidget):
                if i.IncludeErrorButton:
                    i.parentWidget().adjustSize()

    def _ListVeryRecentNotifications(self, N):
        cTime = time.time()
        Error_Text_TT = N.TTS()
        level = N.l()
        icon = N.icon
        for i in range(len(self.Notification_List)):
            if i< 10 and cTime - self.Notification_List[-i-1]._time_time < 2 and len(Error_Text_TT.splitlines())<40:
                if self.Notification_List[-i-1].l()!=0 and (self.Notification_List[-i-1].l()!=4 or self.advanced_mode):
                    Error_Text_TT += "\n\n"
                    Error_Text_TT += str(self.Notification_List[-i-1])
                    cTime = self.Notification_List[-i-1]._time_time
                    if level > self.Notification_List[-i-1].l():
                        level = self.Notification_List[-i-1].l()
                        icon = self.Notification_List[-i-1].icon
            else:
                break
        return (Error_Text_TT,icon)


    def popUpWindowNotinification(self):
        if self.winNotif == None:
            self.winNotif = windowNotification()# TODO: create subclass by QMainWindow 
        self.winNotif.show()
        self.processEvents()
        self.winNotif.positionReset()
        self.processEvents()
        self.winNotif.activateWindow()

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
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint, True)
        
    
        self.GPLWidget = customQFrameWidget(self)
        self.gridLayGPLWidget =  QGridLayout(self.GPLWidget)
        self.gridLayGPLWidget.setContentsMargins(0, 0, 0, 0)
        self.gridLayGPLWidget.setSpacing(0)
        self.gridLayGPLWidget.setObjectName("gridLayout")
        self.GPLWidget.setLayout(self.gridLayGPLWidget)
        
        self.centrWindowWidget = QMainWindow(self)
        self.gridLayGPLWidget.addWidget(self.centrWindowWidget,1,0)
        super(GLPWindow, self).setCentralWidget(self.GPLWidget)

        self.m_menuBar = None
        self.m_centralWidget = None
        self.m_StatusBar = None
        self.BarsHidden = False

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

    def setMenuBar(self, menubar):
        if menubar == None:
            try:
                self.centrWindowWidget.setMenuBar(None)
            except exceptions:
                pass
        else:
            self.centrWindowWidget.setMenuBar(menubar)
            menubar.setCursor(menubar.cursor())
        self.m_menuBar = menubar
        return True

    def menuBar(self):
        return self.centrWindowWidget.menuBar()

    def setCentralWidget(self, CentralWidget):
        if CentralWidget == None:
            try:
                self.centrWindowWidget.setCentralWidget(None)
            except exceptions:
                pass
        else:
            self.centrWindowWidget.setCentralWidget(CentralWidget)
            CentralWidget.setCursor(CentralWidget.cursor())
        self.m_centralWidget = CentralWidget
        return True

    def centralWidget(self):
        return self.centrWindowWidget.centralWidget()

    def setStatusBar(self, StatusBar):
        if StatusBar == None:
            try:
                self.centrWindowWidget.setStatusBar(None)
            except exceptions:
                pass
        else:
            self.centrWindowWidget.setStatusBar(StatusBar)
            StatusBar.setCursor(StatusBar.cursor())
        self.m_StatusBar = StatusBar
        return True

    def statusBar(self):
        return self.centrWindowWidget.statusBar()

    # ToolBar #TODO: Expand
    def addToolBar(self, *ToolBar):
        if ToolBar == None:
            try:
                self.centrWindowWidget.addToolBar(None)
            except exceptions:
                pass
        else:
            self.centrWindowWidget.addToolBar(*ToolBar)
        return True

    def insertToolBar(self, *ToolBar):
        if ToolBar == None:
            try:
                self.centrWindowWidget.insertToolBar(None)
            except exceptions:
                pass
        else:
            self.centrWindowWidget.insertToolBar(*ToolBar)
        return True

    def toolBarArea(self):
        return self.centrWindowWidget.toolBarArea()

    def HideBars(self, boo):
        """
        If boo = True  the menu, top and status bar are permanently hidden. \n
        If boo = False the menu, top and status bar will be shown again. \n
        Hiding these bars is not recommended!
        """
        self.BarsHidden = boo
        self.customQTopBar.setVisible(boo)
        try:
            self.customQMenuBar.setVisible(boo)
        except:
            pass
        try:
            self.customQStatusBar.setVisible(boo)
        except:
            pass
    
    def setTopBarVisible(self,b):
        if not self.BarsHidden:
            self.customQTopBar.setVisible(b)
            try:
                self.customQMenuBar.setVisible(b)
            except:
                pass
            try:
                self.customQStatusBar.setVisible(b)
            except:
                pass

class QCustomMenuBar(QMenuBar):
    '''
    Custom QMenuBar for this library, which can be moveable 
    '''
    def __init__(self, parent = None) -> None:
        super(QCustomMenuBar, self).__init__(parent)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor)) # applies cursor 'Hand'
        self.moving = False
        self.offset = 0
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.actionAt(event.pos()) == None and self.moving == False and self.activeAction() == None:
            self.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            self.offset = event.globalPos()-self.window().geometry().topLeft()
            self.window().GPLWidget.moving = False
            self.moving = True
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
            if (pos.y() < 0):
                pos.setY(0)
                self.window().move(pos)
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
                notify.Notify( exc=sys.exc_info(),
                    win = self.window().windowTitle(),
                    func = "QCustomMenuBar.mouseReleaseEvent")
        else:
            self.moving = False
            super(QCustomMenuBar, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self,event):
        if self.moving:
            event.accept()
            self.window().GPLWidget.moving = False
            if (self.window().isMaximized() or self.window().isFullScreen()):
                try:
                    # TODO: fix bug with maximize button 
                    self.window().QCustomTopBarWidget.custMaxBtn.setText("□")
                except exceptions:
                    pass # TODO: 
                corPos = self.window().geometry().topRight()
                self.window().showNormal()
                self.window().GPLwidget.inFrame()
                QApplication.instance().processEvents()
                self.window().move(corPos-self.window().geometry().topRight() + 
                                self.window().geometry().topLeft())
                self.offset = event.globalPos() - self.window().geometry().topLeft()
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
        self.moving = False
        self.offset = 0

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

        self.ButtonSizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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

        if self._includeAdCB:
            self.AdvancedCB = QCheckBox(self)
            self.AdvancedCB.setText("")
            self.AdvancedCB.setToolTip("Advanced Mode (alt+A)")
            self.AdvancedCB.setChecked(QApplication.instance().advanced_mode)
            self.AdvancedCB.setObjectName("AdvancedCB")
            self.layout().addWidget(self.AdvancedCB, 0, 102, 1, 1,QtCore.Qt.AlignRight)
            self.AdvancedCB.clicked.connect(QApplication.instance().ToggleAdvancedMode)

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

    def eventFilter(self, source, event):
        if event.type() == 10 or event.type() == 11:
            if source == self.custCloseBtn:
                if event.type() == QtCore.QEvent.Enter:#HoverMove
                    self.custCloseBtn.setPalette(self.RedHighlightPalette)
                elif event.type() == QtCore.QEvent.Leave:#HoverLeave
                    self.custCloseBtn.setPalette(self.palette())
            elif source == self.custMaxBtn:
                if event.type() == QtCore.QEvent.Enter:
                    self.custMaxBtn.setAutoRaise(False)
                elif event.type() == QtCore.QEvent.Leave:
                    self.custMaxBtn.setAutoRaise(True)
            elif source == self.custMinBtn:
                if event.type() == QtCore.QEvent.Enter:
                    self.custMinBtn.setAutoRaise(False)
                elif event.type() == QtCore.QEvent.Leave:
                    self.custMinBtn.setAutoRaise(True)
        elif self._includeErrorButton and source is self.error_notification and event.type() == QtCore.QEvent.Enter: #==10
            QToolTip.showText(QtGui.QCursor.pos(),self.error_notification.toolTip(),self.error_notification)
        return super(QCustomTopBarWidget, self).eventFilter(source, event)

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
            item.setData(100, Notification(1,"Could not add notification",err=Error,func=str(self.objectName())+".(NotificationsWidget).AddNotification",win=self.window().windowTitle()))
            
            self.NotificationList.addItem(item)
            self.NotificationList.scrollToBottom()

class ListWidget(QListWidget):
    """
    The base class for list widgets of GLP. \n
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
            notify.Notify(lvl=2,exc=sys.exc_info(),win=self.window().windowTitle(),func=str(self.objectName())+".(ListWidget).keyPressEvent",input=str(event))
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


def trap_exc_during_debug(*args):
    # when app raises uncaught exception, send info
    notify.Notify(1,"An unhandled exception occurred in a QThread!!!", err=str(args))


class GLPTextEdit(QTextEdit):
    returnPressed = QtCore.pyqtSignal()
    returnCtrlPressed = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        QTextEdit.__init__(self, parent)
        self.installEventFilter(self)
        self.setTabChangesFocus(True)
        
    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter: # Connects to returnPressed but does not accept the signal to allow linebreaks
                source.returnPressed.emit()
            if (event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter) and event.modifiers() == QtCore.Qt.ControlModifier:
                source.returnCtrlPressed.emit()
            if event.key() == QtCore.Qt.Key_Up and source.textCursor().blockNumber() == 0: # Move to beginning if up key pressed and in first line
                cursor = source.textCursor()
                if event.modifiers() == QtCore.Qt.ShiftModifier: # If shift is pressed select the text
                    cursor.movePosition(cursor.Start,1)
                else:
                    cursor.movePosition(cursor.Start)
                source.setTextCursor(cursor)
                return True
            elif event.key() == QtCore.Qt.Key_Down and source.textCursor().blockNumber() == source.document().blockCount()-1: # Move to end if down key pressed and in last line
                cursor = source.textCursor()
                if event.modifiers() == QtCore.Qt.ShiftModifier: # If shift is pressed select the text
                    cursor.movePosition(cursor.End,1)
                else:
                    cursor.movePosition(cursor.End)
                source.setTextCursor(cursor)
                return True
        return super(GLPTextEdit, self).eventFilter(source, event)

    def text(self):
        return self.toPlainText()

    def insertFromMimeData(self, MIMEData):
        try:
            Text = MIMEData.text()
            self.textCursor().insertText(Text)
        except exceptions:
            # TODO: ...
            pass


class TextEdit(GLPTextEdit):
    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)
        self.installEventFilter(self)
    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if (event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter) and event.modifiers() == QtCore.Qt.ControlModifier:
                source.returnCtrlPressed.emit()
                return True
        return super(TextEdit, self).eventFilter(source, event)


class Notification_Window(GLPWindow):
    def __init__(self,parent = None):
        try:
            super(Notification_Window, self).__init__(parent)
            self.setWindowTitle("Notifications")
            self.standardSize = (900, 500)
            self.resize(*self.standardSize)
            self.setWindowIcon(QApplication.style().standardIcon(QStyle.SP_MessageBoxInformation))
            
            self.centralwidget = QWidget(self)
            self.centralwidget.setAutoFillBackground(True)
            self.centralwidget.setObjectName("centralwidget")
            self.gridLayout = QGridLayout(self.centralwidget)
            self.gridLayout.setObjectName("gridLayout")
            
            self.NotificationsWidget = NotificationsWidget(self)
            self.NotificationsWidget.setObjectName("NotificationsWidget")
            self.gridLayout.addWidget(self.NotificationsWidget, 0, 0)
            
            self.setCentralWidget(self.centralwidget)
            
            self.setAutoFillBackground(True)
        except exceptions:
            exception(sys.exc_info())


class exec_Window(GLPWindow):
    def __init__(self,parent = None):
        try:
            super(exec_Window, self).__init__(parent, initTopBar = False)
            self._topBar.initialize(    IncludeFontSpinBox  = True,
                                        IncludeErrorButton  = True,
                                        IncludeAdvancedCB   = True)

            self.setWindowTitle("Code Execution Window")
            self.standardSize = (900, 500)
            self.resize(*self.standardSize)
            self.setWindowIcon(QApplication.style().standardIcon(QStyle.SP_ComputerIcon))
                
            self.centralwidget = QWidget(self)
            self.centralwidget.setAutoFillBackground(True)
            self.centralwidget.setObjectName("centralwidget")
            self.gridLayout = QGridLayout(self.centralwidget)
            self.gridLayout.setObjectName("gridLayout")
            
            self.Input_Field = TextEdit(self)
            self.Input_Field.setObjectName("Input_Field")
            self.Input_Field.setTabChangesFocus(False)
            self.Input_Field.setText("# If you have Spyder installed use this to activate the 'Spyder/Dark' syntax highlighter:\nself.highlight()")
            
            self.gridLayout.addWidget(self.Input_Field, 0, 0, 0, 0)
            self.gridLayout.setContentsMargins(0,0,0,0)
            self.setCentralWidget(self.centralwidget)

            self.Input_Field.returnCtrlPressed.connect(self.execute_code)
            
            self.setAutoFillBackground(True)
        except exceptions:
            notify.Notify(exc=sys.exc_info(),win=self.windowTitle(),func="exec_Window.__init__")

    def execute_code(self):
        input_text = self.Input_Field.toPlainText()
        try:
            # Set app and window for the local dictionary so that they can be used in the execution
            app = QApplication.instance() # pylint: disable=unused-variable
            window = QApplication.instance().MainWindow # pylint: disable=unused-variable
            exec(input_text)
        except exceptions:
            notify.Notify(exc=sys.exc_info(),win=self.windowTitle(),func="exec_Window.execute_code",input=input_text)

    def highlight(self):
        try:
            # TODO: ...
            from spyder.utils.syntaxhighlighters import PythonSH
            self.Input_Field_Highlighter = PythonSH(self.Input_Field.document(),color_scheme='Spyder/Dark')
        except:
            pass

class Options_Window(GLPWindow):
    def __init__(self, parent = None):
        #REMINDER: Add more tabs with other option stuff...
        try:
            super(Options_Window, self).__init__(parent, _include_QTopBar = False)
            self.customQTopBar.initialize(_includeFontSpinBox = True, _includeErrorButton = True, _includeAdCB = True)
     
            self.setWindowTitle("Options Window")
            self.standardSize = (700, 500)
            self.resize(*self.standardSize)
            self.setWindowIcon(QApplication.style().standardIcon(QStyle.SP_ComputerIcon))
            
            self.centralwidget = QWidget(self)
            self.centralwidget.setAutoFillBackground(True)
            self.centralwidget.setObjectName("centralwidget")
            self.gridLayout = QGridLayout(self.centralwidget)
            self.gridLayout.setObjectName("gridLayout")
            self.Input_Field = OptionsWidget_1_Appearance(self)
            self.Input_Field.setObjectName("Input_Field")
            
            self.gridLayout.addWidget(self.Input_Field, 0, 0, 0, 0)
            self.gridLayout.setContentsMargins(3,3,3,3)
            self.setCentralWidget(self.centralwidget)
            
            self.setAutoFillBackground(True)
        except exceptions:
            notify.Notify(  exc = sys.exc_info(), 
                            win=self.windowTitle(),
                            func="exec_Window.__init__")


class ColourPicker(QToolButton):
    def __init__(self, Type, Element, parent=None):
        super(ColourPicker, self).__init__(parent)
        self.Type, self.Element = Type, Element
        self.setText("")
        self.LoadCurrentPalette()
        self.clicked.connect(self.PickColour)
        self.setAutoRaise(True)
        self.setAutoFillBackground(True)
        
    def LoadCurrentPalette(self):
        try:
            if self.Type == "Pen":
                self.Colour = QApplication.instance().PenColours[self.Element].color()
            elif self.Type == "Notification":
                self.Colour = QApplication.instance().NotificationColours[self.Element].color()
            elif self.Type == "Misc":
                self.Colour = QApplication.instance().MiscColours[self.Element].color()
        except:
            self.Colour = QtGui.QColor(255, 0, 255)
        self.ColourSelf()
        
    def PickColour(self):
        Colour = QColorDialog.getColor(self.Colour,None,"Choose the {} colour \"{}\"".format(self.Type,self.Element))
        if Colour.isValid(): # If the QColorDialog was aborted by the user the returned colour is invalid
            self.Colour = Colour
        self.ColourSelf()
        
    def ColourSelf(self):
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(self.Colour)
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        # Generate readable text colour
        textColour = QtGui.QColor("black") if (0.299 * self.Colour.red() + 0.587 * self.Colour.green() + 0.114 * self.Colour.blue())/255 > 0.5 else QtGui.QColor("white")
        brush = QtGui.QBrush(textColour)
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.setPalette(palette)
        # Display the HexRgb code of the colour
        #self.setText("#"+str(hex(self.Colour.rgb()))[4:]) # Does the same as the next line
        self.setText(self.Colour.name(0)) # 0 = HexRgb


class PaletteColourPicker(ColourPicker):
    def __init__(self, Mode, Element, ModeText, ElementText, parent=None):
        QToolButton.__init__(self, parent)
        self.Mode, self.Element = Mode, Element
        self.ModeText, self.ElementText = ModeText, ElementText
        self.setText("")
        self.LoadCurrentPalette()
        self.clicked.connect(self.PickColour)
        if self.ElementText != "Button": #MAYBE: Link the Button colour buttons to the ButtonText colour buttons
            self.setAutoRaise(True)
            self.setAutoFillBackground(True)
        
    def LoadCurrentPalette(self):
        try:
            if self.ModeText.endswith("Version 1"):
                self.Colour = QApplication.instance().Palette1.brush(self.Mode, self.Element).color()#QtGui.QColor(255, 255, 255)
            elif self.ModeText.endswith("Version 2"):
                self.Colour = QApplication.instance().Palette2.brush(self.Mode, self.Element).color()#QtGui.QColor(255, 255, 255)
            elif self.ModeText.endswith("Version 3"):
                self.Colour = QApplication.instance().Palette3.brush(self.Mode, self.Element).color()#QtGui.QColor(255, 255, 255)
        except:
            self.Colour = QtGui.QColor(255, 0, 255)
        self.ColourSelf()
        
    def PickColour(self):
        Colour = QColorDialog.getColor(self.Colour,None,"Choose colour for {} when {}".format(self.ElementText,self.ModeText))
        if Colour.isValid(): # If the QColorDialog was aborted by the user the returned colour is invalid
            self.Colour = Colour
        self.ColourSelf()
    
class OptionsWidget_1_Appearance(QWidget):
    def __init__(self, parent=None):
        super(OptionsWidget_1_Appearance, self).__init__(parent)
        self.PaletteColours = []
        self.PenColours = []
        self.NotificationColours = []
        self.MiscColours = []
        
        self.setLayout(QGridLayout())
        self.FontLabel = QLabel(self)
        self.FontLabel.setText("Choose a font:")
        self.FontLabel.setToolTip("The displayed fonts are the fonts that are installed on your copmuter")
        self.layout().addWidget(self.FontLabel,0,0)
        self.fontComboBox = QFontComboBox(self)
        self.fontComboBox.currentFontChanged.connect(self.SetFontFamily)
        self.layout().addWidget(self.fontComboBox,0,1)
        self.ColourListLabel = QLabel(self)
        self.ColourListLabel.setText("Choose a colour palette:")
        self.layout().addWidget(self.ColourListLabel,1,0)
        self.ColourList = QComboBox(self)
        self.ColourList.addItems(self.LoadPaletteList())
        self.ColourList.setCurrentText("Dark")
        if versionParser(QtCore.qVersion()) >= versionParser("5.14"):
            self.ColourList.textActivated.connect(QApplication.instance().Recolour)
        else:
            self.ColourList.currentTextChanged.connect(QApplication.instance().Recolour)
        self.layout().addWidget(self.ColourList,1,1)
        self.ColourTableLabel = QLabel(self)
        self.ColourTableLabel.setText("Or create you own:")
        self.layout().addWidget(self.ColourTableLabel,2,0)
        self.LoadToEditorButton = QPushButton(self)
        self.LoadToEditorButton.setText("Load current palette to editor")
        self.LoadToEditorButton.clicked.connect(lambda: self.LoadCurrentPalette())
        self.layout().addWidget(self.LoadToEditorButton,2,1)
        self.ColourTabs = QTabWidget(self)
        self.layout().addWidget(self.ColourTabs,3,0,1,2)
        self.PaletteTable = QTableWidget(len(theme.PaletteElements),len(theme.PaletteStates),self)
        self.ColourTabs.addTab(self.PaletteTable,"Palettes")
        #self.layout().addWidget(self.PaletteTable,3,0,1,2)
        self.PenTable_Labels = ["Red","Green","Blue","Yellow","Cyan","Magenta","Orange","Light Blue","White","Black"]
        self.PenTable = QTableWidget(len(self.PenTable_Labels),1,self)
        self.PenTable.setVerticalHeaderLabels(self.PenTable_Labels)
        self.ColourTabs.addTab(self.PenTable,"Pen Colours")
        self.NotificationTable_Labels = ["Error","Warning","Notification","Message"]
        self.NotificationTable = QTableWidget(len(self.NotificationTable_Labels),1,self)
        self.NotificationTable.setVerticalHeaderLabels(self.NotificationTable_Labels)
        self.ColourTabs.addTab(self.NotificationTable,"Notification Colours")
        self.MiscTable_Labels = ["Friendly","Hostile","Neutral","Ally","Self",
                                "Common","Uncommon","Rare","Legendary","Mythical","Artefact","Broken","Magical","Important",
                                "Gradient1","Gradient2","Gradient3"]
        self.MiscTable = QTableWidget(len(self.MiscTable_Labels),1,self)
        self.MiscTable.setVerticalHeaderLabels(self.MiscTable_Labels)
        self.ColourTabs.addTab(self.MiscTable,"Misc Colours")
        #
        self.ApplyPaletteButton = QPushButton(self)
        self.ApplyPaletteButton.setText("Apply Palette")
        self.ApplyPaletteButton.clicked.connect(lambda: self.MakePalette())
        self.layout().addWidget(self.ApplyPaletteButton,4,0)
        self.SavePaletteButton = QPushButton(self)
        self.SavePaletteButton.setText("Save Palette")
        self.SavePaletteButton.clicked.connect(lambda: self.SavePalette())
        self.layout().addWidget(self.SavePaletteButton,4,1)
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(3)
        HLabel = ["Active Version 1","Inactive Version 1","Disabled Version 1","Active Version 2","Inactive Version 2","Disabled Version 2","Active Version 3","Inactive Version 3","Disabled Version 3"]
        VLabel = []
        y = 0
        for i, v in theme.PaletteElements.items():
            VLabel.append(i)
            #CLEANUP
            #widget = PaletteColourPicker(AGeColour.PaletteStates["Active"],v,"Active",i,self.PaletteTable)
            #self.PaletteColours.append(widget)
            #self.PaletteTable.setCellWidget(y,0,widget)
            #widget = PaletteColourPicker(AGeColour.PaletteStates["Inactive"],v,"Inactive",i,self.PaletteTable)
            #self.PaletteColours.append(widget)
            #self.PaletteTable.setCellWidget(y,1,widget)
            #widget = PaletteColourPicker(AGeColour.PaletteStates["Disabled"],v,"Disabled",i,self.PaletteTable)
            #self.PaletteColours.append(widget)
            #self.PaletteTable.setCellWidget(y,2,widget)
            x = 0
            for ii, vi in theme.PaletteStates.items():
                widget = PaletteColourPicker(vi,v,ii,i,self.PaletteTable)
                self.PaletteColours.append(widget)
                self.PaletteTable.setCellWidget(y,x,widget)
                x+=1
            y+=1
        self.PaletteTable.setHorizontalHeaderLabels(HLabel)
        self.PaletteTable.setVerticalHeaderLabels(VLabel)
        y = 0
        for i in self.PenTable_Labels:
            widget = ColourPicker("Pen",i,self.PenTable)
            self.PenColours.append(widget)
            self.PenTable.setCellWidget(y,0,widget)
            y+=1
        y = 0
        for i in self.NotificationTable_Labels:
            widget = ColourPicker("Notification",i,self.NotificationTable)
            self.NotificationColours.append(widget)
            self.NotificationTable.setCellWidget(y,0,widget)
            y+=1
        y = 0 
        for i in self.MiscTable_Labels:
            widget = ColourPicker("Misc",i,self.MiscTable)
            self.MiscColours.append(widget)
            self.MiscTable.setCellWidget(y,0,widget)
            y+=1
        
    def SetFontFamily(self,Family):
        QApplication.instance().SetFont(Family,self.window().TopBar.Font_Size_spinBox.value(),self)
        
    def LoadCurrentPalette(self):
        for i in self.PaletteColours+self.PenColours+self.NotificationColours+self.MiscColours:
            i.LoadCurrentPalette()
        #self.PenColours = []
        #self.NotificationColours = []
        #self.MiscColours = []
        
    def LoadPaletteList(self):
        ColourList = []
        try:
            try:
                importlib.reload(theme)
            except:
                notify.Notify(2,"Could not reload theme",exc=sys.exc_info(),func="GLPMainApp.colourSheme")
            try:
                if QApplication.instance().GPathOK:
                    spec = importlib.util.spec_from_file_location("CustomColourPalettes", os.path.join(QApplication.instance().GSettingsPath,"CustomColourPalettes.py"))
                    CustomColours = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(CustomColours)
                    #CustomColours.MyClass()
                else:
                    raise Exception("GPath is not OK")
            except:
                notify.Notify(4,"Could not load custom colours",exc=sys.exc_info(),func="GLPMainApp.colourSheme")
            try:
                for i in theme.Colours.keys():
                    ColourList.append(i)
                for i in CustomColours.Colours.keys():
                    ColourList.append(i)
            except:
                pass
        except:
            notify.Notify(1,"Exception while loading colour palette",exc=sys.exc_info(),func="GLPMainApp.colourSheme")
        return ColourList
        
    def MakePalette(self):
        self.ColourList.blockSignals(True)
        self.ColourList.clear()
        self.ColourList.addItems(self.LoadPaletteList())
        self.ColourList.blockSignals(False)
        palette1,palette2,palette3 = QtGui.QPalette(),QtGui.QPalette(),QtGui.QPalette()
        PenColours , NotificationColours , MiscColours = {},{},{}
        for i in self.PaletteColours:
            brush = QtGui.QBrush(i.Colour)
            brush.setStyle(QtCore.Qt.SolidPattern)
            if int(i.ModeText[-1]) == 1:
                palette1.setBrush(i.Mode, i.Element, brush)
            elif int(i.ModeText[-1]) == 2:
                palette2.setBrush(i.Mode, i.Element, brush)
            elif int(i.ModeText[-1]) == 3:
                palette3.setBrush(i.Mode, i.Element, brush)
        for i in self.PenColours:
            brush = QtGui.QBrush(i.Colour)
            brush.setStyle(QtCore.Qt.SolidPattern)
            PenColours[i.Element] = brush
        for i in self.NotificationColours:
            brush = QtGui.QBrush(i.Colour)
            brush.setStyle(QtCore.Qt.SolidPattern)
            NotificationColours[i.Element] = brush
        for i in self.MiscColours:
            brush = QtGui.QBrush(i.Colour)
            brush.setStyle(QtCore.Qt.SolidPattern)
            MiscColours[i.Element] = brush
            #
        QApplication.instance().colourSheme(palette1 , palette2 , palette3 , PenColours , NotificationColours , MiscColours)
        return palette1 , palette2 , palette3 , PenColours , NotificationColours , MiscColours
    
    def PaletteToPython(self,Palette,FunctionName,Name):
        #window.AMaDiA_About_Window_Window.TextBrowser.setText(app.optionWindow.ColourPicker.PaletteToPython(AGeColour.Colours[app.optionWindow.ColourPicker.LoadPaletteList()[0]],app.optionWindow.ColourPicker.LoadPaletteList()[0])[0])
        Palette1, Palette2, Palette3, _PenColours, _NotificationColours, _MiscColours = Palette()
        PenColours, NotificationColours, MiscColours = ColourDict(),ColourDict(),ColourDict()
        PenColours.copyFromDict(_PenColours)
        NotificationColours.copyFromDict(_NotificationColours)
        MiscColours.copyFromDict(_MiscColours)
        Text = "\ndef "+FunctionName+"():\n    palette1 = QtGui.QPalette()\n    palette2 = QtGui.QPalette()\n    palette3 = QtGui.QPalette()"
        for i, v in theme.PaletteElements.items():
            for ii,iv in theme.PaletteStates.items():
                if int(ii[-1]) == 1:
                    Colour = Palette1.brush(iv, v).color()
                elif int(ii[-1]) == 2:
                    Colour = Palette2.brush(iv, v).color()
                elif int(ii[-1]) == 3:
                    Colour = Palette3.brush(iv, v).color()
                Text += "\n    brush = QtGui.QBrush(QtGui.QColor({},{},{}))".format(str(Colour.red()),str(Colour.green()),str(Colour.blue()))
                Text += "\n    brush.setStyle(QtCore.Qt.SolidPattern)"
                Text += "\n    palette{}.setBrush(QtGui.QPalette.{}, QtGui.QPalette.{}, brush)".format(ii[-1],ii.split()[0],i)
        Text += "\n    PenColours = {"
        for i in self.PenTable_Labels:
            Colour = PenColours[i].color()
            Text += "\n        \"{}\":QtGui.QBrush(QtGui.QColor({},{},{})),".format(i,str(Colour.red()),str(Colour.green()),str(Colour.blue()))
        Text = Text[:-1]+"}\n    NotificationColours = {"
        for i in self.NotificationTable_Labels:
            Colour = NotificationColours[i].color()
            Text += "\n        \"{}\":QtGui.QBrush(QtGui.QColor({},{},{})),".format(i,str(Colour.red()),str(Colour.green()),str(Colour.blue()))
        Text = Text[:-1]+"}\n    MiscColours = {"
        for i in self.MiscTable_Labels:
            Colour = MiscColours[i].color()
            Text += "\n        \"{}\":QtGui.QBrush(QtGui.QColor({},{},{})),".format(i,str(Colour.red()),str(Colour.green()),str(Colour.blue()))
        Text = Text[:-1]+"}\n    return palette1 , palette2 , palette3 , PenColours , NotificationColours , MiscColours\n"
        return Text,FunctionName,Name
    
    def SavePalette(self,Name=None):
        # window.AMaDiA_About_Window_Window.TextBrowser.setText(app.optionWindow.ColourPicker.SavePalette("Test"))
        if Name == None:
            Name = QInputDialog.getText(self,"Palette Name","What should the palette be called?")[0].strip()
            # VALIDATE: Ensure that the names can not break the dictionary
            if Name == None or Name == "":
                notify.Notify(2,"SavePalette has been cancelled")
                return ""
        Text = "from PyQt5 import QtCore, QtGui\n\ndef NewColour():\n    palette1 = QtGui.QPalette()\n    palette2 = QtGui.QPalette()\n    palette3 = QtGui.QPalette()"
        for i in self.PaletteColours:
            Text += "\n    brush = QtGui.QBrush(QtGui.QColor({},{},{}))".format(str(i.Colour.red()),str(i.Colour.green()),str(i.Colour.blue()))
            Text += "\n    brush.setStyle(QtCore.Qt.SolidPattern)"
            Text += "\n    palette{}.setBrush(QtGui.QPalette.{}, QtGui.QPalette.{}, brush)".format(i.ModeText.split()[2],i.ModeText.split()[0],i.ElementText)
        Text += "\n    PenColours = {"
        for i in self.PenColours:
            Text += "\n        \"{}\":QtGui.QBrush(QtGui.QColor({},{},{})),".format(i.Element,str(i.Colour.red()),str(i.Colour.green()),str(i.Colour.blue()))
        Text = Text[:-1]+"}\n    NotificationColours = {"
        for i in self.NotificationColours:
            Text += "\n        \"{}\":QtGui.QBrush(QtGui.QColor({},{},{})),".format(i.Element,str(i.Colour.red()),str(i.Colour.green()),str(i.Colour.blue()))
        Text = Text[:-1]+"}\n    MiscColours = {"
        for i in self.MiscColours:
            Text += "\n        \"{}\":QtGui.QBrush(QtGui.QColor({},{},{})),".format(i.Element,str(i.Colour.red()),str(i.Colour.green()),str(i.Colour.blue()))
        #
        Text = Text[:-1]+"}\n    return palette1 , palette2 , palette3 , PenColours , NotificationColours , MiscColours\n"
        try:
            if not QApplication.instance().GPathOK: raise Exception("GPath is not OK")
            ##
            TheDict = {}
            try:
                nText = Text
                spec = importlib.util.spec_from_file_location("CustomColourPalettes", os.path.join(QApplication.instance().GSettingsPath,"CustomColourPalettes.py"))
                CustomColours = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(CustomColours)
                i=1
                for k,v in CustomColours.Colours.items():
                    fn = "c"+str(i)
                    t,fn,n = self.PaletteToPython(v,fn,k)
                    if n == Name:
                        msgBox = QMessageBox(self)
                        msgBox.setText("\"{}\" already exists".format(Name))
                        msgBox.setInformativeText("Do you want to overwrite \"{}\"?".format(Name))
                        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
                        msgBox.setDefaultButton(QMessageBox.Cancel)
                        ret = msgBox.exec()
                        if ret != QMessageBox.Save:
                            return Text
                        else:
                            continue
                    nText += "\n"
                    nText += t
                    TheDict[n.replace("\\","\\\\").replace("\"","\\\"")] = fn
                    i+=1
            except:
                notify.Notify(2,"Could not load custom colours",exc=sys.exc_info(),func="Main_App.Recolour")
                msgBox = QMessageBox(self)
                msgBox.setText("Could not load previous custom colours!")
                msgBox.setInformativeText("Do you want to save the colour anyways?\nWARNING: This will overwrite any previous colour palettes!!!")
                msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
                msgBox.setDefaultButton(QMessageBox.Cancel)
                ret = msgBox.exec()
                if ret != QMessageBox.Save:
                    return Text
            Text = nText
            ##
            fText = Text+"\nColours = {\""+Name.replace("\\","\\\\").replace("\"","\\\"")+"\":NewColour"
            for k,v in TheDict.items():
                fText += ",\"{}\":{}".format(k,v)
            fText += "}"
            FileName = os.path.join(QApplication.instance().GSettingsPath,"CustomColourPalettes.py")
            with open(FileName,'w',encoding="utf-8") as text_file:
                text_file.write(fText)
        except:
            notify.Notify(1,"Could not save",exc=sys.exc_info())
        self.ColourList.blockSignals(True)
        self.ColourList.clear()
        self.ColourList.addItems(self.LoadPaletteList())
        self.ColourList.blockSignals(False)
        return Text
