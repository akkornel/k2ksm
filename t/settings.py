'''
This module contains all of the tests for everything in the k2ksm.settings
Python module.
'''

from os import close, fdopen, unlink
import random
from tempfile import mkstemp
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
    def makeSettings(cls):
        '''
        Generates up to MAX_ARGS settings.  Agruments are placed into
        one of MAX_MODULES different modules, named
        "module0", "module1", ..., "moduleX".  Each setting name is "settingX",
        where X is a number from 0 to MAX_SETTINGS.  The value of the setting
        is a number from 0 to MAX_VALUE.
        
        @return: A 2-dimensional hash of settings.
        @rtype: Hash of hashes
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
    
    @classmethod
    def makeArguments(cls, settings=None):
        '''
        Convert a L{makeSettings} two-dimensional hash into a list of
        arguments that are suitable for putting on a command line.
        
        @param settings: If provided, use these as the settings.
        @type settings: Hash of hashes
        
        @return: The list of command-line-formatted settings, and the hash of
        settings.
        @rtype: Tuple
        '''
        if (settings == None):
            settings = cls.makeSettings()
        args = []
        for module in settings:
            for setting in settings[module]:
                args.extend([module + '.' + setting,
                             settings[module][setting]
                            ])
        return (args, settings)
        
    @classmethod
    def makeSettingsFile(cls, settings=None):
        '''
        Using L{makeSettings}, generate some settings, and then write them to
        a file.  It is the client's responsibility to delete the file when it
        is no longer needed.
        
        @param settings: If provided, use these as the settings.
        @type settings: Hash of hashes
        
        @return: The path to the created file, and the hash of settings.
        @rtype: Tuple
        '''
        # Create file and contents
        if (settings == None):
            settings = cls.makeSettings()
        (fileNum, filePath) = mkstemp(text=True)
        fileHandle = fdopen(fileNum, 'w')
        
        # Write settings to file
        for module in settings:
            fileHandle.write('[' + module + "]\n")
            for setting in settings[module]:
                fileHandle.write(setting + '=' + str(settings[module][setting])
                                 + "\n")
        
        # Close and return file path
        fileHandle.close()
        return (filePath, settings)
    
    
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
        (args, settings) = self.__class__.makeArguments()
        self.s.loadArgs(args)
        self.assertEquals(len(self.s._K2Settings__unusedSettings), \
                          len(settings))
        
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
    

    def test_loadConfig(self):
        # Try reading from a good settings file
        (filePath, settings) = self.__class__.makeSettingsFile()
        self.s.loadConfig(filePath)
        unlink(filePath)
        self.assertEquals(len(self.s._K2Settings__unusedSettings), \
                          len(settings))
        
    
    def test_load(self):
        # Test the load convenience function
        # To do this, make some settings, and then split into two parts
        settingsAll = self.__class__.makeSettings()
        settingsForFile = {}
        settingsForCLI = {}
        
        for module in settingsAll:
            for setting in settingsAll[module]:
                # Which do we add it to?
                if (random.randint(0,1) == 0):
                    target = settingsForFile
                else:
                    target = settingsForCLI
                
                if (module not in target):
                    target[module] = {}
                target[module][setting] = settingsAll[module][setting]
        
        # Now we have everything distributed, go ahead and make everything
        (filePath, settingsForFile) = self.makeSettingsFile(settingsForFile)
        (args, settingsForCLI) = self.makeArguments(settingsForCLI)
        
        # Finally, do the settings creation, and test
        emptyLog = logger.K2Logger('')
        self.s = settings.K2Settings.load(emptyLog, args, filePath)
        unlink(filePath)
        self.assertEquals(len(self.s._K2Settings__unusedSettings), \
                          len(settingsAll))
    
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
    'test_loadConfig',
    'test_load',
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
