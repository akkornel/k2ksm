'''
Created on May 9, 2014

@author: akkornel
'''

import logging
import logging.handlers
from sys import platform, stderr


class K2Logger(object):
    '''
    K2Logger handles all program logging for K2KSM.  Logging goes to
    standard output and/or syslog, depending on how it is configured by the
    K2KSM server.  The K2KSM server also has access to the full suite of Logger
    options, including setting the minimum severity required for messages to be
    logged.
    
    SECURITY NOTE: If debug logging is enabled, log messages WILL include
    sensitive data!
    '''


    def __init__(self, namePrefix='k2ksm'):
        '''
        Constructor.  Creates and configures the top-level Logger object.
        
        Normally, this class should only be instantiated once per program, by
        the server.  Modules should be given a reference to an instance of this
        class, and then they can call the loggerForModule() method to get a
        Logger object of their own.
        
        @param namePrefix: This is the prefix that is used as the
        "program name" for log messages.  This defaults to "k2ksm", but it
        should typically be set to something like "k2ksm-private" or
        "k2ksm-public".  It needs to be something that can become a string, or
        else a TypeError will be thrown.
        
        @raise TypeError: Thrown if namePrefix can not be treated as a string.
        '''
        
        # Set up the logger
        try:
            self.__namePrefix = str(namePrefix)
        except:
            raise TypeError('namePrefix must support str()')
        
        self.__logger = logging.getLogger(self.__namePrefix)
        self.__logger.propagate = False
        
        # Prepare for logging to stderr
        self.__logStderrHandler = logging.StreamHandler(stderr)
        self.__logger.addHandler(self.__logStderrHandler)
        
        # Prepare for logging to syslog/event log
        if (platform[:3] == 'win'):
            try:
                self.__logSyslogHandler = logging.handlers.NTEventLogHandler(self.__namePrefix)
            except:
                    self.__logSyslogHandler = None
        else:
            self.__logSyslogHandler = logging.handlers.SysLogHandler(None, logging.handlers.SysLogHandler.LOG_AUTHPRIV)
        
        
    '''
    @ivar namePrefix: This is the name of the base Logger object.
    This defaults to "k2ksm", so log messages will appear to be coming from
    the program named "k2ksm".  This should normally be set to something
    more specific, like "k2ksm-public" or "k2ksm-private".
    
    namePrefix is set when the class is instantiated.
    Trying to set or change this property will result in a TypeError.
    
    @raise TypeError: Thrown when trying to change or delete this property.
    '''
    __namePrefix = None
    
    @property
    def namePrefix(self):
        return self.__namePrefix
        
        
    '''
    @ivar logger: The topmost Logger object.
    All configuration is applied here, and will be referenced by the
    sub-Loggers that are created later.
    
    @raise TypeError: Thrown if trying to replace or delete.
    '''
    @property
    def logger(self):
        return self.__logger
    
    
    '''
    @ivar logToStderr: A Boolean.  If true, log messages will be sent to
    stderr.  This is set to True when the class is instantiated.
    
    @raise TypeError: Thrown if deleting, or setting to a non-boolean.
    '''
    __logToStderr = True
    
    @property
    def logToStderr(self):
        return self.__logToStderr
    
    @logToStderr.setter
    def logToStderr(self, value):
        if (value == True):
            if (self.__logToStderr == False):
                self.__logger.addHandler(self.__logStderrHandler)
            self.__logToStderr = True
        elif (value == False):
            if (self.__logToStderr == True):
                self.__logStderrHandler.flush()
                self.__logger.removeHandler(self.__logStderrHandler)
            self.__logToStderr = False
        else:
            raise TypeError('logToStderr must be a Boolean')
    
    
    '''
    @ivar logToSyslog: A Boolean.  If true, log messages will be sent to
    stderr.  This is set to False when the class is instantiated.
    
    If running Windows, we try to send to the NT event log instead.  If the
    Win32 extensions for Python don't exist, we will throw a
    NotImplementedError.
    
    @raise TypeError: Thrown if deleting, or setting to a non-boolean.
    
    @raise NotImplementedError: Thrown if trying to set to True on a
    Windows platform, when the Win32 extensions for Python aren't
    available.
    '''
    __logToSyslog = False
    
    @property
    def logToSyslog(self):
        return self.__logToSyslog
    
    @logToSyslog.setter
    def logToSyslog(self, value):
        if (value == True):
            if (self.__logToSyslog == False):
                if (self.__logSyslogHandler == None):
                    raise NotImplementedError('Could not log to the event log, Win32 extensions needed.')
                self.__logger.addHandler(self.__logSyslogHandler)
            self.__logToSyslog = True
        elif (value == False):
            if (self.__logToSyslog == True):
                self.__logSyslogHandler.flush()
                self.__logger.removeHandler(self.__logSyslogHandler)
            self.__logToSyslog = False
        else:
            raise TypeError('logToSyslog must be a Boolean')

    
    def loggerForModule(self, module):
        '''
        Returns a Logger object configured for a particular K2KSM module.
        The Logger object will be pre-configured, so clients should not change
        anything, just call the log-generating methods (critical, debug, etc.)
        as normal!
        
        @param module: A string containing the module name.
        
        @return: A Logger object that has been pre-configured for the module.
        
        @raise TypeError: Thrown if module can not be treated as a string.
        '''
        try:
            newName = str(module)
        except:
            raise TypeError('module must support str()')
        return self.__logger.getChild(newName)


if (__name__ == "__main__"):
    raise NotImplementedError('This file can not be run like a program!')
