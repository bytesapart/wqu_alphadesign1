"""
Created on Mon 22 Jan 2018

@author: Osama Iqbal

Code uses Python 2.7, packaged with Anaconda 4.4.0
Code developed on Windows 10 OS.
"""
# Some Metadata about the script

__author__ = 'Osama Iqbal (iqbal.osama@icloud.com)'
__license__ = 'MIT'
__vcs_id__ = '$Id$'
__version__ = '1.0.0'  # Versioning: http://www.python.org/dev/peps/pep-0386/

import logging  # Logging class for logging in the case of an error, makes debugging easier
import sys  # For gracefully notifying whether the script has ended or not
from nash import game


def main():
    """
    This function is called from the main block. The purpose of this function is to contain all the calls to
    business logic functions
    :return: int - Return 0 or 1, which is used as the exist code, depending on successful or erroneous flow
    """
    # Wrap in a try block so that we catch any exceptions thrown by other functions and return a 1 for graceful exit
    try:
        # ===== Step 1: Define the parameters for the companies =====
        A = [[25, 9], [33, 10]]
        B = [[30, 13], [36, 12]]

        # Create Nash Game
        o_game = game.Game(A, B)

        # ===== Step 2: Check for Nash Equilibrium in Mixed Strategies =====
        mixed = o_game.zero_sum
        if mixed:
            print('There exist a Nash equilibrium in mixed strategies.')
        else:
            print('There exist no Nash equilibrium in mixed strategies.')

        # ===== Step 3: Calculate Nash Equilibrium =====
        print('Program to demonstrate use of Nash Equilibrium')
        print('Nash Equilibrium Implementation (Pure Strategies)')
        for eq in o_game.support_enumeration():
            equilibrium = eq

        print 'Equilibrium: %s' % str(equilibrium)

        return 0
    except BaseException as e:
        # Casting a wide net to catch all exceptions
        print('\n%s' % str(e))
        return 1


# Main block of the program. The program begins execution from this block when called from a cmd
if __name__ == '__main__':
    # Initialize Logger
    logging.basicConfig(format='%(asctime)s %(message)s: ')
    logging.info('Application Started')
    exit_code = main()
    logging.info('Application Ended')
    sys.exit(exit_code)
