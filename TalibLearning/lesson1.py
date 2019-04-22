from gm.api import *
import numpy as np
import talib
import matplotlib.pylab as plt
set_token("0e5efcc5825e255db5d003f017b648dc4f877472")

data = history_n(symbol='SZSE.399006', frequency='3600s', count=1000, end_time='2018-12-31',
                 fields='close', fill_missing='later', adjust=ADJUST_PREV, df=True)
close = np.asarray(data['close'].values)
ma3 = talib.EMA(close, timeperiod = 3)
ma3 = ma3[~np.isnan(ma3)]
macd, signal, hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
macd = macd[~np.isnan(macd)]
macd_gradit = np.diff(macd, n=1)
macd_gradit = macd_gradit[~np.isnan(macd_gradit)]
plt.plot(macd_gradit)
plt.show()
