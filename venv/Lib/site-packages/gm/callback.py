# coding=utf-8
"""
回调任务分发
"""
from __future__ import unicode_literals, print_function, absolute_import

import collections
import datetime
import time

import six
from typing import Any, Dict, Text, List, Set, NoReturn

from gm.constant import CALLBACK_TYPE_TICK, CALLBACK_TYPE_BAR, \
    CALLBACK_TYPE_SCHEDULE, CALLBACK_TYPE_EXECRPT, \
    CALLBACK_TYPE_ORDER, CALLBACK_TYPE_INDICATOR, CALLBACK_TYPE_CASH, \
    CALLBACK_TYPE_POSITION, CALLBACK_TYPE_PARAMETERS, CALLBACK_TYPE_ERROR, \
    CALLBACK_TYPE_TIMER, CALLBACK_TYPE_BACKTEST_FINISH, CALLBACK_TYPE_STOP, \
    CALLBACK_TYPE_TRADE_CONNECTED, CALLBACK_TYPE_DATA_CONNECTED, \
    CALLBACK_TYPE_ACCOUNTSTATUS, CALLBACK_TYPE_DATA_DISCONNECTED, CALLBACK_TYPE_TRADE_DISCONNECTED, \
    CALLBACK_TYPE_INIT
from gm.csdk.c_sdk import BarLikeDict2, TickLikeDict2, gmi_now_plus
from gm.enum import MODE_BACKTEST, MODE_LIVE
from gm.model import DictLikeExecRpt, DictLikeOrder, DictLikeIndicator, DictLikeParameter, DictLikeAccountStatus, \
    DictLikeConnectionStatus, DictLikeError
from gm.model.storage import Context, context, BarWaitgroupInfo, BarSubInfo
from gm.pb.data_pb2 import Tick, Bar, Quote
from gm.pb.account_pb2 import ExecRpt, Order, Cash, Position, AccountStatus
from gm.pb.performance_pb2 import Indicator
from gm.pb.rtconf_pb2 import Parameters
from gm.pb_to_dict import protobuf_to_dict
from gm.utils import gmsdklogger, beijing_tzinfo, protobuf_timestamp2bj_datetime


def init_callback(data):
    context.bar_data_set.clear()  # 清空之前的
    if context.init_fun is not None:
        context.init_fun(context)


def tick_callback_new(data):
    tick = Tick()
    tick.ParseFromString(data)
    quotes = []
    for q in tick.quotes:  # type: Quote
        quotes.append({
            'bid_p': q.bid_p,
            'bid_v': q.bid_v,
            'ask_p': q.ask_p,
            'ask_v': q.ask_v,
        })

    if len(quotes) < 5:
        for _ in range(len(quotes), 5):
            zero_val = {'bid_p': 0, 'bid_v': 0, 'ask_p': 0, 'ask_v': 0}
            quotes.append(zero_val)

    ticknew = {
        'quotes': quotes,
        'symbol': tick.symbol,
        'created_at': protobuf_timestamp2bj_datetime(tick.created_at),
        'price': tick.price,
        'open': tick.open,
        'high': tick.high,
        'low': tick.low,
        'cum_volume': tick.cum_volume,
        'cum_amount': tick.cum_amount,
        'cum_position': tick.cum_position,
        'last_amount': tick.last_amount,
        'last_volume': tick.last_volume,
        'trade_type': tick.trade_type,
        'receive_local_time': time.time(),  # 收到时的本地时间秒数
    }
    ticknn = TickLikeDict2(ticknew)
    tick_callback(ticknn)


def tick_callback(data):
    tick = data  # type: TickLikeDict2
    symbol = tick['symbol']
    if symbol not in context.tick_sub_symbols:
        gmsdklogger.debug("tick data symbol=%s 不在订阅列表里, 跳过不处理", symbol)
        return

    if symbol not in context.tick_data_cache:
        gmsdklogger.debug("tick data's symbol= %s 在context.tick_data_cache key不存在, 加个key, deque长度为:%d", symbol,
                          context.max_tick_data_count)
        context.tick_data_cache[symbol] = collections.deque(maxlen=context.max_tick_data_count)

    context.tick_data_cache[symbol].appendleft(tick)
    if context.on_tick_fun is not None:
        context.on_tick_fun(context, tick)


