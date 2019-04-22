from gm.api import *
import numpy as np
import talib
from pandas import DataFrame

def init(context):
    context.symbol = 'SZSE.300296'
    context.frequency = 'ld'
    context.fields = 'open, high, low, close'
    context.volume = 200
    #schedule(schedule_func=algo, date_rule='ld', time_rule='09:35:00')

def algo(context):
    now = context.now
    last_day = get_previous_trading_date('SZSE', now)
    data = history_n(symbol=context.symbol, frequency=context.frequency, count=35, end_time=now,
                     fields=context.fields, fill_missing='last', adjust=ADJUST_PREV, df=True)
    open = data['open'].values
    high = data['high'].values
    low = data['low'].values
    close = data['close'].values
    macd, _, _ = talib.MACD(close)
    macd = macd[-1]
    if macd > 0:
        order_volume(symbol=context.symbol, volume=context.volumr, side=PositionSide_Long,
                     order_type=OrderType_Market, position_effect=PositionEffect_Open)
        print('买入')
    elif macd < 0:
        order_volume(symbol=context.symbol, volume=context.volumn,
                     side=PositionSide_Short, order_type=OrderType_Market,
                     position_effect=PositionEffect_Close)
        print('卖出')


if __name__ == '__main__':

    run(strategy_id='326ea827-61dc-11e9-a6ac-00ffa69119ea',
        filename='firstStrategy.py',
        mode=MODE_BACKTEST,
        token='0e5efcc5825e255db5d003f017b648dc4f877472',
        backtest_start_time='2018-01-01 09:00:00',
        backtest_end_time='2019-01-01 09:00:00',
        backtest_initial_cash=20000,
        backtest_adjust=ADJUST_PREV)
