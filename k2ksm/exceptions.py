'''
Created on May 15, 2014

@author: akkornel
'''


class K2FinalizeError(Exception):
    '''
    This exception is thrown if certain changes have been made after the server
    has been finalized.  "Finalized" means that all modules have been loaded,
    and the server is now ready to do actual work.
    '''
    pass