# 回测模式下前一个eob的时间
pre_eob_in_backtest = None  # type: datetime.datetime
# 回测模式且wait_group下的bar集合. 以 frequency 作为 key
bars_in_waitgroup_backtest = collections.defaultdict(list)  # type: Dict[Text, List[BarLikeDict2]]
# 实时模式且wait_group下的bar集合  以 frequency 作为 一级key, eob做为二级key
bars_in_waitgroup_live = dict()  # type:  Dict[Text, Dict[datetime.datetime, List[BarLikeDict2]]]


def bar_callback_new(data):
    bar = Bar()
    bar.ParseFromString(data)
    barnew = {
        'symbol': bar.symbol,
        'eob': protobuf_timestamp2bj_datetime(bar.eob),
        'bob': protobuf_timestamp2bj_datetime(bar.bob),
        'open': bar.open,
        'close': bar.close,
        'high': bar.high,
        'low': bar.low,
        'volume': bar.volume,
        'amount': bar.amount,
        'pre_close': bar.pre_close,
        'position': bar.position,
        'frequency': bar.frequency,
        'receive_local_time': time.time(),  # 收到时的本地时间秒数
    }
    barnn = BarLikeDict2(barnew)
    bar_callback(barnn)


def bar_callback(data):
    global pre_eob_in_backtest, bars_in_waitgroup_backtest, bars_in_waitgroup_live
    bar = data  # type: BarLikeDict2
    symbol, frequency = bar['symbol'], bar['frequency']  # type: Text, Text
    if BarSubInfo(symbol, frequency) not in context.bar_sub_infos:
        gmsdklogger.debug("bar data symbol=%s frequency=%s 不在订阅列表里, 跳过不处理", symbol, frequency)
        return

    k = symbol + "_" + frequency
    # wait_group = True的情况下, 就先不要放入, 不然第一个symbol得到的数据跟别的symbol的数据对不齐
    if not context.has_wait_group:
        context.bar_data_cache[k].appendleft(bar)

    if context.on_bar_fun is None:
        return

    # 没有wait_group的情况, 那就直接发了
    if not context.has_wait_group:
        context.on_bar_fun(context, [bar, ])
        return

    # wait_group = True, 但是股票不在waitgroup的列表里时, 直接发了.
    # 在调用完 on_bar_fun 后, 在把数据放入到bar_data_cache里
    barwaitgroupinfo = context.bar_waitgroup_frequency2Info.get(frequency, BarWaitgroupInfo(frequency, 0))
    if not barwaitgroupinfo.is_symbol_in(symbol):
        gmsdklogger.debug('wait_group = True, 但是股票不在waitgroup的列表里时, 直接发了, symbol=%s, frequency=%s', symbol, frequency)
        context.on_bar_fun(context, [bar, ])
        context._add_bar2bar_data_cache(k, bar)
        return

    eob = bar['eob']  # type: datetime.datetime

    if context.mode == MODE_BACKTEST:  # 处理回测模式下, wait_group = True
        # 在回测模式下, 数据都是按顺序组织好的, 所以可以认为到下一个时间点时, 就把所有的数据统一放出来就好了
        if pre_eob_in_backtest is None:
            context._temporary_now = datetime.datetime.fromtimestamp(gmi_now_plus()).replace(tzinfo=beijing_tzinfo)
            pre_eob_in_backtest = eob
            bars_in_waitgroup_backtest[frequency].append(bar)
            context._add_bar2bar_data_cache(k, bar)
            return

        if pre_eob_in_backtest == eob:
            bars_in_waitgroup_backtest[frequency].append(bar)
            context._add_bar2bar_data_cache(k, bar)
            return

        if pre_eob_in_backtest < eob:  # 说明是下一个时间点了
            for bs in six.itervalues(bars_in_waitgroup_backtest):
                context.on_bar_fun(context, bs)

            context._add_bar2bar_data_cache(k, bar)

            pre_eob_in_backtest = eob
            context._temporary_now = datetime.datetime.fromtimestamp(gmi_now_plus()).replace(tzinfo=beijing_tzinfo)
            bars_in_waitgroup_backtest.clear()
            bars_in_waitgroup_backtest[frequency].append(bar)
            return

        return

    if context.mode == MODE_LIVE:  # 处理实时模式下, wait_group = True
        if frequency not in bars_in_waitgroup_live:
            bars_in_waitgroup_live[frequency] = dict()

        # 以eob做为key值, bar做为value值. 二级dict
        eob_bar_dict = bars_in_waitgroup_live[frequency]  # type: Dict[datetime.datetime, List[BarLikeDict2]]
        if eob not in eob_bar_dict:
            eob_bar_dict[eob] = [bar]
        else:
            eob_bar_dict[eob].append(bar)

        # 检查一下是否全部都到了. 到了的话触发一下
        if len(barwaitgroupinfo) == len(eob_bar_dict[eob]):
            gmsdklogger.debug("实时模式下, wait_group的bar都到齐了, 触发on_bar. eob=%s", eob)
            context.on_bar_fun(context, eob_bar_dict[eob])
            del eob_bar_dict[eob]
            context.bar_data_cache[k].appendleft(bar)
        else:
            context.bar_data_cache[k].appendleft(bar)

        return


