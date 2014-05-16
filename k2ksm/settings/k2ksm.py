'''
All of the settings for the K2KSM module are defined here.
'''

import dateutil.parser
from . import K2SettingsModule

__all__ = ('K2KSMSettings',)


'''
The following private functions are validators for the various settings which
appear below.  I really wish that I could have Perl-style multi-line anonymous
subroutines.
'''


def _boolean_validator(value):
    if (   (value == True)
        or (value == False)
        ):
        return True
    else:
        return False


def _counter_validator(value, context):
    # Fail immediately if we're not in test mode
    if (context['K2KSM'][0]['TestMode'] == False):
        return False
    
    # It's OK if the value is None (to un-set the setting)
    if (value == None):
        return True

    # The value must be a non-negative Integer
    try:
        value = int(value)
    except:
        return False
    if (value < 0):
        return False
    else:
        return True


def _datetime_validator(value, context):
    # Fail immediately if we're not in test mode
    if (context['K2KSM'][0]['TestMode'] == False):
        return False
    
    # If the parser can parse it, then we'll accept it
    try:
        value = dateutil.parser.parse(value)
    except:
        return False
    return True


#: settings is a hash that details what the K2KSM module's settings are.
settings = {}

settings['testMode'] = {'perSession': False,
                        'mutable': False,
                        'required': True,
                        'validator': _boolean_validator,
                        }
settings['testMode']['description'] = \
    "If True, this server is running in test mode.  Certain settings (like " \
    "the various Override* settings) can be set.  Needless to say (but I'm" \
    "saying it anyway), DO NOT RUN TEST MODE IN PRODUCTION!!!"


settings['ServerPrivate'] = {'perSession': False,
                             'mutable': False,
                             'required': True,
                             'validator': _boolean_validator,
                             }
settings['ServerPrivate']['description'] = \
    "If True, this is the private side of the server.  Otherwise, this is " \
    + "the public-facing server."
    

settings['OverrideCounter'] = {'perSession': False,
                               'mutable': True,
                               'default': None,
                               'contextValidator': _counter_validator
                               }
settings['OverrideCounter']['description'] = \
    "Used by authentication modules that require a counter.  If set, the " \
    + "value will be what is used by the authentication module.  The value " \
    + "does NOT auto-increment.  This setting may only be set if the server " \
    + "is in test mode."

settings['OverrideTimer'] = {'perSession': False,
                               'mutable': True,
                               'default': None,
                               'contextValidator': _datetime_validator
                               }
settings['OverrideTimer']['description'] = \
    "Used by authentication modules that require a time.  If set, the " \
    + "value will be what is used by the authentication module.  The value " \
    + "does NOT change automatically, and it must be in ISO 8601 combined " \
    + "format (for example: 2014-05-15T20:00:00Z).  This setting may only " \
    + "be set if the server is in test mode."


class K2KSMSettings(K2SettingsModule):
    '''
    K2KSMSettings provides access to all of the settings for the K2KSM server.
    The work of storing settings is handled by the L{K2SettingsModule}
    superclass.  We just provide the list of settings and their properties.
    '''


    @staticmethod
    def settingsList():
        '''
        Returns a list of all of the setting names that this module recognizes.
        
        @rtype: List
        @return: A sequence of strings.
        '''
        return settings.keys()
    
    
    @staticmethod
    def nameValid(name):
        '''
        Returns true if the name provided is a valid setting name.
        
        @param name: The name of the setting.
        @type name: A string.
        
        @rtype: Boolean
        @return: True if the setting is recognized, false otherwise.
        '''
        return (name in settings)
    
    
    @staticmethod
    def description(name):
        '''
        Returns a human-readable description of the named setting.
        
        @param name: The name of the setting.
        @type name: A string.
        
        @rtype: String
        @return: A human-readable description of the named setting.
        
        @raise KeyError: Thrown if the setting name is not recognized.
        '''
        return settings[name]['description']
    
    
    @staticmethod
    def perSession(name):
        '''
        Returns true if the setting is session-specific, false otherwise.
        
        @param name: The name of the setting.
        @type name: A string.
        
        @rtype: Boolean
        @return: True if the setting is session-specific, false otherwise.
        
        @raise KeyError: Thrown if the setting name is not recognized.
        '''
        return settings[name]['perSession']
    
    
    @staticmethod
    def mutable(name):
        '''
        Returns true of the setting can be changed after server start.
        
        @param name: The name of the setting.
        @type name: String
        
        @rtype: Boolean
        @return: True if the setting can be changed after server
        start; false otherwise.
        
        @raise KeyError: Thrown if the setting name is not recognized.
        '''
        return settings[name]['mutable']
    
    
    @staticmethod
    def required(name):
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
        # I'm not requiring the required key in my settings hashes
        if ('required' in settings[name]):
            return settings[name]['required']
        else:
            return False
    
    
    @staticmethod
    def default(name):
        '''
        Returns the default value for a setting, or None if the setting does
        not have a default value.
        
        @param name: The name of the setting.
        @type name: A string.
        
        @return: The default value for the setting (which might be None).
        
        @raise KeyError: Thrown if the setting name is not recognized.
        '''
        # I'm not requiring the default key in my hashes
        if ('default' in settings[name]):
            return settings[name]['default']
        else:
            return None
    
    @staticmethod
    def settingValid(name, value, context):
        '''
        Returns true if the value provided for the named setting is valid.
        
        @param name: The name of the setting.
        @type name: A string.
        
        @param value: The proposed value for the setting.
        
        @param context: For settings which are context-sensitive (that is,
        their value depends on other settings), this provides access to all of
        the settings that are currently in effect.
        @type context: A hash of a hash of L{K2SettingsModule} objects.
        
        @rtype: Boolean
        @return: True if the value provided is valid for the
        setting; false otherwise.
        
        @raise KeyError: Thrown if the setting name is not recognized.
        '''
        if ('contextValidator' in settings[name]):
            return settings[name]['cointextValidator'](value, context)
        else:
            return settings[name]['validator'](value)
