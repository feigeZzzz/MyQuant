# coding=utf-8
from __future__ import print_function, absolute_import, unicode_literals

import collections
import os
import sys
from importlib import import_module
from optparse import OptionParser

import six
from typing import Text, List, Dict, NoReturn, Any

from gm.__version__ import __version__
from gm.callback import callback_controller
from gm.constant import DATA_TYPE_TICK, SCHEDULE_INFO
from gm.csdk.c_sdk import py_gmi_current, py_gmi_schedule, py_gmi_set_data_callback, py_gmi_set_strategy_id, \
    gmi_set_mode, py_gmi_set_backtest_config, py_gmi_subscribe, py_gmi_set_token, py_gmi_unsubscribe, \
    py_gmi_get_parameters, py_gmi_add_parameters, py_gmi_set_parameters, py_gmi_log, py_gmi_strerror, \
    py_gmi_run, py_gmi_set_serv_addr, gmi_init, gmi_poll, gmi_get_c_version, py_gmi_set_apitoken, c_status_fail
from gm.enum import MODE_UNKNOWN, ADJUST_NONE, MODE_BACKTEST, MODE_LIVE, ADJUST_POST, ADJUST_PREV
from gm.model.storage import context, BarSubInfo, BarWaitgroupInfo
from gm.pb.common_pb2 import Logs, Log
from gm.pb.data_pb2 import Ticks
from gm.pb.rtconf_pb2 import Parameters, Parameter
from gm.pb.rtconf_service_pb2 import GetParametersReq
from gm.pb_to_dict import protobuf_to_dict
from gm.utils import load_to_list, load_to_second, adjust_frequency, GmSymbols, gmsdklogger

running = True


def _unsubscribe_all():
    context.bar_sub_infos.clear()
    context.tick_sub_symbols.clear()
    context.bar_waitgroup_frequency2Info.clear()
    context.bar_data_cache.clear()
    context.tick_data_cache.clear()
    context.max_tick_data_count = 1
    context.max_bar_data_count = 1


def set_token(token):
    # type: (Text) ->NoReturn
    """
    设置用户的token，用于身份认证
    """
    py_gmi_set_token(token)
    context.token = str('bearer {}'.format(token))


def get_version():
    # type: () ->Text
    return __version__


def subscribe(symbols, frequency='1d', count=1, wait_group=False, wait_group_timeout='10s', unsubscribe_previous=False):
    # type:(GmSymbols, Text, int, bool, Text, bool) ->NoReturn
    """
    订阅行情，可以指定symbol， 数据滑窗大小，以及是否需要等待全部代码的数据到齐再触发事件。
    wait_group: 是否等待全部相同频度订阅的symbol到齐再触发on_bar事件。
    一个 frequency, 只能有一个 wait_group_timeout 也就是说如果后面调用该函数时, 相同的frequency, 但是 wait_group_timeout 不同,
    则 wait_group_timeout 被忽略.
    同时要注意, 一个symbol与frequency组合, 只能有一种wait_group, 即wait_group要么为true, 要么为false
    """
    frequency = adjust_frequency(frequency)

    symbols = load_to_list(symbols)
    symbols_str = ','.join(symbols)
    status = py_gmi_subscribe(symbols_str, frequency, unsubscribe_previous)
    if c_status_fail(status, 'py_gmi_subscribe'):
        return

    if unsubscribe_previous:
        _unsubscribe_all()

    if frequency == DATA_TYPE_TICK:
        if context.max_tick_data_count < count:
            context.max_tick_data_count = count
        for sy in symbols:
            context.tick_data_cache[sy] = collections.deque(maxlen=count)
            context.tick_sub_symbols.add(sy)
        return

    # 处理订阅bar的情况
    context._set_onbar_waitgroup_timeout_check()
    wait_group_timeoutint = load_to_second(wait_group_timeout)
    if context.max_bar_data_count < count:
        context.max_bar_data_count = count
    for sy in symbols:
        context.bar_data_cache["{}_{}".format(sy, frequency)] = collections.deque(maxlen=count)
        barsubinfo = BarSubInfo(sy, frequency)
        if barsubinfo not in context.bar_sub_infos:
            context.bar_sub_infos.add(barsubinfo)
            if wait_group:
                if frequency not in context.bar_waitgroup_frequency2Info:
                    context.bar_waitgroup_frequency2Info[frequency] = BarWaitgroupInfo(frequency, wait_group_timeoutint)
                context.bar_waitgroup_frequency2Info[frequency].add_one_symbol(sy)
        else:
            gmsdklogger.debug("symbol=%s frequency=%s 已订阅过", sy, frequency)
            continue


