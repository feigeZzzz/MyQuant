# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import

import collections
import datetime
import struct
import sys
import sysconfig

import pandas as pd
from typing import NoReturn, Text, Dict, Any, List, Set, Sequence, Union, Deque

from gm import __version__
from gm.constant import DATA_TYPE_TICK
from gm.csdk.c_sdk import BarLikeDict2, TickLikeDict2, py_gmi_get_cash, py_gmi_get_positions, \
    py_gmi_get_accounts, py_gmi_set_timer, gmi_now_plus, c_status_fail
from gm.enum import MODE_BACKTEST, MODE_LIVE
from gm.model.account import Account
from gm.pb.account_pb2 import Positions, Cashes, Accounts, Account as PbAccount
from gm.pb.trade_pb2 import GetCashReq, GetPositionsReq
from gm.pb_to_dict import protobuf_to_dict
from gm.utils import adjust_frequency, gmsdklogger, beijing_tzinfo


class BarSubInfo(object):
    __slots__ = ['symbol', 'frequency']

    def __init__(self, symbol, frequency):
        self.symbol = symbol  # type: Text
        self.frequency = frequency  # type: Text

    def __hash__(self):
        return hash((self.symbol, self.frequency))

    def __eq__(self, other):
        if not isinstance(other, BarSubInfo):
            return False

        return (self.symbol, self.frequency) == (other.symbol, other.frequency)


class BarWaitgroupInfo(object):
    __slots__ = ['symbols', 'frequency', 'timeout_seconds']

    def __init__(self, frequency, timeout_seconds):
        self.symbols = set()  # type: Set[Text]
        self.frequency = frequency  # type: Text
        self.timeout_seconds = timeout_seconds  # type: int

    def add_one_symbol(self, symbol):
        # type: (Text) ->NoReturn
        self.symbols.add(symbol)

    def add_symbols(self, syms):
        # type: (Sequence[Text]) ->NoReturn
        self.symbols.union(syms)

    def remove_one_symbol(self, symbol):
        # type: (Text) ->NoReturn
        self.symbols.discard(symbol)

    def is_symbol_in(self, symbol):
        # type: (Text) -> bool
        return symbol in self.symbols

    def __len__(self):
        return len(self.symbols)


class DefaultFileModule(object):
    def on_tick(self, ctx, tick):
        print('请初始化on_tick方法')

    def on_bar(self, ctx, bar):
        print('请初始化on_bar方法')

    def on_bod(self, ctx, bod):
        print('请初始化on_bod方法')

    def on_eod(self, ctx, eod):
        print('请初始化on_eod方法')


