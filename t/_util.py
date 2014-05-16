'''
This package has useful stuff that is used by the other test modules.
'''

from sys import version_info


#: If True, then we are using a new-enough Python that supports
# C{@unittest.skip} and C{@unittest.expectedFailure}
# Test skipping and expected failures came in 2.7.
canSkipOrFail = False
_majorVer, _minorVer = version_info[:2]
if (   (_majorVer >= 3)
    or (_minorVer >= 7)
       ):
    canSkipOrFail = True


__all__ = (canSkipOrFail,)
