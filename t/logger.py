'''
Created on May 9, 2014

@author: akkornel
'''
import unittest
import logging
from ._util import canSkipOrFail, nonStr

# If we're being run directly, then we need to add the parent dir to path
try:
    from k2ksm import logger
except:
    from sys import path
    path.append('..')
    from k2ksm import logger
    


class K2LoggerTests(unittest.TestCase):
    # All of the tests of the K2Logger are in this class.

    def test_create(self):
        # Creating a logger with a valid name should pass
        l = logger.K2Logger('Karl')
        self.assertTrue(isinstance(l, logger.K2Logger))
        
    if canSkipOrFail:
        def test_create_badName(self):
            # Creating a logger with something non-str()able should fail
            nonstr = nonStr()
            self.assertRaises(TypeError, logger.K2Logger, nonstr)

    def test_namePrefix_get(self):
        # Make sure the namePrefix matches what is stored
        l = logger.K2Logger('Karl')
        prefix = l.namePrefix
        self.assertEqual(prefix, l._K2Logger__namePrefix)

    if canSkipOrFail:
        @unittest.expectedFailure
        def test_namePrefix_set(self):
            # Trying to set the namePrefix should fail
            l = logger.K2Logger('Karl')
            l.namePrefix = 'SomeoneElse'
    
    if canSkipOrFail:
        @unittest.expectedFailure
        def test_namePrefix_delete(self):
            # Trying to delete the namePrefix should fail
            l = logger.K2Logger('Karl')
            del l.namePrefix
    
    def test_logger(self):
        # The logger attribute should be a Logger object
        l = logger.K2Logger('Karl')
        self.assertTrue(isinstance(l.logger, logging.Logger))
        
    if canSkipOrFail:
        @unittest.expectedFailure
        def test_logger_set(self):
            # We shouldn't be able to replace the logger
            l = logger.K2Logger('Karl')
            l.logger = logging.getLogger('Hello!')
    
    if canSkipOrFail:
        @unittest.expectedFailure
        def test_logger_delete(self):
            # We shouldn't be able to delete the logger
            l = logger.K2Logger('Karl')
            del l.logger

    def test_logStderr_false(self):
        l = logger.K2Logger('Karl')
        l.logToStderr = False
    
    if canSkipOrFail:
        def test_logStderr_nonBoolean(self):
            # Passing a non-boolean should fail
            l = logger.K2Logger('Karl')
            self.assertRaises(TypeError, l.__setattr__, 'logToStderr', 'Karl')
    
    def test_logSyslog_true(self):
        l = logger.K2Logger('Karl')
        l.logToSyslog = True
    
    def test_logSyslog_tf(self):
        l = logger.K2Logger('Karl')
        l.logToSyslog = True
        l.logToSyslog = False
    
    if canSkipOrFail:
        def test_logSyslog_nonBoolean(self):
            l = logger.K2Logger('Karl')
            self.assertRaises(TypeError, l.__setattr__, 'logToSyslog', 'Karl')
    
    
    
    # TODO: Add test cases for loggerForModule
    # Also, try to actually log stuff, to see if it works!
        
        
# List the tests and create a test suite, for use by the top-level test script.
tests = ('test_create',
         'test_namePrefix_get',
         'test_logger',
         'test_logStderr_false',
         'test_logSyslog_true', 'test_logSyslog_tf',
         )
skippedTests = ('test_create_badName',
                'test_namePrefix_set', 'test_namePrefix_delete',
                'test_logger_set', 'test_logger_delete',
                'test_logStderr_nonBoolean',
                'test_logSyslog_nonBoolean',
                )
if canSkipOrFail:
    K2LoggerTestSuite = unittest.TestSuite(map(K2LoggerTests, (tests + skippedTests)))
else:
    K2LoggerTestSuite = unittest.TestSuite(map(K2LoggerTests, tests))

    
# Allow this set of test cases to be run by themselves.
if __name__ == "__main__":
    unittest.main()
