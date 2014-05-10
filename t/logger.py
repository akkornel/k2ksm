'''
Created on May 9, 2014

@author: akkornel
'''
import unittest
import logging
from sys import version_info

# If we're being run directly, then we need to add the parent dir to path
try:
    from k2ksm import logger
except:
    from sys import path
    path.append('..')
    from k2ksm import logger
    
# Get the version number.  Test skipping and expected failures came in 2.7.
majorVer, minorVer = version_info[:2]
canSkip = False
if (   (majorVer >= 3)
    or (minorVer >= 7)
       ):
    canSkip = True


class K2LoggerTests(unittest.TestCase):
    # All of the tests of the K2Logger are in this class.

    def test_create(self):
        # Creating a logger with a valid name should pass
        l = logger.K2Logger('Karl')
        self.assertTrue(isinstance(l, logger.K2Logger))
    
    # Skipping is allowed in 3+ or 2.7+
    if canSkip:
        @unittest.skip("I don't know what object won't give me a str() output")
        def test_create_badName(self):
            # Creating a logger with something non-str()able should fail
            pass

    if canSkip:
        @unittest.expectedFailure
        def test_namePrefix_set(self):
            # Trying to set the namePrefix should fail
            l = logger.K2Logger('Karl')
            l.namePrefix = 'SomeoneElse'
    
    if canSkip:
        @unittest.expectedFailure
        def test_namePrefix_delete(self):
            # Trying to delete the namePrefix should fail
            l = logger.K2Logger('Karl')
            del l.namePrefix
    
    
    def test_logger(self):
        # The logger attribute should be a Logger object
        l = logger.K2Logger('Karl')
        self.assertTrue(isinstance(l.logger, logging.Logger))
        
    if canSkip:
        @unittest.expectedFailure
        def test_logger_set(self):
            # We shouldn't be able to replace the logger
            l = logger.K2Logger('Karl')
            l.logger = logging.getLogger('Hello!')
    
    if canSkip:
        @unittest.expectedFailure
        def test_logger_delete(self):
            # We shouldn't be able to delete the logger
            l = logger.K2Logger('Karl')
            del l.logger
        
    
    # TODO: Add test cases for logToStderr, logToSyslog, and loggerForModule
    # Also, try to actually log stuff, to see if it works!
    # Finally, add an extra test for Windows.
        
        
# List the tests and create a test suite, for use by the top-level test script.
tests = ('test_create',
         'test_logger')
skippedTests = ('test_create_badName',
                'test_namePrefix_set', 'test_namePrefix_delete',
                'test_logger_set', 'test_logger_delete')
if canSkip:
    K2LoggerTestSuite = unittest.TestSuite(map(K2LoggerTests, tests, skippedTests))
else:
    K2LoggerTestSuite = unittest.TestSuite(map(K2LoggerTests, tests))

    
# Allow this set of test cases to be run by themselves.
if __name__ == "__main__":
    unittest.main()
