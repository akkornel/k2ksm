
from abc import ABCMeta, abstractmethod
from sys import argv


'''
@var K2_DEFAULT_CONFIG: This is the default configuration file location.
Individual distributions should replace the /dev/null source distribution
default with something disto-appropriate.
'''
K2_DEFAULT_CONFIG = '/dev/null'


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

    '''
    @ivar __unusedSettings: A 2-dimensional array of settings that have been
    pulled in somehow, but which have not already been claimed by a module.
    '''
    __unusedSettings = {}

    '''
    @ivar __moduleSettings: An array of K2SettingsModule objects.  The key is
    the name of the module.
    '''
    __moduleSettings = {}
    
    '''
    @ivar finalized: Set to true once all modules have been registered.
    '''
    finalized = False
    
    '''
    @ivar logger: A K2Logger object that we can use.
    '''
    logger = None

    
    def __init__(self, logger):
        '''
        Right now, we just create a logger for ourselves.
        
        @param logger: A K2Logger object, which we can use to create a
        logging.logger object for ourselves.
        @type logger: K2Logger
        '''
        
        self.logger = logger.loggerForModule('DB')
        self.logger.debug('K2Settings instantiated')
    
    
    def loadArgs(self, args=argv):
        '''
        Load settings from command-line arguments.
        A list of arguments can be provided for parsing, otherwise sys.argv
        is used.
        
        @param args: A list of command-line arguments.
        @type args: List
        '''
        self.logger.info('Parsing command-line arguments')
        # TODO
    
    
    def loadConfig(self, config=K2_DEFAULT_CONFIG):
        '''
        Load settings from a .ini-style configuration file.
        If the configuration file to use is not provided, then the default
        K2_DEFAULT_CONFIG will be used instead.
        
        @param config: The path to an .ini-style configuration file.
        @type config: A string
        '''
        self.logger.info('Loading configuration from path' + config)
        # TODO
    
    
    @classmethod
    def load(cls, logger, args=argv, config=K2_DEFAULT_CONFIG):
        '''
        A convenience method.  Creates a new K2Settings object, calls loadArgs
        and loadConfig, and then returns the newly-made class.
        
        @param logger: A K2Logger object, which we can use to create a
        logging.logger object for ourselves.
        @type logger: K2Logger
        
        @param args: A list of command-line arguments.
        @type args: List
        
        @param config: The path to an .ini-style configuration file.
        @type config: A string
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
        del self.__unusedSettings
        self.finalized = True
        # TODO: Generate a warning for each module that has unused settings.


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
    
    For each module, the server process will generally create 2+ instances of
    this class.  One instance will hold all of the server-wide settings; the
    other instances will hold session-specific settings.
    '''
    
    # We're an abstract base class.
    __metaclass__ = ABCMeta
    
    '''
    @ivar settings: This is where settings are stored.
    @type settings: A hash.
    '''
    settings = {}

    '''
    @ivar sessionID: If this instance is holding session-specific settings,
    then a session ID will be set.
    '''
    sessionID = None
    
    
    @abstractmethod
    def settingsList(self):
        '''
        Returns a list of all of the setting names that this module recognizes.
        
        @return: A tuple of strings.
        '''
        pass
    
    
    @abstractmethod
    def nameValid(self, name):
        '''
        Returns true if the name provided is a valid setting name.
        
        @param name: The name of the setting.
        @type name: A string.
        
        @return: A Boolean: True if the setting is recognized, false otherwise.
        
        @raise K2SettingUnknown: Thrown if the setting name is not recognized.
        '''
        pass
    
    
    @abstractmethod
    def description(self, name):
        '''
        Returns a human-readable description of the named setting.
        
        @param name: The name of the setting.
        @type name: A string.
        
        @return: A string containing a human-readable description.
        
        @raise K2SettingUnknown: Thrown if the setting name is not recognized.
        '''
        pass
    
    
    @abstractmethod
    def perSession(self, name):
        '''
        Returns true if the setting is session-specific, false otherwise.
        
        @param name: The name of the setting.
        @type name: A string.
        
        @return: A Boolean: True if the setting is session-specific, false
        otherwise.
        
        @raise K2SettingUnknown: Thrown if the setting name is not recognized.
        '''
        pass
    
    
    @abstractmethod
    def mutable(self, name):
        '''
        Returns true of the setting can be changed after server start.
        
        @param name: The name of the setting.
        @type name: A string.
        
        @return: A Boolean: True if the setting can be changed after server
        start; false otherwise.
        
        @raise K2SettingUnknown: Thrown if the setting name is not recognized.
        '''
        pass
    
    
    @abstractmethod
    def required(self, name):
        '''
        Returns true if the setting must be set before settings are finalized.
        
        NOTE: Settings that are required should not have a default.
        
        @param name: The name of the setting.
        @type name: A string.
        
        @return: A Boolean: True if the setting can be changed after server
        start; false otherwise.
        
        @raise K2SettingUnknown: Thrown if the setting name is not recognized.
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
        
        @raise K2SettingUnknown: Thrown if the setting name is not recognized.
        '''
        pass
    
    
    @abstractmethod
    def valid(self, name, value):
        '''
        Returns true if the value provided for the named setting is valid.
        
        @param name: The name of the setting.
        @type name: A string.
        
        @param value: The proposed value for the setting.
        
        @return: A Boolean: True if the value provided is valid for the
        setting; false otherwise.
        
        @raise K2SettingUnknown: Thrown if the setting name is not recognized.
        '''
    pass


    def __len__(self):
        '''
        Returns the number of settings that are set to non-default values.
        
        @return: An Integer.
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
        
        @raise K2SettingUnknown: Thrown if the setting name is not recognized.
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
        
        @raise K2SettingUnknown: Thrown if the setting name is not recognized.
        @raise K2SettingImmutable: Thrown if the setting can not be changed.
        @raise ???: Thrown if the setting's value is invalid.
        '''
        if (not self.mutable(key)):
            # raise ?????
            # TODO
            pass
        if (self.valid(key, value)):
            if (value != self.default(key)):
                self.settings[key] = value
        else:
            # raise ?????
            # TODO
            pass

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
            # TODO
            pass
        if (not self.required(key)):
            # raise ?????
            # TODO
        del self.settings[key]
