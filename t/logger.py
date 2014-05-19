'''
Created on May 9, 2014

@author: akkornel
'''
import unittest
import logging

# If we're being run directly, then we need to add the parent dir to path
try:
    from k2ksm import logger
    from ._util import canSkipOrFail, nonStr
except:
    from sys import path
    path.append('..')
    from k2ksm import logger
    from t._util import canSkipOrFail, nonStr
    


class K2LoggerTests(unittest.TestCase):
    # All of the tests of the K2Logger are in this class.
    
    def setUp(self):
        self.l = logger.K2Logger('Karl')
        
    def testDown(self):
        self.l = None
        

    def test_create(self):
        # Creating a logger with a valid name should pass
        self.assertTrue(isinstance(self.l, logger.K2Logger))
        
    if canSkipOrFail:
        def test_create_badName(self):
            # Creating a logger with something non-str()able should fail
            nonstr = nonStr()
            self.assertRaises(TypeError, logger.K2Logger, nonstr)

    def test_namePrefix_get(self):
        # Make sure the namePrefix matches what is stored
        prefix = self.l.namePrefix
        self.assertEqual(prefix, self.l._K2Logger__namePrefix)

    if canSkipOrFail:
        @unittest.expectedFailure
        def test_namePrefix_set(self):
            # Trying to set the namePrefix should fail
            self.l.namePrefix = 'SomeoneElse'
    
    if canSkipOrFail:
        @unittest.expectedFailure
        def test_namePrefix_delete(self):
            # Trying to delete the namePrefix should fail
            del self.l.namePrefix
    
    def test_logger(self):
        # The logger attribute should be a Logger object
        self.assertTrue(isinstance(self.l.logger, logging.Logger))
        
    if canSkipOrFail:
        @unittest.expectedFailure
        def test_logger_set(self):
            # We shouldn't be able to replace the logger
            self.l.logger = logging.getLogger('Hello!')
    
    if canSkipOrFail:
        @unittest.expectedFailure
        def test_logger_delete(self):
            # We shouldn't be able to delete the logger
            del self.l.logger

    def test_logStderr_false(self):
        self.l.logToStderr = False
    
    if canSkipOrFail:
        def test_logStderr_nonBoolean(self):
            # Passing a non-boolean should fail
            self.assertRaises(TypeError, self.l.__setattr__, 'logToStderr', \
                              'Karl')
    
    def test_logSyslog_true(self):
        self.l.logToSyslog = True
    
    def test_logSyslog_tf(self):
        self.l.logToSyslog = True
        self.l.logToSyslog = False
    
    if canSkipOrFail:
        def test_logSyslog_nonBoolean(self):
            self.assertRaises(TypeError, self.l.__setattr__, 'logToSyslog', \
                              'Karl')
    
    
    
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