def schedule_callback(data):
    # python 3 传过来的是bytes 类型， 转成str
    if isinstance(data, bytes):
        data = bytes.decode(data)

    schedule_func = context.inside_schedules.get(data)
    if not schedule_func:
        return

    schedule_func(context)


def _or_not_none(a, b):
    # type: (Any, Any) -> bool
    """
    两个中有一个不为None
    """
    return a is not None or b is not None


def excerpt_callback(data):
    if _or_not_none(context.on_execution_report_fun, context.on_execution_report_fun_v2):
        excerpt = ExecRpt()
        excerpt.ParseFromString(data)
        if context.on_execution_report_fun_v2 is not None:
            context.on_execution_report_fun_v2(context, excerpt)
            return

        excerpt = protobuf_to_dict(excerpt, including_default_value_fields=True, dcls=DictLikeExecRpt)
        context.on_execution_report_fun(context, excerpt)


def order_callback(data):
    if _or_not_none(context.on_order_status_fun, context.on_order_status_fun_v2):
        order = Order()
        order.ParseFromString(data)
        if context.on_order_status_fun_v2 is not None:
            context.on_order_status_fun_v2(context, order)
            return

        order = protobuf_to_dict(order, including_default_value_fields=True, dcls=DictLikeOrder)
        context.on_order_status_fun(context, order)


def indicator_callback(data):
    if _or_not_none(context.on_backtest_finished_fun, context.on_backtest_finished_fun_v2):
        indicator = Indicator()
        indicator.ParseFromString(data)
        if context.on_backtest_finished_fun_v2 is not None:
            context.on_backtest_finished_fun_v2(context, indicator)
            return

        indicator = protobuf_to_dict(indicator, including_default_value_fields=True, dcls=DictLikeIndicator)
        context.on_backtest_finished_fun(context, indicator)


def cash_callback(data):
    cash = Cash()
    cash.ParseFromString(data)
    cash = protobuf_to_dict(cash, including_default_value_fields=True)
    account_id = cash['account_id']
    accounts = context.accounts
    accounts[account_id].cash = cash


def position_callback(data):
    position = Position()
    position.ParseFromString(data)
    position = protobuf_to_dict(position, including_default_value_fields=True)
    symbol = position['symbol']
    side = position['side']
    account_id = position['account_id']
    accounts = context.accounts
    position_key = '{}.{}'.format(symbol, side)
    accounts[account_id].inside_positions[position_key] = position

    if not position.get('volume'):
        if accounts[account_id].inside_positions.get(position_key):
            return accounts[account_id].inside_positions.pop(position_key)


def parameters_callback(data):
    if _or_not_none(context.on_parameter_fun, context.on_parameter_fun_v2):
        parameters = Parameters()
        parameters.ParseFromString(data)
        if context.on_parameter_fun_v2 is not None:
            context.on_parameter_fun_v2(context, parameters.parameters[0])
            return

        parameters = [protobuf_to_dict(p, including_default_value_fields=True, dcls=DictLikeParameter) for p in
                      parameters.parameters]
        context.on_parameter_fun(context, parameters[0])


