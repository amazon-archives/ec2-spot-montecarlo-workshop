'''
ver 0.1, namera@ , initial-release, Oct26'17
ver 0.2, namera@ , included execution id for traceability, Nov3'17


Hedge Your Own Funds: Running Monte Carlo Simulations on EC2 Spot
=================================================================

This simulations worker script launches the Monte-Carlo simulations as described in the session's Jupiter Notebook.
All input parameters have defaults, please see 'parser.add_argument' for details or simply append -h at the end of the execution line to
see input parameter details.

e.g. python mc_worker.py -h

Output:
-------
This script writes simualted results into CSV files, the files are:
<exec_id>_<Stock_Name>_MonteCarloSimResult.csv - for example, AMZN_MonteCarloSimResult.csv , this file holds the last Monte-Carlo simulated value
 for each iteration and the expected cache value given the trading strategy specified in the notebook. Initial investment is $100,000 
ProtfolioRiskAssessment.csv - returns the risk value of multiple-socks protfolio. see --portfolio_stocks_list input paramter for more detai$
 

Sample executions:
------------------
Run simulation with default parameters: 
python mc_worker.py 

Specify a list of stocks for Portfolio Risk Assessment:
python mc_worker.py --stocks-list IBM AMZN MSFT

Specify 1,000,000 simulations to execute:
python mc_worker.py --iterations 1000000
'''


import pandas as pd
from pandas_datareader import data as pdr
import numpy as np
import datetime , time
from math import sqrt
from scipy.stats import norm


import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('--iterations', dest='iterations',default=2000, type=int,
                   help='Number of simulated iterations default=2000')

parser.add_argument('--stock', dest='stock',default="AMZN",
                   help='Stock Name')

parser.add_argument('--short_window_days', dest='short_window_days',default=10, type=int,
                   help='Short moving avearge in days default=10')

parser.add_argument('--long_window_days', dest='long_window_days',default=40, type=int,
                   help='Long moving avearge in days (default=40)')

parser.add_argument('--trading_days', dest='trading_days',default=252, type=int,
                   help='Number of trading days (default=252)')

parser.add_argument('-n', '--stocks-list', default=['AAPL','AMZN','MSFT','INTC'], nargs='+')

parser.add_argument('--id', dest='exec_id',default="None",
                   help='Unique execution  id')

args = parser.parse_args()

STOCK=args.stock
short_window = args.short_window_days
long_window = args.long_window_days
trading_days = args.trading_days
sim_num = args.iterations
portfolio_stocks_list = args.stocks_list
file_prepend_str = args.exec_id

#create output files (CSV) unique string to preapend 
if (file_prepend_str == 'None'):
    t = time.localtime()
    file_prepend_str = time.strftime('%b-%d-%Y_%H%M', t)


'''
uncomment this section for Jupyter
# Initialize the short and long windows
short_window = 10
long_window = 40

# Number of simulations
sim_num = 300

trading_days = 252 # Number of trading days

STOCK="AMZN"

'''

stock_df = pdr.get_data_yahoo(STOCK,start=datetime.datetime(2006, 10, 1), end=datetime.datetime(2017, 10, 1))

#calculate the compound annual growth rate (CAGR) which 
#will give us our mean return input (mu) 
days = (stock_df.index[-1] - stock_df.index[0]).days
cagr = ((((stock_df['Adj Close'][-1]) / stock_df['Adj Close'][1])) ** (365.0/days)) - 1
mu = cagr
 
#create a series of percentage returns and calculate 
#the annual volatility of returns. Generally, the higher the volatility, 
#the riskier the investment in that stock, which results in investing in one over another.
stock_df['Returns'] = stock_df['Adj Close'].pct_change()
vol = stock_df['Returns'].std()*sqrt(252)

# Set the initial capital
initial_capital= float(100000.0)

#set up empty list to hold our ending values for each simulated price series
sim_result = []

# Set up empty list to hold protfolio value for each simulated price serries, this is the value of position['total']
portfolio_total = []
 
#Define Variables
start_price = stock_df['Adj Close'][-1] #starting stock price (i.e. last available real stock price)

# Initialize the `signals` DataFrame 
signals = pd.DataFrame()

# initialize by setting the value for all rows in this column to 0.0.
signals['signal'] = 0.0
signals['short_mavg'] = 0.0

