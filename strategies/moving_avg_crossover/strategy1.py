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
import time

pd.options.display.max_columns = 999

if __name__ == '__main__':

    symbol = 'EURUSD-Z'  # symbol name in the broker platform
    lot_size = 1.0  # float
    deviation = 20

    sma_period = 20

    # Before we create our Strategy, we need a MetaTrader5 Account
    # Demo Account Credentials - Create your own Trading Account at https://admiralmarkets.com/
    login_credentials = {
        'login': 41259280,
        'password': 'fgW8D6HGhqH8',
        'server': 'AdmiralMarkets-Demo'
    }

    # Initialize MetaTrader5 platform. MetaTrader5 must be installed on your PC.
    isInitialized = mt.initialize()
    print('Platform Initialized: ', isInitialized)

    # Log in to MetaTrader5. First log in must be done manually in the platform
    isLoggedIn = mt.login(login_credentials['login'], login_credentials['password'], login_credentials['server'])
    print('Account Logged In: ', isLoggedIn)

    while True:
        # requesting current market price
        current_price = mt.symbol_info_tick(symbol)

        print('time (UNIX): ', current_price.time)
        print('bid: ', current_price.bid, ',', 'ask: ', current_price.ask)

        # requesting OHLC Data for SMA calculation and saving them in a Pandas DataFrame
        # to calculate the SMA, we are using the close prices and calculate the average value (mean)
        sma = pd.DataFrame(mt.copy_rates_from_pos(symbol, mt.TIMEFRAME_M1, 0, sma_period))['close'].mean()
        print('sma: ', sma)

        # requesting number of open positions
        num_open_trades = mt.positions_total()
        print('current open positions: ', num_open_trades)

        try:  # checking exposure of open trades
            open_trades = pd.DataFrame(list(mt.positions_get()), columns=mt.positions_get()[0]._asdict().keys())

            long_trades = open_trades[open_trades['type'] == 0]
            short_trades = open_trades[open_trades['type'] == 1]

            print('open_trades', open_trades[['symbol', 'volume', 'type']])
        except TypeError and IndexError:
            print('open trades: None')

        # trade logic buy
        if current_price.bid > sma:

            if not short_trades.empty:
                print('existing short trade')

            if num_open_trades == 0:
                # create buy request
                request = {
                    "action": mt.TRADE_ACTION_DEAL,
                    "symbol": symbol,
                    "volume": lot_size,
                    "type": mt.ORDER_TYPE_BUY,
                    "price": current_price.ask,
                    "sl": 0,
                    "tp": 0,
                    "deviation": deviation,
                    "magic": 111,
                    "comment": "Python Script BUY",
                    "type_time": mt.ORDER_TIME_GTC,
                    "type_filling": mt.ORDER_FILLING_RETURN,
                }

                # send request to platform
                order_result = mt.order_send(request)
                print('order result: ', order_result)

        # trade logic sell
        elif current_price.bid < sma:

            if not long_trades.empty:
                print('existing long trade')

            if num_open_trades == 0:
                # create sell request
                request = {
                    "action": mt.TRADE_ACTION_DEAL,
                    "symbol": symbol,
                    "volume": lot_size,
                    "type": mt.ORDER_TYPE_SELL,
                    "price": current_price.ask,
                    "sl": 0,
                    "tp": 0,
                    "deviation": deviation,
                    "magic": 111,
                    "comment": "Python Script SELL",
                    "type_time": mt.ORDER_TIME_GTC,
                    "type_filling": mt.ORDER_FILLING_RETURN,
                }

                # send request to platform
                order_result = mt.order_send(request)
                print('order result: ', order_result)

        print('---')
        time.sleep(5)