class Context(object):
    """
    策略运行的上下文类. 这在整个进程中要保证是单一实例
    注意: 一个运行的python进程只能运行一个策略.
    警告: 客户写的策略代码不要直接使用这个类来实例化, 而是使用 sdk 实例化好的 context 实例
    """
    inside_file_module = DefaultFileModule()
    on_bar_fun = None
    on_tick_fun = None
    init_fun = None
    on_execution_report_fun = None
    on_execution_report_fun_v2 = None
    on_order_status_fun = None
    on_order_status_fun_v2 = None
    on_backtest_finished_fun = None
    on_backtest_finished_fun_v2 = None
    on_parameter_fun = None
    on_parameter_fun_v2 = None
    on_error_fun = None
    on_shutdown_fun = None
    on_trade_data_connected_fun = None
    on_market_data_connected_fun = None
    on_account_status_fun = None
    on_account_status_fun_v2 = None
    on_market_data_disconnected_fun = None
    on_trade_data_disconnected_fun = None

    strategy_id = ''  # type: Text
    token = None  # type: Text
    mode = None  # type: int
    backtest_and_not_wait_group = False  # type: bool
    _temporary_now = None  # type: datetime.datetime  # 用于回测模式下, 且wait_group=True时, 要修改context.now 时的值, 因为这时时钟是走到了下一个时刻, 而数据还是上一时刻的, 所以要修改时钟为上一时刻,跟数据时间一致
    backtest_start_time = None  # type: Text
    backtest_end_time = None  # type: Text
    adjust_mode = None  # type: int
    inside_schedules = {}  # type: Dict[Text, Any]

    sdk_lang = "python{}.{}".format(sys.version_info.major, sys.version_info.minor)  # type: Text
    sdk_version = __version__.__version__  # type: Text
    sdk_arch = str(struct.calcsize("P") * 8)  # type: Text
    sdk_os = sysconfig.get_platform()  # type: Text

    tick_data_cache = dict()  # type: Dict[Text, Deque[Any]]
    max_tick_data_count = 1
    bar_data_cache = dict()  # type: Dict[Text, Deque[Any]]  # 以 bar.symbol+bar.frequency作为key
    max_bar_data_count = 1
    bar_data_set = set()  # type: Set  # 保存已有的bar的 (symbol, frequency, eob), 用于判断是否重复值
    tick_sub_symbols = set()  # type: Set[Text]   # 订阅tick的symbol
    bar_sub_infos = set()  # type: Set[BarSubInfo]   # 订阅bar的信息集合
    # 订阅bar用freequency做为key, 相应的股票集合做为value
    bar_waitgroup_frequency2Info = dict()  # type: Dict[Text, BarWaitgroupInfo]

    is_set_onbar_timeout_check = False

    def __init__(self):
        self.inside_accounts = {}  # type: Dict[Text, Account]

    def _set_onbar_waitgroup_timeout_check(self):
        if self.is_live_model() and not self.is_set_onbar_timeout_check:
            # 实时模式下 3000毫秒触发一次timer事件 用来处理wait_group的过期.
            # fixme 这里底层不支持动态设置多个, 先固定一个吧
            py_gmi_set_timer(3000)
            self.is_set_onbar_timeout_check = True

    def _add_bar2bar_data_cache(self, k, bar):
        # type: (Text, Dict[Text, Any]) -> NoReturn
        kk = (bar['symbol'], bar['frequency'], bar['eob'])
        if kk in self.bar_data_set:
            gmsdklogger.debug("bar data %s 已存在, 跳过不加入", kk)
        else:
            if k not in context.bar_data_cache:
                gmsdklogger.debug("bar data %s 在context.bar_data_cache相应的key=%s不存在, 加个key, deque长度为:%d", kk, k,
                                  context.max_bar_data_count)
                context.bar_data_cache[k] = collections.deque(maxlen=context.max_bar_data_count)

            context.bar_data_cache[k].appendleft(bar)
            self.bar_data_set.add(kk)

    @property
    def has_wait_group(self):
        # type: () ->bool
        return len(self.bar_waitgroup_frequency2Info) > 0

    @property
    def now(self):
        # type: ()->datetime.datetime
        """
        实时模式返回当前本地时间, 回测模式返回当前回测时间
        """
        if self._temporary_now:  # 这个是在回测模式且wait_group=True的情况下时存在的
            if self._temporary_now.tzinfo is None:
                return self._temporary_now.replace(tzinfo=beijing_tzinfo)
            return self._temporary_now

        now = gmi_now_plus()
        # now == 0 说明是回测模式而且处于init装填 c sdk拿不到时间
        if now == 0:
            return datetime.datetime.strptime(context.backtest_start_time, "%Y-%m-%d %H:%M:%S").replace(
                tzinfo=beijing_tzinfo)

        return datetime.datetime.fromtimestamp(now).replace(tzinfo=beijing_tzinfo)

    @property
    def symbols(self):
        # type: ()->Set[Text]
        """
        订阅bar跟tick的symbol集合
        bar 的symbols + tick 的symbols
        """
        return set(barsub.symbol for barsub in self.bar_sub_infos).union(self.tick_sub_symbols)

    @property
    def accounts(self):
        # type: ()->Dict[Text, Account]
        """
        用户资金 & 持仓情况
        """
        if not self.inside_accounts:
            self._set_accounts()

        return self.inside_accounts

    def account(self, account_id=''):
        accounts = self.accounts
        # 只有一个账户 且未有account_id 的情况下返回唯一用户
        if not account_id and len(accounts) == 1:
            default_id = sorted(accounts.keys())[0]
            return accounts.get(default_id)

        return accounts.get(account_id)

    @property
    def parameters(self):
        """
        动态参数
        """
        from gm.api.basic import get_parameters
        parameters = get_parameters()
        return {p['key']: p for p in parameters}

    def _set_accounts(self):
        status, data = py_gmi_get_accounts()
        if c_status_fail(status, 'py_gmi_get_accounts'):
            return

        accounts = Accounts()
        accounts.ParseFromString(data)
        for account in accounts.data:  # type: PbAccount
            self._get_account_info(account.account_id, account.account_name)

    @staticmethod
    def data(symbol, frequency, count=1, fields='', bar_df=True):
        # type: (Text, Text, int, Text, bool) -> Union[List[Union[TickLikeDict2, BarLikeDict2]], pd.DataFrame]
        """
        获取订阅的bar或tick滑窗，数据为包含当前时刻推送bar或tick的前count条bar(tick)数据.
        注意: 为了兼容之前的sdk版本, 在 frequency 为非 tick 的情况下, 返回的数据类型为 pandas的DataFrame.
        你可以显示的设置参数 bar_df=False, 这样返回的的数据是 List[BarLikeDict2].
        frequency为tick时, 返回的数据类型为 List[TickLikeDict2]
        fields 参数的取值情况:
          1. 当 frequency == 'tick' 时, fields的取值可以为:'quotes,symbol,created_at,price,open,high,low,cum_volume,cum_amount,cum_position,last_amount,last_volume,trade_type'
          2. 当 数据为bar时, fields的取值可以为: 'symbol,eob,bob,open,close,high,low,volume,amount,pre_close,position,frequency'
        """
        symbol = symbol.strip()
        if ',' in symbol:
            gmsdklogger.warning('不支持返回多个symbol, 返回空list')
            return []
        if ',' in frequency:
            gmsdklogger.warning('不支持多个频率, 返回空list')
            return []

        if count < 1:
            count = 1
        frequency = adjust_frequency(frequency)
        if frequency == DATA_TYPE_TICK:
            if symbol in context.tick_data_cache:
                symbol_tick_queue = context.tick_data_cache[symbol]  # type: collections.deque
                if count > symbol_tick_queue.maxlen:
                    count = symbol_tick_queue.maxlen
                if count > len(symbol_tick_queue):
                    # 数据不够, 说明要补数据
                    delta_count = symbol_tick_queue.maxlen - len(symbol_tick_queue)
                    from gm.api.query import history_n
                    if len(symbol_tick_queue) == 0:
                        query_data_end_time = context.now
                    else:
                        query_data_end_time = symbol_tick_queue[-1]['created_at']
                    tick_datas = history_n(symbol=symbol, frequency=frequency, count=delta_count,
                                           end_time=query_data_end_time)
                    tick_datas_trans = list()  # type: List[TickLikeDict2]
                    for bd in tick_datas:
                        tick_datas_trans.append(TickLikeDict2(data=bd))

                    comb_tick_datas = list(symbol_tick_queue) + tick_datas_trans  # type: List[TickLikeDict2]
                    # 排除掉重复的数据
                    tick_key_set = set()
                    new_tick_datas = list()  # type: List[TickLikeDict2]
                    for tick_item in comb_tick_datas:
                        kk = (tick_item['symbol'], tick_item['created_at'])
                        if kk not in tick_key_set:
                            tick_key_set.add(kk)
                            new_tick_datas.append(tick_item)

                    new_tick_datas.sort(key=lambda item: item['created_at'])
                    symbol_tick_queue.clear()
                    symbol_tick_queue.extendleft(new_tick_datas)

                # 按要求取数据
                d = [v for idx, v in enumerate(symbol_tick_queue) if idx < count]
                d.reverse()
                if len(fields) == 0:
                    return d
                else:  # 用户指定字段的情况, 进行字段的筛选
                    all_fields = {'quotes', 'symbol', 'created_at', 'price', 'open', 'high', 'low', 'cum_volume',
                                  'cum_amount', 'cum_position', 'last_amount', 'last_volume', 'trade_type'}
                    filter_fields = []
                    for f in fields.lower().strip().split(','):
                        f = f.strip()
                        if f in all_fields:
                            filter_fields.append(f)

                    if len(filter_fields) == 0:
                        return []

                    dd = []
                    for bar_data_item in d:
                        item = {}
                        for f in filter_fields:
                            item[f] = bar_data_item.data.get(f)
                        dd.append(TickLikeDict2(data=item))
                    return dd
            else:
                return []
        else:  # bar type
            all_fields = {'symbol', 'eob', 'bob', 'open', 'close', 'high', 'low', 'volume', 'amount', 'pre_close',
                          'position', 'frequency', }
            filter_fields = []
            for f in fields.lower().strip().split(','):
                f = f.strip()
                if f in all_fields:
                    filter_fields.append(f)

            k = symbol + "_" + frequency
            if k in context.bar_data_cache:
                symbol_bar_queue = context.bar_data_cache[k]  # type: collections.deque
                if count > symbol_bar_queue.maxlen:
                    count = symbol_bar_queue.maxlen
                if count > len(symbol_bar_queue):
                    # 数据不够, 说明要补数据
                    delta_count = symbol_bar_queue.maxlen - len(symbol_bar_queue) + 1
                    from gm.api.query import history_n
                    if len(symbol_bar_queue) == 0:
                        query_data_end_time = context.now
                    else:
                        query_data_end_time = symbol_bar_queue[-1]['eob']
                    bar_datas = history_n(symbol=symbol, frequency=frequency, count=delta_count,
                                          end_time=query_data_end_time)

                    bar_datas_trans = list()  # type: List[BarLikeDict2]
                    for bd in bar_datas:
                        if frequency == '1d':  # 1d的话统一替换成 15:15:01
                            bd['eob'] = bd['eob'].replace(hour=15, minute=15, second=1)
                        bar_datas_trans.append(BarLikeDict2(data=bd))

                    comb_bar_datas = list(symbol_bar_queue) + bar_datas_trans  # type: List[BarLikeDict2]
                    # 排除掉重复的数据
                    bar_key_set = set()
                    new_bar_datas = list()  # type: List[BarLikeDict2]
                    for bar_item in comb_bar_datas:
                        kk = (bar_item['symbol'], bar_item['frequency'], bar_item['eob'])
                        if kk not in bar_key_set:
                            bar_key_set.add(kk)
                            new_bar_datas.append(bar_item)
                            context.bar_data_set.add(bar_item)

                    new_bar_datas.sort(key=lambda item: item['eob'])
                    symbol_bar_queue.clear()
                    symbol_bar_queue.extendleft(new_bar_datas)

                # 按要求取数据
                d = [v for idx, v in enumerate(symbol_bar_queue) if idx < count]  # type: List[BarLikeDict2]
                d.reverse()
                if bar_df:
                    if len(fields) == 0:
                        td = [{
                            'symbol': item.symbol,
                            'eob': item.eob,
                            'bob': item.bob,
                            'open': item.open,
                            'close': item.close,
                            'high': item.high,
                            'low': item.low,
                            'amount': item.amount,
                            'pre_close': item.pre_close,
                            'position': item.position,
                            'frequency': item.frequency,
                            'volume': item.volume,
                        } for item in d]
                        return pd.DataFrame(data=td)
                    else:  # 用户指定字段的情况
                        dd = []
                        for tick_item in d:
                            item = {}
                            for f in filter_fields:
                                item[f] = tick_item.data.get(f)
                            dd.append(item)
                        return pd.DataFrame(data=dd)
                else:
                    if len(fields) == 0:
                        return d
                    else:  # 用户指定字段的情况
                        dd = []
                        for tick_item in d:
                            item = {}
                            for f in filter_fields:
                                item[f] = tick_item.data.get(f)
                            dd.append(BarLikeDict2(data=item))
                        return dd
            else:
                if bar_df:
                    if len(fields) == 0:
                        return pd.DataFrame(
                            columns=['symbol', 'eob', 'bob', 'open', 'close', 'high', 'low', 'volume', 'amount',
                                     'pre_close', 'position', 'frequency'])
                    else:  # 用户指定字段的情况
                        return pd.DataFrame(columns=filter_fields)
                else:
                    return []

    def _get_account_info(self, account_id, account_name):
        # 资金信息
        req = GetCashReq()
        req.account_id = account_id
        req = req.SerializeToString()
        status, result = py_gmi_get_cash(req)
        if c_status_fail(status, 'py_gmi_get_cash'):
            return

        cashes = Cashes()
        cashes.ParseFromString(result)
        cashes = [protobuf_to_dict(cash) for cash in cashes.data]
        cash = cashes[0]

        # 持仓信息
        req = GetPositionsReq()
        req.account_id = account_id
        req = req.SerializeToString()
        status, result = py_gmi_get_positions(req)
        if c_status_fail(status, 'py_gmi_get_positions'):
            return

        positions = Positions()
        positions.ParseFromString(result)

        positions = [protobuf_to_dict(position, including_default_value_fields=True) for position in positions.data]
        positions_infos = {'{}.{}'.format(position['symbol'], position['side']): position for position in positions}

        account = Account(account_id, account_name, cash, positions_infos)
        self.inside_accounts[account_id] = account

    def is_backtest_model(self):
        # type: () ->bool
        """
        是否回测模式
        """
        return self.mode == MODE_BACKTEST

    def is_live_model(self):
        # type: () ->bool
        """
        是否实时模式
        """
        return self.mode == MODE_LIVE


# 提供给API的唯一上下文实例
context = Context()
