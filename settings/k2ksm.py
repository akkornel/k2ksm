from . import K2SettingsModule

__all__ = ('K2KSMSettings')

settings = {'OverrideCounter': {'description': "If set, the value specified " +
                                               "will be used as the current " +
                                               "counter value for all " +
                                               "counter-based authenticators.",
                                'perSession': False,
                                'mutable': True,
                                },
            'OverrideTimer': {'description': "If set, the time specified " +
                                             "will be used as the " +
                                             "current time for all time-" +
                                             "based authenticators.",
                              'perSession': False,
                              'mutable': True,
                              },
            'TestMode': {'description': "If set, certain other settings " +
                                        "will be accessible.  For " +
                                        "example, OverrideCounter and " +
                                        "OverrideTimer will be able to " +
                                        "be changed.",
                         'perSession': False,
                         'mutable': False,
                         },
            }


class K2KSMSettings(K2SettingsModule):
    '''
    K2KSMSettings handles all of the settings for the K2KSM server
    
    '''
    pass

    @staticmethod
    def settingsList():
        return settings.keys()
    
    @staticmethod
    def nameValid(name):
        return (name in settings)
        return False
    
    @staticmethod
    def description(name):
        return settings[name]['description']
    
    @staticmethod
    def perSession(name):
        return settings[name]['perSession']
    
    @staticmethod
    def mutable(name):
        return settings[name]['mutable']
    
    @staticmethod
    def default(name):
        if ('default' in settings[name]):
            return settings[name]['default']
        else:
            return None
    
    def valid(self, name, value):
        # TODO
        pass
