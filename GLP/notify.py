# General Library Pre-Build QApplication
# Notify file
Author = "Alex Povod"
Version = "0.0.1"
Domain = "https://github.com/ialexpovod/GLP"

# Python Traceback
# https://www.geeksforgeeks.org/python-traceback/

import datetime
import os
import sys
# Support for regular expressions (RE).
# This module provides regular expression matching operations similar to those found in Perl. It supports both 8-bit and Unicode strings; 
# both the pattern and the strings being processed can contain null bytes and characters outside the US ASCII range.

import re               # RegEx module
import traceback        # Extracting, formating and printing information about Python stack traces.
from PyQt5 import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QStyle)

exceptions = (TypeError , SyntaxError, re.error ,  AttributeError , ValueError , NotImplementedError , Exception , RuntimeError , ImportError)


class NotificationEvent(QtCore.QEvent):
    EVENT_TYPE = QtCore.QEvent.Type(QtCore.QEvent.registerEventType())
    def __init__(self, N):
        QtCore.QEvent.__init__(self, NotificationEvent.EVENT_TYPE)
        self.N = N


class Notify():
    '''
    Basic Notify class of GLP. All notifications are saved and accesible through a notify window, which
    opens by clicks on the notify button of any window. Notifications are used to interaction with the user
    and can be used to handle exceptions because they provide a location for the entire error report.

    Notification component (this module) can produce all information from exceptions. 
    
    Notify is flexiable. Fuul example:
    Notify(1, "Error! Could not save file (picture)")
    Notify(2, "Error! Could not save file (picture)")
    Notify("Error! Could not save file (picture)")
    Notify("Error! Could not save file (picture)", tracebak = True)
    Notify("Error! Could not save file (picture)", exc = sys.exc_info()))

    Levels:
    -  0 = NULL
    -  1 = Error
    -  2 = Warning
    -  3 = Notification
    -  4 = Enhanced Mode Notification
    -  5 = Direct Input Notification 

    '''
    def __init__(self, level = None, message = None , time = None, input = None, error = None, traceback = None, exc = None, wfunction = None, 
    window = None, displayDirect = None, send = True):
        self.initializeValues()
        self._was_send = False
        try:
            self._time = datetime.datetime.now() if time == None else time
            self.TimeStr = self._time.strftime('%H:%M:%S')
            self._displayDirect = displayDirect
            self._window = window
            self._function = wfunction
            self._input = input
            if exc != None:
                if exc == True:
                    self.exc_type, self.exc_obj, self.exc_tb = sys.exc_info()
                else:
                    self.exc_type, self.exc_obj, self.exc_tb = exc
                fileName = os.path.split(self.exc_tb.tb_frame.f_code.co_filename)[1]
                if type(level) == str:
                    self._level = 1
                    self._message = level 
                elif message == None and type(level) == tuple:
                    self._level, self._message = level[0], level[1]
                else:
                    self._level = 1 if level == None else level
                    self._message = str(message) if message != None else None
                self._traceback = str(self.exc_type) +"  in " + str(fileName) +"  line " + str(self.exc_tb.tb_lineno)+"\n\n"+str(traceback.format_exc())
                
                print(self.TimeStr,":")
                if len(str(self.exc_obj))<150:
                    self._error = str(self.exc_type) + ": " + str(self.exc_obj)
                    print(self.exc_type, " in", fileName, " line", self.exc_tb.tb_lineno,": ", self.exc_obj)
                else:
                    self._error = str(self.exc_type)
                    self.ErrorLongDesc = str(self.exc_obj)
                    print(self.exc_type, " in", fileName, " line", self.exc_tb.tb_lineno)
            else:
                if type(level)==str:
                    self._level = 3
                    self._message = level
                elif message == None and type(level) == tuple:
                    self._level, self._message = level[0], level[1]
                else:
                    self._level = 3 if level == None else level
                    self._message = str(message) if message != None else None
                self._error = error
                if traceback == True:
                    self._traceback = ""
                    try:
                        for i in traceback.format_stack()[0:-1]:
                            self._traceback += str(i)
                    except:
                        self._traceback = str("Could not extract callstack")
                else:
                    self._traceback = traceback
            self.GenerateLevelName()
            if send == True:
                self.send()
        except Exception as ex:
            self.initializeValues()
            print(str(datetime.datetime.now().strftime('%H:%M:%S')),": An exception occurred while trying to create a notification")
            print(ex)
            self._time = datetime.datetime.now() if time == None else time
            self.TimeStr = self._time.strftime('%H:%M:%S')
            self._message = "An exception occurred while trying to create a notification"
            self.exc_obj = ex
            self._error = str(ex)
            self.GenerateLevelName()
            self.send(force = True) # Display Notification 

    def initializeValues(self):
        self.exc_type, self.exc_obj, self.exc_tb = None, None, None
        self._time, self.TimeStr, self._error = None,None,None
        self._window, self._traceback, self._function = None,None,None
        self._level, self.Level, self._message = 1,"Notification level 1",None
        self._input, self.ErrorLongDesc = None,None
        self._displayDirect, self._ttstr = None,None
        self.icon = QtGui.QIcon()
        try:
            self.Flash = QApplication.instance().NCF_NONE
        except exceptions as ex:
            print(ex)
            self.Flash = None
        
        self._itemsDictionary = {   "Time:\n":              self.TimeStr,
                                    "Level: ":              self.Level,
                                    "Message:\n":           self._message,
                                    "Error:\n":             self._error,
                                    "Error Description:\n": self.ErrorLongDesc,
                                    "Error Traceback:\n":   self._traceback,
                                    "Function:\n":          self._function,
                                    "Window:\n":            self._window,
                                    "Input:\n":             self._input
                                    }
    
    def GenerateLevelName(self):
        """
        Generates str(self.Level) from int(self.level)
        -  0 = NULL
        -  1 = Error
        -  2 = Warning
        -  3 = Notification
        -  4 = Enhanced Mode Notification
        -  5 = Direct Input Notification 
        """
        try:
            if self._level == 0:
                self.Level = str("None Notification")
                self.icon = QtGui.QIcon()
                self.Flash = QApplication.instance().NCF_NONE
            elif self._level == 1:
                self.Level = str("Error")
                self.icon = QApplication.style().standardIcon(QStyle.SP_MessageBoxCritical)
                self.Flash = QApplication.instance().NCF_r
            elif self._level == 2:
                self.Level = str("Warning")
                self.icon = QApplication.style().standardIcon(QStyle.SP_MessageBoxWarning)
                self.Flash = QApplication.instance().NCF_y
            elif self._level == 3:
                self.Level = str("Notification")
                self.icon = QApplication.style().standardIcon(QStyle.SP_MessageBoxInformation)
                self.Flash = QApplication.instance().NCF_b
            elif self._level == 4:
                self.Level = str("Enhanced Mode Notification")
                self.icon = QApplication.style().standardIcon(QStyle.SP_MessageBoxInformation)
                self.Flash = QApplication.instance().NCF_b
            elif self._level == 10:
                self.Level = str("Direct Input Notification") 
                self.icon = QtGui.QIcon()
                self.Flash = QApplication.instance().NCF_NONE
            else:
                self.Level = str("Notification level") + str(self.level)
                self.Flash = QApplication.instance().NCF_b
            return self.Level
        except exceptions as ex:
            print(ex)
            return str("Could not generate Level Name")

    def send(self, force = False):

        """
        Send = Display Notification. 
        """ 

    def items(self):
        """
        Metdod that return .iems of dictionary argument notification.
        """
        self._itemsDictionary = {   "Time:\n":                      self.TimeStr,
                                    "Level:                         ":"({})\n{}".format(str(self._level),self.Level),
                                    "Message:\n":                   self._message,
                                    "Error:\n":                     self._error,
                                    "Error Description:\n":         self.ErrorLongDesc,
                                    "Error Traceback:\n":           self._traceback,
                                    "Function:\n":                  self._function,
                                    "Window:\n":                    self._window,
                                    "Input:\n":                     self._input,
                                    "Versions:\n":                  QApplication.instance().ModuleVersions
                                    }

        return self._itemsDictionary.items()            

    def unpack(self):
        return (self._level, str(self._message), self.TimeStr)



    def lvl(self, level = None):
        '''
        Access to class argument Level.
        
        return: int(level)
        An int can be given to change the level.
        '''
        if level != None:
            self._level = level
            self.GenerateLevelName()
        return self._level

    def msg(self, message = None): 
        '''
        Access to class argument Message.

        return: str(Message)  \n
        A str can be given to change the Message.
        '''
        
        if message != None:
            self._message = str(message)
        if self._message == None and self._error != None:
            return str(self._error)
        else:
            return str(self._message)

    def time(self, time = None):
        '''            
        Access to class argument Time.

        return: time as %H:%M:%S 
        datetime.datetime.now() can be given to change the time
        '''
        if time != None:
            self._time = time
            self.TimeStr = self._time.strftime('%H:%M:%S')
        return self.TimeStr 
    def err(self, error = None, ErrorTraceback = None):
        '''
        Acces to class arguments Error and Traceback.
        Traceback is a report containing the function calls made in code at a specific point i.e.

        return: str(Error)
        strings can be given to change the Error and ErrorTraceback
        '''
        if error != None:
            self._error = str(error)
        if ErrorTraceback != None:
            self._traceback = str(ErrorTraceback)
        return str(self._error)

    def func(self, function = None):
        '''
        Acces to class argument Function.

        return: str(Function)
        A str can be given to change the Function
        Function is the name of the function from which this notification originates

        '''
        if function != None:

            self._function = str(function)
        return str(self._function)

    def inp(self, input=None):
        '''
        Acces to class argument Input.

        return: str(Input)
        A str can be given to change the Input  \n
        Input is the (user-)input that caused this notification
        '''
        
        if input != None:
            self._input = str(input)
        return str(self._input)

    def win(self, window = None):
        '''
        Returns str(Window)  \n
        A str can be given to change the Window  \n
        Window is the name of the window from which this notification originates  
        '''
        if window != None:
            self._window = str(window)
        return str(self._window)

        
    def trb(self, traceback = None):
        '''
        Acces to class argument Traceback.

        return: str(ErrorTraceback)
        A str can be given to change the ErrorTraceback        
        '''
        if traceback != None:
            self._traceback = str(traceback)
        return str(self._traceback)

    def dps(self, displayDirect = None):
        '''
        Acces to class argument _displayDirect (displayed directly in view string).

        return: str(_displayDirect)
        _displayDirect is the string that is intended to be displayed directly
        A str can be given to change the _displayDirect
        '''
        if displayDirect != None:
            self._displayDirect = str(displayDirect)
        elif self._displayDirect == None:
            if self._level == 10:
                self._displayDirect = self.msg()
            else:
                self._displayDirect = self.Level + " at " + self.time()
        return str(self._displayDirect)

    def tts(self, ttstr = None):
        '''
        Acces to class arguments ttstr (the tool tip in view string).

        return: str(TTStr)
        TTStr is the string that is intended to be displayed as the tool tip   \n
        A str can be given to change the TTStr
        
        '''
        if ttstr != None:
            self._ttstr = str(ttstr)
        elif self._ttstr == None:
            if self._level == 10:
                self._ttstr = self.Level + " at " + self.time()
            else:
                self._ttstr = self.msg()
        return str(self._ttstr)