def unsubscribe(symbols, frequency='1d'):
    # type: (GmSymbols, Text) ->NoReturn
    """
    unsubscribe - 取消行情订阅

    取消行情订阅，默认取消所有已订阅行情
    """
    symbols = load_to_list(symbols)
    symbols_str = ','.join(symbols)
    frequency = adjust_frequency(frequency)

    status = py_gmi_unsubscribe(symbols_str, frequency)
    if c_status_fail(status, 'py_gmi_unsubscribe'):
        return

    if symbols_str == '*':
        _unsubscribe_all()
        return

    if frequency == DATA_TYPE_TICK:
        for sy in symbols:
            if sy in list(six.iterkeys(context.tick_data_cache)):
                del context.tick_data_cache[sy]
                context.tick_sub_symbols.remove(sy)
        return

    # 处理bar的退订
    for sy in symbols:
        k = sy + "_" + frequency
        if k in list(six.iterkeys(context.bar_data_cache)):
            del context.bar_data_cache[k]
            context.bar_sub_infos.remove(BarSubInfo(sy, frequency))
            barwaitgroupinfo = context.bar_waitgroup_frequency2Info.get(frequency, None)
            if barwaitgroupinfo:
                barwaitgroupinfo.remove_one_symbol(sy)

    # 处理已全部退订的 frequency
    for frequency in list(six.iterkeys(context.bar_waitgroup_frequency2Info)):
        if len(context.bar_waitgroup_frequency2Info[frequency]) == 0:
            gmsdklogger.debug('frequency=%s 已全部取消订阅', frequency)
            del context.bar_waitgroup_frequency2Info[frequency]


def current(symbols, fields=''):
    # type: (GmSymbols, Text) -> List[Any]
    """
    查询当前行情快照，返回tick数据
    """
    symbols = load_to_list(symbols)
    fields = load_to_list(fields)

    symbols_str = ','.join(symbols)
    fields_str = ','.join(fields)

    ticks = Ticks()
    status, data = py_gmi_current(symbols_str, fields_str)
    if c_status_fail(status, 'py_gmi_current'):
        return []

    ticks.ParseFromString(data)
    ticks = [protobuf_to_dict(tick, including_default_value_fields=False) for tick in ticks.data]
    if not fields:
        return ticks

    return ticks


def get_strerror(error_code):
    # type: (int) -> Text
    return py_gmi_strerror(error_code)


def schedule(schedule_func, date_rule, time_rule):
    # type: (Any, Text, Text) ->NoReturn
    """
    定时任务. 这里的schedule_func 要求只能有一个context参数的函数
    """
    schemdule_info = SCHEDULE_INFO.format(date_rule=date_rule, time_rule=time_rule)
    context.inside_schedules[schemdule_info] = schedule_func
    py_gmi_schedule(date_rule, time_rule)


def _all_not_none(a, b):
    # type: (Any, Any) -> bool
    """
    全部都不为None
    """
    return a is not None and b is not None


