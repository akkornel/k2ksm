
from abc import ABCMeta, abstractmethod
from sys import argv
from ..logger import K2Logger



K2_DEFAULT_CONFIG = '/dev/null'
'''
This is the default configuration file location.
Individual distributions should replace the /dev/null source distribution
default with something disto-appropriate.
'''



class K2Settings(object):
    '''
    K2Settings is used to handle server settings, both for the K2KSM server
    and for individual modules.  K2Settings pulls configuration from the
    command line as well as settings files.  Each module provides their own
    list of valid settings, as well as handling changes.
    
    The typically life-cycle for this module is:
    
    1) Server instantiates the module and loads initial settings
    
    2) Server loads individual modules and passes the instance to the module's
    register() method.
    
    3) Module treats the settings instance as a hash, adding a new key (its
    module ID), with the value being a K2SettingsModule object.
    
    4) Settings are checked & changed as needed.
    '''

    __unusedSettings = {}
    '''
    @ivar: A 2-dimensional array of settings that have been
    pulled in by L{loadArgs} or L{loadConfig}, but which haven't
    yet been given to a module (because the module hasn't registered yet).
    Only server-wide settings can be placed here.
    '''

    __moduleSettings = {}
    '''
    @ivar: A hash of a hash of K2SettingsModule objects.  The first key is
    the name of the module; the second key is the session ID (to store session-
    specific settings), or zero (to store server-wide settings).
    '''
    
    finalized = False
    '''
    @ivar: Set to true once all modules have been registered.
    @type: Boolean
    '''
    
    logger = None
    '''
    @ivar: A K2Logger object that we can use.
    @type: K2Logger
    '''
    
    configArgs = None
    '''
    @ivar: The source of command-line arguments.
    This is set when loadArgs() is called.  If set to None, then loadArgs()
    was never called.
    @type: String
    '''
    
    configPath = None
    '''
    @ivar: The path to the configuration file.
    This is set when loadConfig is called.  If set to None, then loadConfig()
    was never called.
    @type: String
    '''

    
    def __init__(self, logger):
        '''
        Create a new K2Settings object for settings storage.
        
        @param logger: A K2Logger object, which we can use to create a
        logging.logger object for ourselves.
        @type logger: K2Logger
        
        @rtype: K2Logger
        @return: A new empty K2Logger object.
        
        @raise TypeError: Thrown if logger is not a K2Logger object.
        '''
        
        # Just set up the logger
        if (not isinstance(logger, K2Logger)):
            raise TypeError('logger must be a K2Logger object')
        self.logger = logger.loggerForModule('Settings')
        self.logger.debug('K2Settings instantiated')
    
    
    def loadArgs(self, args=argv):
        '''
        Load settings from a list of arguments.
        A list of arguments can be provided for parsing, otherwise sys.argv
        is used.
        
        Arguments must appear in the following form::
        
            moduleName.settingName settingValue
            
        That means the total number of arguments will be 2 times the number of
        settings.
        
        If called without args being specified, C{sys.argv} will be used.
        
        @param args: An even-numbered list of arguments.
        @type args: List
        
        @raise IndexError: Thrown if an odd-numbered list of arguments
        is provided.
        '''
        self.logger.info('Parsing command-line arguments')
        self.configArgs = args
        if (len(self.configArgs) % 2 != 0):
            raise IndexError('args must have an even number of items')
        
        i = 0
        while (i < len(self.configArgs)):
            lvalue = self.configArgs[i]
            settingValue = self.configArgs[i + 1]
            moduleName, settingName = lvalue.split('.', 1)
            
            if (moduleName not in self.__unusedSettings):
                self.__unusedSettings[moduleName] = {}
                
            self.__unusedSettings[moduleName][settingName] = settingValue
            self.logger.debug('Added setting %s.%s=%s' % (
                             moduleName, settingName, settingValue
                             ))
            
            i += 2
    
    
    def loadConfig(self, config=K2_DEFAULT_CONFIG):
        '''
        Load settings from a .ini-style configuration file.
        If the configuration file to use is not provided, then the default
        L{K2_DEFAULT_CONFIG} will be used instead.
        
        @param config: The path to an .ini-style configuration file.
        @type config: String
        '''
        self.logger.info('Loading configuration from path ' + config)
        self.configPath = config
        # TODO
    
    
    @classmethod
    def load(cls, logger, args=None, config=None):
        '''
        A convenience method to create & configure a L{K2Settings} object.
        Creates a new L{K2Settings} object, calls L{loadArgs}
        and L{loadConfig}, and then returns the newly-made class.  This method
        will use the defaults for C{args} and C{config}; if you want an empty
        L{K2Settings} object, you should just create a new one of your own.
        
        @param logger: A L{K2Logger} object, which we can use to create a
        logging.logger object for ourselves.
        @type logger: L{K2Logger}
        
        @param args: A list of command-line arguments.  If not specified,
        sys.argv will be used.
        @type args: List
        
        @param config: The path to an .ini-style configuration file.  If not
        specified, L{K2_DEFAULT_CONFIG} will be used.
        @type config: A string
        
        @rtype: K2Settings
        @return: A new L{K2Settings} object loaded with settings.
        
        @raise TypeError: Thrown if logger is not a L{K2Logger} object.
        '''
        
        x = cls(logger)
        x.loadArgs(args)
        x.loadConfig(config)
        
        return x
        
    
    def finalize(self):
        '''
        This is called by the server after everything has been initially
        registered.  Right now, we only use this to get rid of the hash of
        unused settings, since we don't need them anymore.
        '''
        
        self.logger.debug(  'K2Settings setup complete.  '
                          + 'Deleting unused settings.')
        for moduleName in self.__unusedSettings:
            self.logger.warning('Module ' + moduleName
                                + ' had settings defined, but ' + moduleName
                                + 'was not loaded.')
        del self.__unusedSettings
        self.finalized = True
        


