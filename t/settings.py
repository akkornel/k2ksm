'''
This module contains all of the tests for everything in the k2ksm.settings
Python module.
'''

import random
import unittest

# If we're being run directly, then we need to add the parent dir to path
try:
    from k2ksm import logger, settings
    from k2ksm.exceptions import K2FinalizeError
    from t._util import canSkipOrFail
except:
    from sys import path
    path.append('..')
    from k2ksm import logger, settings
    from k2ksm.exceptions import K2FinalizeError
    from t._util import canSkipOrFail

    



class K2SettingsTests(unittest.TestCase):
    # All of the tests of the K2Settings are in this class.
    
    MAX_ARGS = 10
    MAX_MODULES = 3
    MAX_SETTINGS = 5
    MAX_VALUE = 120
    
    @classmethod
    def makeArguments(cls):
        '''
        Generates up to MAX_ARGS pairs of arguments.  Agruments are placed into
        one of MAX_MODULES different modules, named
        "module0", "module1", ..., "moduleX".  Each setting name is "settingX",
        where X is a number from 0 to MAX_SETTINGS.  The value of the setting
        is a number from 0 to MAX_VALUE.
        '''
        
        #: A 2-dimensional hash.  The outer key is the module name, the inner
        # key is the setting name.
        modules = {}
        
        for i in xrange(1, random.randint(1, cls.MAX_ARGS)):
            moduleString = 'module' + str(random.randint(0, cls.MAX_MODULES))
            settingString = 'setting' + str(random.randint(0, cls.MAX_SETTINGS))
            if (    (moduleString in modules)
                and (settingString in modules[moduleString])
               ):
                # Don't duplicate entries.  We've lost this chance; try again!
                continue

            # (If needed) make the 2nd-level hash, then assign the value
            if (moduleString not in modules):
                modules[moduleString] = {}
            modules[moduleString][settingString] = random.randint(0, \
                                                    cls.MAX_VALUE)
            
        return modules
    
    
    def setUp(self):
        random.seed()
        emptyLog = logger.K2Logger('')
        #emptyLog.logToStderr = False
        self.s = settings.K2Settings(emptyLog)
        
    def tearDown(self):
        self.s = None
    

    def test_create(self):
        # Creating a basic settings object should pass
        self.assertTrue(isinstance(self.s, settings.K2Settings))
    
    if canSkipOrFail:
        def test_create_badLogger(self):
            # Creating without a K2Logger should fail
            self.assertRaises(TypeError, settings.K2Settings, 'String')
    
    
    def test_loadArgs(self):
        # Generate some sample module/setting data
        samples = self.__class__.makeArguments()
        args = []
        
        # Convert into argument strings
        for module in samples:
            for setting in samples[module]:
                args.extend([module + '.' + setting,
                             samples[module][setting]
                            ])
        
        self.s.loadArgs(args)
        self.assertEquals(len(self.s._K2Settings__unusedSettings), \
                          len(samples))
        
    def test_loadArgs_emptyList(self):
        # We should be able to loadArgs with an empty list
        self.s.loadArgs(())
        self.assertEquals(len(self.s._K2Settings__unusedSettings), 0)
        
    if canSkipOrFail:
        def test_loadArgs_oddList(self):
            # We should NOT be able to loadArgs with an odd-numbered list
            args = ('module.setting',)
            self.assertRaises(IndexError, self.s.loadArgs, args)
    
    if canSkipOrFail:
        def test_loadArgs_finalized(self):
            # We should be able to loadArgs after settings have been finalized
            args = ('module.setting', '15')
            self.s.finalize()
            self.assertRaises(K2FinalizeError, self.s.loadArgs, args)
    
    # TODO: Test loadConfig()
    
    # TODO: Test load()
    
    # TODO: Test procesUnused()
    
    # TODO: Test register(), we'll probably need to make our own basic class
    
    def test_finalize(self):
        # We should be able to finalize an empty object
        self.s.finalize()
        self.assertEquals(len(self.s._K2Settings__unusedSettings), 0)

    # TODO: Test newSession()
    
    # TODO: Test delSession()
    
    # TODO: Test settingGet()
    
    # TODO: Test settingSet()


class K2SettingsModuleTests(unittest.TestCase):
    # All of the tests of K2SettingsModule are in this class.
    # TODO: Test everything
    pass


        
# List the tests and create a test suite, for use by the top-level test script.
tests = {}
tests['K2Settings'] = (
    'test_create',
    'test_loadArgs', 'test_loadArgs_emptyList',
    'test_finalize',
)
tests['K2SettingsModule'] = (
)

skippableTests = {}
skippableTests['K2Settings'] = (
    'test_loadArgs_oddList', 'test_loadArgs_finalized',
)
skippableTests['K2SettingsModule'] = (
)

if canSkipOrFail:
    K2SettingsTestSuite = unittest.TestSuite(\
        map(K2SettingsTests, (tests['K2Settings']
                              + skippableTests['K2Settings'])
            )
        )
    K2SettingsModuleTestSuite = unittest.TestSuite(\
        map(K2SettingsModuleTests, (tests['K2SettingsModule']
                                    + skippableTests['K2SettingsModule'])
            )
        )
else:
    K2SettingsTestSuite = unittest.TestSuite(\
        map(K2SettingsTests, tests['K2Settings']))
    K2SettingsModuleTestSuite = unittest.TestSuite(\
        map(K2SettingsModuleTests, tests['K2SettingsModule']))



# Allow this set of test cases to be run by themselves.
if __name__ == "__main__":
    unittest.main()