def run(strategy_id='', filename='', mode=MODE_UNKNOWN, token='',
        backtest_start_time='',
        backtest_end_time='',
        backtest_initial_cash=1000000,
        backtest_transaction_ratio=1,
        backtest_commission_ratio=0,
        backtest_slippage_ratio=0,
        backtest_adjust=ADJUST_NONE,
        backtest_check_cache=1,
        serv_addr=''):
    # type: (Text, Text, int, Text, Text, Text, float, float, float, float, int, int, Text) ->NoReturn
    """
    执行策略
    """

    parser = OptionParser()
    parser.add_option("--strategy_id", action="store",
                      dest="strategy_id",
                      default=strategy_id,
                      help="策略id")

    parser.add_option("--filename", action="store",
                      dest="filename",
                      default=filename,
                      help="策略文件名称")

    parser.add_option("--mode", action="store",
                      dest="mode",
                      default=mode,
                      help="策略模式选择")

    parser.add_option("--token", action="store",
                      dest="token",
                      default=token,
                      help="用户token")

    parser.add_option("--apitoken", action="store",
                      dest="apitoken",
                      default='',
                      help="用户token")

    parser.add_option("--backtest_start_time", action="store",
                      dest="backtest_start_time",
                      default=backtest_start_time,
                      help="回测开始时间")

    parser.add_option("--backtest_end_time", action="store",
                      dest="backtest_end_time",
                      default=backtest_end_time,
                      help="回测结束时间")

    parser.add_option("--backtest_initial_cash", action="store",
                      dest="backtest_initial_cash",
                      default=backtest_initial_cash,
                      help="回测初始资金")

    parser.add_option("--backtest_transaction_ratio", action="store",
                      dest="backtest_transaction_ratio",
                      default=backtest_transaction_ratio,
                      help="回测交易费率")

    parser.add_option("--backtest_commission_ratio", action="store",
                      dest="backtest_commission_ratio",
                      default=backtest_commission_ratio,
                      help="回测成交比率")

    parser.add_option("--backtest_slippage_ratio", action="store",
                      dest="backtest_slippage_ratio",
                      default=backtest_slippage_ratio,
                      help="回测滑点费率")

    parser.add_option("--backtest_adjust", action="store",
                      dest="backtest_adjust",
                      default=backtest_adjust,
                      help="回测复权模式")

    parser.add_option("--backtest_check_cache", action="store",
                      dest="backtest_check_cache",
                      default=backtest_check_cache,
                      help="回测是否使用缓存")

    parser.add_option("--serv_addr", action="store",
                      dest="serv_addr",
                      default=serv_addr,
                      help="终端地址")

    (options, args) = parser.parse_args()
    strategy_id = options.strategy_id
    filename = options.filename
    mode = int(options.mode)
    if mode not in (MODE_UNKNOWN, MODE_LIVE, MODE_BACKTEST):
        raise ValueError('模式只能设置成 MODE_UNKNOWN, MODE_LIVE, MODE_BACKTEST 值')

    token = options.token
    apitoken = options.apitoken
    backtest_start_time = options.backtest_start_time
    backtest_end_time = options.backtest_end_time
    backtest_initial_cash = float(options.backtest_initial_cash)
    backtest_transaction_ratio = float(options.backtest_transaction_ratio)
    backtest_commission_ratio = float(options.backtest_commission_ratio)
    backtest_slippage_ratio = float(options.backtest_slippage_ratio)
    backtest_adjust = int(options.backtest_adjust)
    if backtest_adjust == 3:
        backtest_adjust = ADJUST_NONE  # 这个修改是为了适合终端之前把 3 认为是 不复权
    if backtest_adjust not in (ADJUST_NONE, ADJUST_POST, ADJUST_PREV):
        raise ValueError('回测复权模式只能设置成 ADJUST_NONE, ADJUST_POST, ADJUST_PREV 值')

    if backtest_initial_cash < 1:
        raise ValueError('回测初始资金不能设置为小于1, 当前值为:{}'.format(backtest_initial_cash))

    if not 0 <= backtest_transaction_ratio <= 1:
        raise ValueError('回测成交比例允许的范围值为 0<=x<=1, 当前值为{}'.format(backtest_transaction_ratio))

    if not 0 <= backtest_commission_ratio <= 0.1:
        raise ValueError('回测佣金比例允许的范围值为 0<=x<=0.1, 当前值为{}'.format(backtest_commission_ratio))

    if not 0 <= backtest_slippage_ratio <= 0.1:
        raise ValueError('回测滑点比例允许的范围值为 0<=x<=0.1, 当前值为{}'.format(backtest_slippage_ratio))

    backtest_check_cache = int(options.backtest_check_cache)
    serv_addr = options.serv_addr

    from gm import api

    # 处理用户传入 __file__这个特殊变量的情况
    syspathes = set(s.replace('\\', '/') for s in sys.path)
    commonpaths = [os.path.commonprefix([p, filename]) for p in syspathes]
    commonpaths.sort(key=lambda s: len(s), reverse=True)
    maxcommonpath = commonpaths[0]
    filename = filename.replace(maxcommonpath, '')  # type: str
    if filename.startswith('/'):
        filename = filename[1:]

    if filename.endswith(".py"):
        filename = filename[:-3]
    filename = filename.replace("/", ".")
    filename = filename.replace('\\', ".")
    fmodule = import_module(filename)

    # 把gm.api里的所有的符号都导出到当前策略文件(fmodule)的命令空间, 方便使用
    for name in api.__all__:
        if name not in fmodule.__dict__:
            fmodule.__dict__[name] = getattr(api, name)

    # 服务地址设置
    if serv_addr:
        set_serv_addr(serv_addr)

    set_token(token)
    py_gmi_set_apitoken(apitoken)

    py_gmi_set_strategy_id(strategy_id)
    gmi_set_mode(mode)
    context.mode = mode
    context.strategy_id = strategy_id

    # 调用户文件的init
    context.inside_file_module = fmodule
    context.on_tick_fun = getattr(fmodule, 'on_tick', None)
    context.on_bar_fun = getattr(fmodule, 'on_bar', None)
    context.init_fun = getattr(fmodule, 'init', None)
    context.on_execution_report_fun = getattr(fmodule, 'on_execution_report', None)
    context.on_execution_report_fun_v2 = getattr(fmodule, 'on_execution_report_v2', None)
    context.on_order_status_fun = getattr(fmodule, 'on_order_status', None)
    context.on_order_status_fun_v2 = getattr(fmodule, 'on_order_status_v2', None)
    context.on_backtest_finished_fun = getattr(fmodule, 'on_backtest_finished', None)
    context.on_backtest_finished_fun_v2 = getattr(fmodule, 'on_backtest_finished_v2', None)
    context.on_parameter_fun = getattr(fmodule, 'on_parameter', None)
    context.on_parameter_fun_v2 = getattr(fmodule, 'on_parameter_v2', None)
    context.on_error_fun = getattr(fmodule, 'on_error', None)
    context.on_shutdown_fun = getattr(fmodule, 'on_shutdown', None)
    context.on_trade_data_connected_fun = getattr(fmodule, 'on_trade_data_connected', None)
    context.on_market_data_connected_fun = getattr(fmodule, 'on_market_data_connected', None)
    context.on_account_status_fun = getattr(fmodule, 'on_account_status', None)
    context.on_account_status_fun_v2 = getattr(fmodule, 'on_account_status_v2', None)
    context.on_market_data_disconnected_fun = getattr(fmodule, 'on_market_data_disconnected', None)
    context.on_trade_data_disconnected_fun = getattr(fmodule, 'on_trade_data_disconnected', None)

    context.backtest_start_time = backtest_start_time
    context.backtest_end_time = backtest_end_time
    context.adjust_mode = backtest_adjust
    py_gmi_set_data_callback(callback_controller)  # 设置事件处理的回调函数

    splash_msgs = [
        '-' * 40,
        'python sdk version: {}'.format(__version__),
        'c_sdk version: {}'.format(gmi_get_c_version()),
        '-' * 40,
    ]

    print(os.linesep.join(splash_msgs))

    # 检查是否使用相应回调函数的v2版本,如果用了, 则v1版本不会使用, 要打印出警告消息
    if _all_not_none(context.on_execution_report_fun, context.on_execution_report_fun_v2):
        gmsdklogger.warning('{0} 与 {0}_v2 都定义了, 只会调用{0}_v2'.format('on_execution_report_fun'))
    if _all_not_none(context.on_order_status_fun, context.on_order_status_fun_v2):
        gmsdklogger.warning('{0} 与 {0}_v2 都定义了, 只会调用{0}_v2'.format('on_order_status_fun'))
    if _all_not_none(context.on_backtest_finished_fun, context.on_backtest_finished_fun_v2):
        gmsdklogger.warning('{0} 与 {0}_v2 都定义了, 只会调用{0}_v2'.format('on_backtest_finished_fun'))
    if _all_not_none(context.on_parameter_fun, context.on_parameter_fun_v2):
        gmsdklogger.warning('{0} 与 {0}_v2 都定义了, 只会调用{0}_v2'.format('on_parameter_fun'))
    if _all_not_none(context.on_account_status_fun, context.on_account_status_fun_v2):
        gmsdklogger.warning('{0} 与 {0}_v2 都定义了, 只会调用{0}_v2'.format('on_account_status_fun'))

    if mode == MODE_BACKTEST:
        py_gmi_set_backtest_config(start_time=backtest_start_time,
                                   end_time=backtest_end_time,
                                   initial_cash=backtest_initial_cash,
                                   transaction_ratio=backtest_transaction_ratio,
                                   commission_ratio=backtest_commission_ratio,
                                   slippage_ratio=backtest_slippage_ratio,
                                   adjust=backtest_adjust,
                                   check_cache=backtest_check_cache
                                   )

        return py_gmi_run()

    if gmi_init():
        return

    context._set_accounts()

    while running:
        gmi_poll()


