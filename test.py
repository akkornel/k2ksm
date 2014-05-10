#!/usr/bin/env python

from optparse import OptionParser
import unittest
from sys import exit
from t import *

# Check to see if we're running in verbose mode
parser = OptionParser('usage: %prog [-v]')
parser.add_option('-v', action='store_true', dest='verbose', default=False,
                   help='Display one line of text for each test')
options, args = parser.parse_args()
verbosity = 1
if (options.verbose == True):
    verbosity = 2

# Assemble all of the test suites
tests = unittest.TestSuite()
tests.addTest(logger.K2LoggerTestSuite)

# Configure the runner, and run the tests
runner = unittest.TextTestRunner(verbosity=verbosity)
result = runner.run(tests)

# Clean up
if (not result.wasSuccessful()):
    exit(1)
