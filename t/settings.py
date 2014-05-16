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
    
    def setUp(self):
        random.seed()
        emptyLog = logger.K2Logger('')
        #emptyLog.logToStderr = False
        self.s = settings.K2Settings(emptyLog)
        
    def tearDown(self):
        self.s = None
    

    def test_create(self):
        print id(self.s)
        # Creating a basic settings object should pass
        self.assertTrue(isinstance(self.s, settings.K2Settings))
        
    
    def test_loadArgs(self):
        print id(self.s)
        # We should be able to load some number of arguments
        args = []
        modules = {}
        
        # Generate up to 10 pairs of arguments to load
        for i in xrange(1, random.randint(1, 10)):
            moduleNumber = random.randint(0, 3)
            settingNumber = random.randint(0, 5)
            # modules keeps track of the # of modules we've created, and
            # also makes sure that we don't use the same
            # moduleNumber/settingNumber combo multiple times.
            if (moduleNumber not in modules):
                modules[moduleNumber] = []
            if (settingNumber not in modules[moduleNumber]):
                modules[moduleNumber].append(settingNumber)
                args.append('module' + str(moduleNumber) \
                            + '.setting' + str(settingNumber))
                args.append(str(random.randint(0, 120)))
        self.s.loadArgs(args)
        self.assertEquals(len(self.s._K2Settings__unusedSettings), \
                          len(modules))
        
    def test_loadArgs_emptyList(self):
        print id(self.s)
        # We should be able to loadArgs with an empty list
        self.s.loadArgs(())
        self.assertEquals(len(self.s._K2Settings__unusedSettings), 0)
        
    if canSkipOrFail:
        def test_loadArgs_oddList(self):
            print id(self.s)
            # We should NOT be able to loadArgs with an odd-numbered list
            args = ('module.setting',)
            self.assertRaises(IndexError, self.s.loadArgs, args)
    
    if canSkipOrFail:
        def test_loadArgs_finalized(self):
            print id(self.s)
            # We should be able to loadArgs after settings have been finalized
            args = ('module.setting', '15')
            self.s.finalize()
            self.assertRaises(K2FinalizeError, self.s.loadArgs, args)
    
    # TODO: Test loadConfig()
    
    # TODO: Test load()
    
    # TODO: Test procesUnused()
    
    # TODO: Test register(), we'll probably need to make our own basic class
    
    def test_finalize(self):
        print id(self.s)
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