class K2SettingsModule(object):
    '''
    K2SettingsModule is a class that handles the settings of a module.
    This class is partially abstract:  Each module needs to provide a class of
    their own that subclasses this module and implements everything that is
    abstract.
    
    NOTE:  Most of these methods do not need to be instance methods.  They can
    easily be static methods.  Only a few abstract methods really need to be
    implemented as instance methods, but you (of course) can do it however you
    like!
    
    A set of settings can be thought of as as set.  Clients will primarily be
    treating instances of this class like hash, in order to get and change
    settings.  To that end, this class implements the behavior of a hash.  The
    module developer only needs to implement the abstract methods.
    
    When implementing a subclass of this class, do not assume that your
    subclass will hold all of the settings for your module in a single
    instance!  The server process will likely create 2+ instances of this
    class:  One instance will hold all of the server-wide settings; the
    other instances will hold session-specific settings.
    '''
    
    # We're an abstract base class
    # @undocumented: __metaclass__
    __metaclass__ = ABCMeta

    
    settings = {}
    '''
    @ivar: If L{K2SettingsModule} is being allowed to store the settings, then
    is where settings are stored.
    @type: Hash
    '''
    
    
    @abstractmethod
    def settingsList(self):
        '''
        Returns a list of all of the setting names that this module recognizes.
        
        @rtype: List
        @return: A sequence of strings.
        '''
        pass
    
    
    @abstractmethod
    def nameValid(self, name):
        '''
        Returns true if the name provided is a valid setting name.
        
        @param name: The name of the setting.
        @type name: A string.
        
        @rtype: Boolean
        @return: True if the setting is recognized, false otherwise.
        '''
        pass
    
    
    @abstractmethod
    def description(self, name):
        '''
        Returns a human-readable description of the named setting.
        
        @param name: The name of the setting.
        @type name: A string.
        
        @rtype: String
        @return: A human-readable description of the named setting.
        
        @raise KeyError: Thrown if the setting name is not recognized.
        '''
        pass
    
    
    @abstractmethod
    def perSession(self, name):
        '''
        Returns true if the setting is session-specific, false otherwise.
        
        @param name: The name of the setting.
        @type name: A string.
        
        @rtype: Boolean
        @return: True if the setting is session-specific, false otherwise.
        
        @raise KeyError: Thrown if the setting name is not recognized.
        '''
        pass
    
    
    @abstractmethod
    def mutable(self, name):
        '''
        Returns true of the setting can be changed after server start.
        
        @param name: The name of the setting.
        @type name: String
        
        @rtype: Boolean
        @return: True if the setting can be changed after server
        start; false otherwise.
        
        @raise KeyError: Thrown if the setting name is not recognized.
        '''
        pass
    
    
    @abstractmethod
    def required(self, name):
        '''
        Returns true if the setting must be set before settings are finalized.
        
        NOTE: Settings that are required should not have a default.
        
        @param name: The name of the setting.
        @type name: A string.
        
        @rtype: Boolean
        @return: True if the setting can be changed after server
        start; false otherwise.
        
        @raise KeyError: Thrown if the setting name is not recognized.
        '''
        pass
    
    
    @abstractmethod
    def default(self, name):
        '''
        Returns the default value for a setting, or None if the setting does
        not have a default value.
        
        @param name: The name of the setting.
        @type name: A string.
        
        @return: The default value for the setting (which might be None).
        
        @raise KeyError: Thrown if the setting name is not recognized.
        '''
        pass
    
    
    @abstractmethod
    def settingValid(self, name, value):
        '''
        Returns true if the value provided for the named setting is valid.
        
        @param name: The name of the setting.
        @type name: A string.
        
        @param value: The proposed value for the setting.
        
        @rtype: Boolean
        @return: True if the value provided is valid for the
        setting; false otherwise.
        
        @raise KeyError: Thrown if the setting name is not recognized.
        '''
    pass


    def __len__(self):
        '''
        Returns the number of settings that are set to non-default values.
        
        @rtype: Integer.
        '''
        return len(self.settings)


    def __getitem__(self, key):
        '''
        Returns a setting's value.  If no custom value has been set, then it
        returns the setting's default value.
        
        @param key: The name of the setting.
        @type key: A string
        
        @return: The value of the setting, or the default value, which might be
        None.
        
        @raise KeyError: Thrown if the setting name is not recognized.
        '''
        if (key in self.settings):
            return self.settings[key]
        else:
            return self.default(key)
    
    
    def __setitem__(self, key, value):
        '''
        Changes a setting's value.  The value must be valid.
        
        @param key: The name of the setting.
        @type key: A string
        
        @param value: The new value for the setting.
        
        @raise KeyError: Thrown if the setting name is not recognized.
        @raise K2SettingImmutable: Thrown if the setting can not be changed.
        @raise ValueError: Thrown if the setting's value is invalid.
        '''
        if (not self.mutable(key)):
            # raise ?????
            # TODO
            pass
        # Checking for validity is what raises the KeyError
        if (self.valid(key, value)):
            if (value != self.default(key)):
                self.settings[key] = value
        else:
            raise ValueError("Value %s is invalid for key %s" % (value, key))

    def __delitem__(self, key):
        '''
        Returns a setting's value to the default.
        
        @param key: The name of the setting.
        @type key: A string.
        
        @raise K2SettingUnknown: Thrown if the setting's name is not recognized.
        @raise K2SettingImmutable: Thrown if the setting can not be changed.
        @raise ???: Thrown if the setting is required
        '''
        if (not self.mutable(key)):
            # raise ?????
            # TODO:
            pass
        if (not self.required(key)):
            # raise ?????
            # TODO
            pass
        del self.settings[key]