def get_parameters():
    # type: () ->List[Dict[Text, Any]]
    req = GetParametersReq()
    req.owner_id = context.strategy_id
    req = req.SerializeToString()
    status, result = py_gmi_get_parameters(req)
    if c_status_fail(status, 'py_gmi_get_parameters'):
        return []

    req = Parameters()
    req.ParseFromString(result)

    return [protobuf_to_dict(parameters) for parameters in req.parameters]


def add_parameter(key, value, min=0, max=0, name='', intro='', group='', readonly=False):
    # type: (Text, float, float, float, Text, Text, Text, bool) ->NoReturn
    req = Parameters()
    req.owner_id = context.strategy_id
    p = req.parameters.add()  # type: Parameter
    p.key = key
    p.value = value
    p.min = min
    p.max = max
    p.name = name
    p.intro = intro
    p.group = group
    p.readonly = readonly
    req = req.SerializeToString()
    py_gmi_add_parameters(req)


def set_parameter(key, value, min=0, max=0, name='', intro='', group='', readonly=False):
    # type: (Text, float, float, float, Text, Text, Text, bool) ->NoReturn
    req = Parameters()
    req.owner_id = context.strategy_id
    p = req.parameters.add()  # type: Parameter
    p.key = key
    p.value = value
    p.min = min
    p.max = max
    p.name = name
    p.intro = intro
    p.group = group
    p.readonly = readonly
    req = req.SerializeToString()
    py_gmi_set_parameters(req)


def log(level, msg, source):
    # type: (Text, Text, Text) ->NoReturn
    logs = Logs()
    item = logs.data.add()  # type: Log
    item.owner_id = context.strategy_id
    item.source = source
    item.level = level
    item.msg = msg

    req = logs.SerializeToString()
    py_gmi_log(req)


def stop():
    """
    停止策略的运行,用exit(2)退出
    """
    global running
    running = False
    sys.exit(2)


def set_serv_addr(addr):
    # type: (Text) -> NoReturn
    """
    设置终端服务地址
    """
    py_gmi_set_serv_addr(addr)
