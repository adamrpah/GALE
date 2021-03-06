'''
File: errors.py
Author: Adam Pah
Description: 
Error Handling
'''

from __future__ import division, print_function

def generic_error_handler(message=''):
    '''
    Generic handler for custom thrown exceptions.
    input:
        m - message to display
    '''
    import sys
    print( 'ERROR: Stopped Execution due to Incorrect Usage' )
    print( message )
    sys.exit()
