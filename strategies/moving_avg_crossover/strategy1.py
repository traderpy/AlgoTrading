# Provided by https://traderpy.com/ - GitHub https://github.com/traderpy/AlgoTrading

# DISCLAIMER - Trading the Financial Markets is risky and may cause significant financial losses. Please make sure to
# understand the risks and the provided code before attempting to trade. The material provided by the author is for
# educational purposes only and does not serve as financial advice. The author is not liable for any losses caused from
# the usage of this material. The code is provided 'as is' without any warranty.

# AFFILIATE DISCLAIMER - Links provided in this code may contain affiliate links. TraderPy may receive a commission from
# those links.

# STRATEGY DESCRIPTION - In this Python file, we will create a Moving Average Crossover Trading Strategy which will
# run on the MetaTrader5 platform. Whenever price is above the Moving Average, it will send a request to buy,
# whenever price is below the Moving Average, it will send a request to sell. We will deploy the strategy on EUR/USD
# 1-minute timeframe using the 20-period Simple Moving Average. But you can choose which symbols or timeframes you want
# to trade.

# Libraries
import pandas as pd  # Pandas Documentation: https://pandas.pydata.org/
import MetaTrader5 as mt  # MetaTrader5 Documentation: https://www.mql5.com/en/docs/integration/python_metatrader5
from datetime import datetime  # datetime Documentation: https://docs.python.org/3/library/datetime.html

# Before we create our Strategy, we need a MetaTrader5 Account where we can request data and send orders to the market
# Demo Account Credentials - Create your own Trading Account at https://admiralmarkets.com/
login_credentials = {
    'login': 41259280,
    'password': 'fgW8D6HGhqH8',
    'server': 'AdmiralMarkets-Demo'
}

# Path to the MetaTrader5 Client Terminal - Try to use Absolute Path in case platform does not start
platform_path = r'AlgoTrading\AlgoTrading\platform\Admiral Markets MT5\terminal64.exe'

# Initialize MetaTrader5 platform with path where MetaTrader5 is installed
isInitialized = mt.initialize(platform_path)
print('Platform Initialized: ', isInitialized)

# Log in to MetaTrader5
isLoggedIn = mt.login(login_credentials['login'], login_credentials['password'], login_credentials['server'])
print('Account Logged In: ', isLoggedIn)