def default_err_callback(ctx, code, info):
    # type: (Context, Text, Text) -> NoReturn
    if code in ('1201', '1200'):
        gmsdklogger.warning(
            '行情重连中..., error code=%s, info=%s. 可用on_error事件处理', code, info
        )
    else:
        gmsdklogger.warning(
            '发生错误, 调用默认的处理函数, error code=%s, info=%s.  你可以在策略里自定义on_error函数接管它. 类似于on_tick',
            code, info
        )


def err_callback(data):
    """
    遇到错误时回调, 错误代码跟错误信息的对应关系参考: https://www.myquant.cn/docs/cpp/170
    """
    if context.on_error_fun is None:
        context.on_error_fun = default_err_callback

    try:
        data_unicode = data.decode('utf8')
        sparr = data_unicode.split('|', 1)
        if len(sparr) == 1:
            code, info = "code解析不出来", sparr[0]
        else:
            code, info = sparr
        context.on_error_fun(context, code, info)
    except Exception as e:
        gmsdklogger.exception("字符编码解析错误", e)
        context.on_error_fun(context, "1011", data)


# 已超时触发过的eob集合, 原则上是触发过的, 即可后面在收到数据也不再次触发
already_fire_timeout_eobs = set()  # type: Set[datetime.datetime]


def timer_callback(data):
    global bars_in_waitgroup_live, already_fire_timeout_eobs
    if (context.on_bar_fun is not None) and context.has_wait_group and context.is_live_model():
        # 这里处理实时模式下wait_group=true时, on_bar超时触发
        # 比较逻辑是: 取本地时间, 然后跟相同的eob的bars里的第1个bar的 receive_local_time (接收到时的本地时间) 相比
        cur_now_s = time.time()
        must_del_keys = []
        for frequency, eob_tick_dict in six.iteritems(bars_in_waitgroup_live):
            barwaitgroupinfo = context.bar_waitgroup_frequency2Info.get(frequency, None)
            if barwaitgroupinfo is not None:
                timeout_seconds = barwaitgroupinfo.timeout_seconds
                for eob_time in list(six.iterkeys(eob_tick_dict)):
                    first_bar = eob_tick_dict[eob_time][0]  # 这个eob下的收到的第1个bar
                    delta_second = cur_now_s - first_bar['receive_local_time']  # type: float
                    if delta_second >= timeout_seconds:
                        if eob_time in already_fire_timeout_eobs:
                            gmsdklogger.debug(
                                'frequency=%s eob=%s timeout_seconds=%d, 已超时触发过, 后面又收到数据, 不进行触发',
                                frequency, eob_time
                            )
                            del eob_tick_dict[eob_time]
                            continue

                        gmsdklogger.info(
                            "frequency=%s eob=%s timeout_seconds=%d 已超时了超时秒数=%s, 触发on_bar",
                            frequency, eob_time, timeout_seconds, delta_second
                        )
                        context.on_bar_fun(context, eob_tick_dict[eob_time])
                        del eob_tick_dict[eob_time]
                        already_fire_timeout_eobs.add(eob_time)
            else:
                # 说明有些 frequency 已经退订了
                gmsdklogger.debug("frequency =%s 已全部退订", frequency)
                must_del_keys.append(frequency)

        if must_del_keys:
            for k in must_del_keys:
                del bars_in_waitgroup_live[k]
        return


def backtest_finish_callback(data):
    global pre_eob_in_backtest, bars_in_waitgroup_backtest
    # 在回测结束前, 把之前累积的bar给放出来
    if bars_in_waitgroup_backtest:
        for bs in six.itervalues(bars_in_waitgroup_backtest):
            context.on_bar_fun(context, bs)

    pre_eob_in_backtest = None
    bars_in_waitgroup_backtest = collections.defaultdict(list)
    context._temporary_now = None
    context.bar_data_set.clear()  # 清空之前的
    context.bar_data_cache.clear()
    context.tick_data_cache.clear()
    context.max_tick_data_count = 1
    context.max_bar_data_count = 1


def stop_callback(data):
    if context.on_shutdown_fun is not None:
        context.on_shutdown_fun(context)

    from gm.api import stop
    print("!~~~~~~~~~~~!停止策略!~~~~~~~~~~~!")
    stop()


