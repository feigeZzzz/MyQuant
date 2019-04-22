# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import
import traceback
import grpc
import pandas as pd

from gm import utils
from gm.constant import DATA_TYPE_TICK
from gm.model.fundamental import FundamentalApi
from gm.model.history import HistoryApi
from gm.retrying import retry
from gm.utils import load_to_datetime_str, standard_fields, gmsdklogger

fundamentalapi = FundamentalApi()
historyapi = HistoryApi()

pd.set_option('precision', 4)


def reset_historyapi():
    historyapi.reset_addr()


def reset_fundamentalapi():
    fundamentalapi.reset_addr()


def condune_error(func):
    """
    网络调用尝试三次
    """

    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except grpc.RpcError as e:
            func_name = func.__name__
            details_fun = getattr(e, 'details', None)
            code_fun = getattr(e, 'code', None)
            if callable(details_fun) and callable(code_fun):
                detailsstr = details_fun()
                code = code_fun()
                if code is grpc.StatusCode.RESOURCE_EXHAUSTED and 'extract' in detailsstr:
                    exc_msg = traceback.format_exc()
                    gmsdklogger.warn("你今天的数据限额已用完,请联系商务提高数据限额.返回空数据给你. api[%s]", func_name)
                    # 这个会记录到日志文件里
                    gmsdklogger.debug("你今天的数据限额已用完,请联系商务提高数据限额.返回空数据给你. api[%s] 返回的详细信息:%s\n 执行堆栈信息:%s", func_name, e, exc_msg)
                elif 'header' in detailsstr and 'http2' in detailsstr and '429' in detailsstr:
                    exc_msg = traceback.format_exc()
                    gmsdklogger.warn("你调用api[%s]的速度太快了, 服务器对你做限流了.返回空数据给你", func_name)
                    # 这个会记录到日志文件里
                    gmsdklogger.debug("你调用api[%s]的速度太快了. 返回空数据 返回的详细信息:%s\n 执行堆栈信息:%s", func_name, e, exc_msg)
                else:
                    gmsdklogger.exception(e)

                dfval = kw.get('df', None)
                if dfval:  # df 参数为true
                    return pd.DataFrame([])
                else:
                    if func_name in {'get_previous_trading_date', 'get_next_trading_date', }:  # 这两个函数比较特殊
                        return ""
                    return []

        except Exception as e:
            func_name = func.__name__
            gmsdklogger.exception(e)
            dfval = kw.get('df', None)
            if dfval:  # df 参数为true
                return pd.DataFrame([])
            else:
                if func_name in {'get_previous_trading_date', 'get_next_trading_date', }:  # 这两个函数比较特殊
                    return ""
                return []

    return wrapper


@condune_error
@retry(pre_func=reset_fundamentalapi, stop_max_attempt_number=3)
def get_fundamentals(table, symbols, start_date, end_date, fields=None,
                     filter=None, order_by=None, limit=1000, df=False):
    """
    查询基本面财务数据
    """
    fields_str, fields_list = standard_fields(fields, letter_upper=True)
    start_date = utils.to_datestr(start_date)
    end_date = utils.to_datestr(end_date)
    data = fundamentalapi.get_fundamentals(table=table, symbols=symbols,
                                           start_date=start_date,
                                           end_date=end_date, fields=fields_str,
                                           filter=filter, order_by=order_by,
                                           limit=limit)

    if df:
        data = pd.DataFrame(data)
        if fields_list:
            fields_list = ['symbol', 'pub_date', 'end_date'] + fields_list
            columns = [field for field in fields_list if field in data.columns]
            data = data[columns]

    return data


@condune_error
@retry(pre_func=reset_fundamentalapi, stop_max_attempt_number=3)
def get_fundamentals_n(table, symbols, end_date, fields=None, filter=None,
                       order_by=None, count=1, df=False):
    """
    查询基本面财务数据,每个股票在end_date的前n条
    """
    fields_str, fields_list = standard_fields(fields, letter_upper=True)
    data = fundamentalapi.get_fundamentals_n(table=table, symbols=symbols,
                                             end_date=end_date,
                                             fields=fields_str,
                                             filter=filter, order_by=order_by,
                                             count=count)

    if df:
        data = pd.DataFrame(data)
        if fields_list:
            fields_list = ['symbol', 'pub_date', 'end_date'] + fields_list
            columns = [field for field in fields_list if field in data.columns]
            data = data[columns]

    return data


