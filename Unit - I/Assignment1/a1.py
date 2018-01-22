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
from pandas_datareader import data as pdr  # The pandas Data Module used for fetching data from a Data Source
import warnings  # For removing Deprication Warning w.r.t. Yahoo Finance Fix
import scipy.stats
from sklearn import linear_model
import numpy as np
import matplotlib.pyplot as plt
import time

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from fix_yahoo_finance import pdr_override  # For overriding Pandas DataFrame Reader not connecting to YF


def yahoo_finance_bridge():
    """
    This function fixes problems w.r.t. fetching data from Yahoo Finance
    :return: None
    """
    logging.info('Correcting Yahoo Finance')
    pdr_override()


def main():
    """
    This function is called from the main block. The purpose of this function is to contain all the calls to
    business logic functions
    :return: int - Return 0 or 1, which is used as the exist code, depending on successful or erroneous flow
    """
    # Wrap in a try block so that we catch any exceptions thrown by other functions and return a 1 for graceful exit
    try:
        # ===== Step 0: Fix Yahoo Finance =====
        yahoo_finance_bridge()
        time.sleep(2)
        # ===== Step 1: Download Data =====
        data_disney = pdr.get_data_yahoo('DIS', start='2008-10-01', end='2013-09-01', auto_adjust=True)
        time.sleep(2)
        data_snp = pdr.get_data_yahoo('^GSPC', start='2008-10-01', end='2013-09-01', auto_adjust=True)

        # ===== Step 2: Get Monthly Returns =====
        disney_monthly = data_disney.asfreq('BM').ffill().pct_change().dropna()
        snp_monthly = data_snp.asfreq('BM').ffill().pct_change().dropna()

        # ===== Step 3: PLot Disney against SnP =====
        x = np.reshape(snp_monthly['Close'], (len(snp_monthly['Close']), 1))
        y = np.reshape(disney_monthly['Close'], (len(disney_monthly['Close']), 1))

        regr = linear_model.LinearRegression()
        regr.fit(x, y)
        y_predict = regr.predict(x)

        plt.scatter(x, y, color='black')
        plt.plot(x, y_predict, color='blue', linewidth=3)
        plt.grid(True, which='both')
        plt.axhline(y=0, color='black')
        plt.axvline(x=0, color='black')
        plt.show()

        # ===== Step 4: Display slope, intercept, r^2, stderr
        slope, intercept, r_value, p_value, stderr = scipy.stats.linregress(snp_monthly['Close'], disney_monthly['Close'])
        print('\nBeta (Slope): %s' % str(slope))
        print('Alpha (Intercept): %s' % str(intercept))
        print('Standard Error: %s' % str(stderr))
        print('R^2: %s' % str(r_value ** 2))

        # ===== Step 5: Calculate Annualized Excess Return =====
        average_annual_t_bill = 0.5
        monthly_riskfree_rate = average_annual_t_bill / 12
        risk_free_rate = monthly_riskfree_rate * (1 - slope)
        jensens_alpha = intercept * 100 - (risk_free_rate)

        annualized_excess_return = ((1 + (jensens_alpha/100)) ** 12) - 1
        print('Annualized Excess Return: %s %%' % str(annualized_excess_return * 100))

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
