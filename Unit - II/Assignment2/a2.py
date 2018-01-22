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
import warnings
import datetime
import seaborn as sns
import pandas as pd
import pandas_datareader
import numpy as np
import datetime
import matplotlib.pyplot as plt

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
        # ===== Step 0: Yahoo Finance override =====
        # ===== Step 0: Fix Yahoo Finance =====
        yahoo_finance_bridge()
        # ===== Step 1: Download the Data =====
        start = datetime.datetime(2015, 1, 1)
        end = datetime.datetime(2018, 1, 1)

        data = pandas_datareader.data.DataReader(['AAPL', 'MSFT'], 'yahoo', start, end)
        data = data['Close']

        # Normalize Data
        (data / data.iloc[0] * 100).plot(figsize=(15, 6))
        plt.show()

        # ===== Step 2: Calculate Daily return with comparitive study =====
        # change to daily returns
        data2 = pd.DataFrame()
        tickers = ['AAPL', 'MSFT']

        for tick in tickers:
            data2[tick + ' Return'] = data[tick].pct_change()

        data2.plot()
        plt.show()
        # ===== Step 3: Calculate Expected Return for each stock =====
        print('\nData Description:\n')
        data2.describe()
        weights = np.array([0.50, 0.50])  # weight of security in portfolio
        # annual returns of each of the stocks and then calculate the dot product of these returns and the weights
        annual_returns = data2.mean() * 250
        print('Annual Returns:\n')
        print(annual_returns)
        annual_returns.plot.bar()
        plt.show()

        # ===== Step 4: Calculate Std Dev of Portfolio =====
        np.dot(annual_returns, weights)
        pfolio_1 = str(round(np.dot(annual_returns, weights), 5) * 100) + ' %'
        print('\nExpected Portfolio Returns:\n')
        print(pfolio_1)  # portoflio expected returns

        print('Std Dev of the returns:\n')
        print(data2.std() * 250 ** 0.5)  # standev of returns

        cov_matrix = data2.cov()  # cov mat
        print('Cov Mat:\n')
        print(cov_matrix)

        cov_matrix_a = data2.cov() * 250  # annualized cov mat
        print('Cov Mat Annualized')
        print(cov_matrix_a)

        corr_matrix = data2.corr()  # corr mat
        print('Portfolio Variance:\n')
        pfolio_var = np.dot(weights.T, np.dot(data2.cov() * 250, weights))
        print(pfolio_var)

        print('Portfolio Volatility:\n')
        pfolio_vol = (np.dot(weights.T, np.dot(data2.cov() * 250, weights))) ** 0.5
        print (str(round(pfolio_vol, 5) * 100) + ' %')

        # ===== Step 5: How does the return profile of the current portfolio compare to one that is
        # consisting solely of Treasury Bonds =====

        # Calculate expected return using CAPM
        start = datetime.datetime(2015, 1, 1)
        end = datetime.datetime(2018, 1, 1)

        data3 = pandas_datareader.data.DataReader(['AAPL', 'MSFT', 'SPY'], 'yahoo', start, end)
        data3 = data3['Close']
        data3 = data3.pct_change(periods=1)  # Daily Returns

        data3['PortfolioReturn'] = data3['AAPL'] + data3['MSFT']
        data3 = data3[['SPY', 'PortfolioReturn']]

        cov = data3.cov() * 250
        cov_with_market = cov.iloc[1, 0]
        market_var = data3['SPY'].var() * 250
        port_beta = cov_with_market / market_var

        print('Assume a risk-free rate of 1.72% and a risk premium of 5%. Estimate the expected return of Portfolio.')
        port_er = 0.025 + port_beta * 0.05
        port_er = str(port_er * 100) + ' %'
        print(port_er)

        start = datetime.datetime(2015, 1, 1)
        end = datetime.datetime(2018, 1, 1)

        data4 = pandas_datareader.data.DataReader(['AAPL', 'MSFT', 'IEF'], 'yahoo', start, end)
        data4 = data4['Close']
        data4 = data4.pct_change(periods=1)
        data4['PortfolioReturn'] = data4['AAPL'] + data4['MSFT']
        data4 = data4[['IEF', 'PortfolioReturn']]

        rets = data4.dropna()
        area = np.pi * 20.0

        # ====== Step 6: How does the Risk Profile of the two compare? =======
        sns.set(style='darkgrid')
        plt.figure(figsize=(9, 9))
        plt.scatter(rets.mean(), rets.std(), s=area)
        plt.xlabel("Expected Return", fontsize=15)
        plt.ylabel("Risk", fontsize=15)
        plt.title("Return/Risk for Portfolio vs. IEF ", fontsize=20)

        for label, x, y in zip(rets.columns, rets.mean(), rets.std()):
            plt.annotate(label, xy=(x, y), xytext=(50, 0), textcoords='offset points',
                         arrowprops=dict(arrowstyle='-', connectionstyle='bar,angle=180,fraction=-0.2'),
                         bbox=dict(boxstyle="round", fc="w"))
        plt.show()
        # ====== Step 7: Use Python to print a comparative analysis of the two ======
        import ffn
        data4.dropna(inplace=True)
        data4.sort_index(inplace=True)
        stats = data4.calc_stats()
        stats.display()
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