@condune_error
@retry(pre_func=reset_fundamentalapi, stop_max_attempt_number=3)
def get_instruments(symbols=None, exchanges=None, sec_types=None, names=None,
                    skip_suspended=True, skip_st=True, fields=None, df=False):
    """
    查询最新交易标的信息,有基本数据及最新日频数据
    """
    fields_str, fields_list = standard_fields(fields, letter_upper=False)
    data = fundamentalapi.get_instruments(symbols, exchanges, sec_types, names,
                                          skip_suspended, skip_st, fields_str)

    if df:
        data = pd.DataFrame(data)
        if fields_list:
            columns = [field for field in fields_list if field in data.columns]
            data = data[columns]

    return data


@condune_error
@retry(pre_func=reset_fundamentalapi, stop_max_attempt_number=3)
def get_history_instruments(symbols, fields=None, start_date=None,
                            end_date=None, df=False):
    """
    返回指定的symbols的标的日指标数据
    """
    fields_str, fields_list = standard_fields(fields, letter_upper=False)

    data = fundamentalapi.get_history_instruments(symbols, fields_str,
                                                  start_date, end_date)

    if df:
        data = pd.DataFrame(data)
        if fields_list:
            columns = [field for field in fields_list if field in data.columns]
            data = data[columns]

    return data


@condune_error
@retry(pre_func=reset_fundamentalapi, stop_max_attempt_number=3)
def get_instrumentinfos(symbols=None, exchanges=None, sec_types=None,
                        names=None, fields=None, df=False):
    """
    查询交易标的基本信息
    如果没有数据的话,返回空列表. 有的话, 返回list[dict]这样的列表. 其中 listed_date, delisted_date 为 datetime 类型
    @:param fields: 可以是 'symbol, sec_type' 这样的字符串, 也可以是 ['symbol', 'sec_type'] 这样的字符list
    """
    fields_str, fields_list = standard_fields(fields, letter_upper=False)
    data = fundamentalapi.get_instrumentinfos(symbols, exchanges, sec_types,
                                              names, fields)

    if df:
        data = pd.DataFrame(data)
        if fields_list:
            columns = [field for field in fields_list if field in data.columns]
            data = data[columns]

    return data


@condune_error
@retry(pre_func=reset_fundamentalapi, stop_max_attempt_number=3)
def get_constituents(index, fields=None, df=False):
    """
    查询指数最新成分股
    返回的list每项是个字典,包含的key值有:
    symbol 股票symbol
    weight 权重
    """
    fields_str, fields_list = standard_fields(fields, letter_upper=False)
    data = fundamentalapi.get_constituents(index, fields, df)
    if df:
        data = pd.DataFrame(data)
        if fields_list:
            columns = [field for field in fields_list if field in data.columns]
            data = data[columns]

    return data


@condune_error
@retry(pre_func=reset_fundamentalapi, stop_max_attempt_number=3)
def get_history_constituents(index, start_date=None, end_date=None):
    """
    查询指数历史成分股
    返回的list每项是个字典,包含的key值有:
    trade_date: 交易日期(datetime类型)
    constituents: 一个字典. 每个股票的sybol做为key值, weight做为value值
    """
    return fundamentalapi.get_history_constituents(index, start_date, end_date)


@condune_error
@retry(pre_func=reset_fundamentalapi, stop_max_attempt_number=3)
def get_sector(code):
    """
    查询板块股票列表
    """
    return fundamentalapi.get_sector(code)


@condune_error
@retry(pre_func=reset_fundamentalapi, stop_max_attempt_number=3)
def get_industry(code):
    """
    查询行业股票列表
    """
    return fundamentalapi.get_industry(code)


@condune_error
@retry(pre_func=reset_fundamentalapi, stop_max_attempt_number=3)
def get_concept(code):
    """
    查询概念股票列表
    """

    return fundamentalapi.get_concept(code)


@condune_error
@retry(pre_func=reset_fundamentalapi, stop_max_attempt_number=3)
def get_trading_dates(exchange, start_date, end_date):
    """
    查询交易日列表
    如果指定的市场不存在, 返回空列表. 有值的话,返回 yyyy-mm-dd 格式的列表
    """
    return fundamentalapi.get_trading_dates(exchange, start_date, end_date)