# Create a DataFrame `positions`
positions = pd.DataFrame(index=signals.index).fillna(0.0)

#choose number of runs to simulate - I have chosen 1,000
for i in range(sim_num):
    #create list of daily returns using random normal distribution
    daily_returns=np.random.normal(mu/trading_days,vol/sqrt(trading_days),trading_days)+1
 
    #set starting price and create price series generated by above random daily returns
    price_list = [start_price]
 
    for x in daily_returns:
        price_list.append(price_list[-1]*x)
 
    #Convert list to Pandas DataFrame
    price_list_df = pd.DataFrame(price_list)
   
    #append the ending value of each simulated run to the empty list we created at the beginning
    sim_result.append(price_list[-1])
    
    # Create short simple moving average over the short & long window
    signals['short_mavg']  = price_list_df[0].rolling(short_window).mean()
    signals['long_mavg']  = price_list_df[0].rolling(long_window).mean()
 
    # Create a signal when the short moving average crosses the long moving average, 
    # but only for the period greater than the shortest moving average window. 
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] 
                                            > signals['long_mavg'][short_window:], 1.0, 0.0)   

    # Generate trading orders
    signals['positions'] = signals['signal'].diff()
    
    # Buy 100 shares
    positions[STOCK] = 100*signals['signal']
  
    # Initialize the portfolio with value owned   
    portfolio = positions.multiply(price_list_df[0], axis=0)
    
    # Store the difference in shares owned 
    pos_diff = positions.diff()

    # Add `holdings` to portfolio
    portfolio['holdings'] = (positions.multiply(price_list_df[0], axis=0)).sum(axis=1)

    # Add `cash` to portfolio
    portfolio['cash'] = initial_capital - (pos_diff.multiply(price_list_df[0], axis=0)).sum(axis=1).cumsum()   

    # Add `total` to portfolio
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    
    #append the ending value of each simulated run to the empty list we created at the beginning
    portfolio_total.append(portfolio['total'].iloc[-1])

    
# Simulation Results
#print sim_result
df1 = pd.DataFrame(sim_result, columns=["MonteCarloResults"])
df1.to_csv(file_prepend_str + "_" + STOCK + "_sim_results.csv")

# Protfolio Total
#print portfolio_total
df2 = pd.DataFrame(portfolio_total, columns=["ProtfolioTotal"])
df2.to_csv(file_prepend_str + "_" + STOCK + "_portfolio_total.csv")

# Create one data frame and write to file.
result = pd.concat([df1, df2], axis=1, join_axes=[df1.index])

result.to_csv(file_prepend_str + "_" + STOCK + "_MonteCarloSimResult.csv")


## Protfolio Risk Assessment Section

#list of stocks in portfolio
#defaults are: STOCKS = ['AAPL','AMZN','MSFT','INTC']

portfolio_data = pdr.get_data_yahoo(portfolio_stocks_list, 
                          start=datetime.datetime(2015, 1, 1), 
                          end=datetime.datetime(2017, 1, 1))['Adj Close']

#convert daily stock prices into daily returns
returns = portfolio_data.pct_change()
 
#calculate mean daily return and covariance of daily returns
mean_daily_returns = returns.mean()
cov_matrix = returns.cov()
 
#set up array to hold results
results = np.zeros((3,sim_num))
 
# run the sumulator  
for i in range(sim_num):
    #select random weights for portfolio holdings
    weights = np.random.random(len(portfolio_stocks_list))
    #rebalance weights to sum to 1
    weights /= np.sum(weights)
 
    #calculate portfolio return and volatility
    portfolio_return = np.sum(mean_daily_returns * weights) * 252
    portfolio_std_dev = np.sqrt(np.dot(weights.T,np.dot(cov_matrix, weights))) * np.sqrt(252)
 
    #store results in results array
    results[0,i] = portfolio_return
    results[1,i] = portfolio_std_dev
    #store Sharpe Ratio (return / volatility) - risk free rate element excluded for simplicity
    results[2,i] = results[0,i] / results[1,i]
 
#convert results array to Pandas DataFrame
results_frame = pd.DataFrame(results.T,columns=['ret','stdev','sharpe'])

results_frame.to_csv(file_prepend_str + "_PortfolioRiskAssessment.csv")