def trade_connected_callback():
    gmsdklogger.info("连接交易服务成功")
    if context.on_trade_data_connected_fun is not None:
        context.on_trade_data_connected_fun(context)


def data_connected_callback():
    gmsdklogger.info("连接行情服务成功")
    if context.on_market_data_connected_fun is not None:
        context.on_market_data_connected_fun(context)


def account_status_callback(data):
    if _or_not_none(context.on_account_status_fun, context.on_account_status_fun_v2):
        account_status = AccountStatus()
        account_status.ParseFromString(data)
        if context.on_account_status_fun_v2 is not None:
            context.on_account_status_fun_v2(context, account_status)
            return

        # account_status = protobuf_to_dict(account_status)   # 之前的

        account_status_dict = DictLikeAccountStatus()
        account_status_dict['account_id'] = account_status.account_id
        account_status_dict['account_name'] = account_status.account_name

        status_dict = DictLikeConnectionStatus()
        account_status_dict['status'] = status_dict
        if account_status.status is not None:
            status_dict['state'] = account_status.status.state
            error_dict = DictLikeError()
            status_dict['error'] = error_dict
            if account_status.status.error is not None:
                error_dict['code'] = account_status.status.error.code
                error_dict['type'] = account_status.status.error.type
                error_dict['info'] = account_status.status.error.info

        context.on_account_status_fun(context, account_status_dict)


def data_disconnected_callback():
    if context.on_market_data_disconnected_fun is not None:
        context.on_market_data_disconnected_fun(context)


def trade_disconnected_callback():
    if context.on_trade_data_disconnected_fun is not None:
        context.on_trade_data_disconnected_fun(context)


def callback_controller(msg_type, data):
    """
    回调任务控制器
    """
    try:
        # python 3 传过来的是bytes 类型， 转成str
        if isinstance(msg_type, bytes):
            msg_type = bytes.decode(msg_type)

        if msg_type == CALLBACK_TYPE_TICK:
            return tick_callback_new(data)

        if msg_type == CALLBACK_TYPE_BAR:
            return bar_callback_new(data)

        if msg_type == CALLBACK_TYPE_INIT:
            return init_callback(data)

        if msg_type == CALLBACK_TYPE_SCHEDULE:
            return schedule_callback(data)

        if msg_type == CALLBACK_TYPE_ERROR:
            return err_callback(data)

        if msg_type == CALLBACK_TYPE_TIMER:
            return timer_callback(data)

        if msg_type == CALLBACK_TYPE_EXECRPT:
            return excerpt_callback(data)

        if msg_type == CALLBACK_TYPE_ORDER:
            return order_callback(data)

        if msg_type == CALLBACK_TYPE_INDICATOR:
            return indicator_callback(data)

        if msg_type == CALLBACK_TYPE_CASH:
            return cash_callback(data)

        if msg_type == CALLBACK_TYPE_POSITION:
            return position_callback(data)

        if msg_type == CALLBACK_TYPE_PARAMETERS:
            return parameters_callback(data)

        if msg_type == CALLBACK_TYPE_BACKTEST_FINISH:
            return backtest_finish_callback(data)

        if msg_type == CALLBACK_TYPE_STOP:
            return stop_callback(data)

        if msg_type == CALLBACK_TYPE_TRADE_CONNECTED:
            return trade_connected_callback()

        if msg_type == CALLBACK_TYPE_TRADE_DISCONNECTED:
            return trade_disconnected_callback()

        if msg_type == CALLBACK_TYPE_DATA_CONNECTED:
            return data_connected_callback()

        if msg_type == CALLBACK_TYPE_DATA_DISCONNECTED:
            return data_disconnected_callback()

        if msg_type == CALLBACK_TYPE_ACCOUNTSTATUS:
            return account_status_callback(data)

        gmsdklogger.warn("没有处理消息:%s的处理函数", msg_type)

    except SystemExit:
        gmsdklogger.exception("^^--------------SystemExit--------------^^")
        from gm.api import stop
        stop()

    except BaseException as e:
        gmsdklogger.exception("^^--------------遇到exception--------------^^")
        from gm.api import stop
        stop()