@condune_error
@retry(pre_func=reset_fundamentalapi, stop_max_attempt_number=3)
def get_previous_trading_date(exchange, date):
    """
    返回指定日期的上一个交易日
    @:param exchange: 交易市场
    @:param date: 指定日期, 可以是datetime.date 或者 datetime.datetime 类型. 或者是 yyyy-mm-dd 或 yyyymmdd 格式的字符串
    @:return 返回下一交易日, 为 yyyy-mm-dd 格式的字符串, 如果不存在则返回None
    """
    return fundamentalapi.get_previous_trading_date(exchange, date)


@condune_error
@retry(pre_func=reset_fundamentalapi, stop_max_attempt_number=3)
def get_next_trading_date(exchange, date):
    """
    返回指定日期的下一个交易日
    @:param exchange: 交易市场
    @:param date: 指定日期, 可以是datetime.date 或者 datetime.datetime 类型. 或者是 yyyy-mm-dd 或 yyyymmdd 格式的字符串
    @:return 返回下一交易日, 为 yyyy-mm-dd 格式的字符串, 如果不存在则返回None
    """
    return fundamentalapi.get_next_trading_date(exchange, date)


@condune_error
@retry(pre_func=reset_fundamentalapi, stop_max_attempt_number=3)
def get_dividend(symbol, start_date, end_date=None, df=False):
    """
    查询分红送配
    """
    data = fundamentalapi.get_dividend(symbol, start_date, end_date)

    if df:
        data = pd.DataFrame(data)

    return data


@condune_error
@retry(pre_func=reset_fundamentalapi, stop_max_attempt_number=3)
def get_continuous_contracts(csymbol, start_date=None, end_date=None):
    """
    获取连续合约
    """
    return fundamentalapi.get_continuous_contracts(csymbol, start_date,
                                                   end_date)


@condune_error
@retry(pre_func=reset_historyapi, stop_max_attempt_number=3)
def history(symbol, frequency, start_time, end_time, fields=None,
            skip_suspended=True, fill_missing=None, adjust=None,
            adjust_end_time='', df=False):
    """
    查询历史行情
    """
    start_time = load_to_datetime_str(start_time)
    end_time = load_to_datetime_str(end_time)
    adjust_end_time = load_to_datetime_str(adjust_end_time)

    if frequency == DATA_TYPE_TICK:
        return historyapi.get_history_ticks(symbols=symbol,
                                            start_time=start_time,
                                            end_time=end_time, fields=fields,
                                            skip_suspended=skip_suspended,
                                            fill_missing=fill_missing,
                                            adjust=adjust,
                                            adjust_end_time=adjust_end_time,
                                            df=df)

    else:
        return historyapi.get_history_bars(symbols=symbol, frequency=frequency,
                                           start_time=start_time,
                                           end_time=end_time, fields=fields,
                                           skip_suspended=skip_suspended,
                                           fill_missing=fill_missing,
                                           adjust=adjust,
                                           adjust_end_time=adjust_end_time,
                                           df=df)


@condune_error
@retry(pre_func=reset_historyapi, stop_max_attempt_number=3)
def history_n(symbol, frequency, count, end_time=None, fields=None,
              skip_suspended=True, fill_missing=None, adjust=None,
              adjust_end_time='', df=False):
    """
    查询历史行情
    """
    end_time = load_to_datetime_str(end_time)
    adjust_end_time = load_to_datetime_str(adjust_end_time)

    if frequency == DATA_TYPE_TICK:
        return historyapi.get_history_n_ticks(symbol=symbol, count=count,
                                              end_time=end_time, fields=fields,
                                              skip_suspended=skip_suspended,
                                              fill_missing=fill_missing,
                                              adjust=adjust,
                                              adjust_end_time=adjust_end_time,
                                              df=df)

    else:
        return historyapi.get_history_n_bars(symbol=symbol, frequency=frequency,
                                             count=count, end_time=end_time,
                                             fields=fields,
                                             skip_suspended=skip_suspended,
                                             fill_missing=fill_missing,
                                             adjust=adjust,
                                             adjust_end_time=adjust_end_time,
                                             df=df)
