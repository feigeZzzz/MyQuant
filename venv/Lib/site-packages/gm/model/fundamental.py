# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import

from datetime import date as Date, datetime as Datetime

import grpc
import six
from google.protobuf.timestamp_pb2 import Timestamp
from six import string_types
from typing import List, Dict, Text, Any, Union

from gm import utils
from gm.constant import FUNDAMENTAL_ADDR
from gm.csdk.c_sdk import py_gmi_get_serv_addr
from gm.model.storage import context
from gm.pb.data_pb2 import Instrument, InstrumentInfo, ContinuousContract, Dividend
from gm.pb.fundamental_pb2_grpc import FundamentalServiceStub
from gm.pb.fundamental_pb2 import GetFundamentalsReq, GetInstrumentsReq, GetHistoryInstrumentsReq, \
    GetInstrumentInfosReq, GetConstituentsReq, GetIndustryReq, GetConceptReq, GetTradingDatesReq, \
    GetPreviousTradingDateReq, GetNextTradingDateReq, GetDividendsReq, \
    GetContinuousContractsReq, GetFundamentalsRsp, GetFundamentalsNReq
from gm.pb_to_dict import protobuf_to_dict
from gm.utils import str_lowerstrip, load_to_list

GmDate = Union[Text, Datetime, Date]  # 自定义gm里可表示时间的类型
TextNone = Union[Text, None]  # 可表示str或者None类型

MAX_MESSAGE_LENGTH = 1024 * 1024 * 128


def get_sec_type_str(sec_types):
    """把int类型的sectype转为字符串的sectype, 不能转换则返回None"""
    d = {
        1: 'stock',
        2: 'fund',
        3: 'index',
        4: 'future',
        5: 'option',
        10: 'confuture',
        '1': 'stock',
        '2': 'fund',
        '3': 'index',
        '4': 'future',
        '5': 'option',
        '10': 'confuture',
        'stock': 'stock',
        'fund': 'fund',
        'index': 'index',
        'future': 'future',
        'option': 'option',
        'confuture': 'confuture',
    }
    result = []
    for sec_type in sec_types:
        if isinstance(sec_type, six.string_types):
            sec_type = sec_type.strip().lower()
        if sec_type in d:
            result.append(d.get(sec_type))

    return result


class FundamentalApi(object):
    def __init__(self):
        self.addr = None

    def _init_addr(self):
        new_addr = py_gmi_get_serv_addr(FUNDAMENTAL_ADDR)
        if not new_addr:
            raise EnvironmentError("获取不到基本面服务地址")

        if not self.addr:
            self.addr = new_addr
            channel = grpc.insecure_channel(self.addr,
                                            options=[('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
                                                     ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)])
            self.stub = FundamentalServiceStub(channel)

    def reset_addr(self):
        self.addr = None

    def get_fundamentals(self, table, symbols, start_date, end_date, fields=None, filter=None, order_by=None,
                         limit=1000):
        """
        查询基本面财务数据
        """
        self._init_addr()

        if isinstance(symbols, string_types):
            symbols = [s.strip() for s in symbols.split(',') if s.strip()]
        if not symbols:
            symbols = []

        req = GetFundamentalsReq(table=table, start_date=start_date, end_date=end_date,
                                 fields=fields, symbols=','.join(symbols), filter=filter,
                                 order_by=order_by, limit=limit)
        resp = self.stub.GetFundamentals(req, metadata=[
            (str('authorization'), context.token),
            (str('sdk-lang'), context.sdk_lang),
            (str('sdk-version'), context.sdk_version),
            (str('sdk-arch'), context.sdk_arch),
            (str('sdk-os'), context.sdk_os),
        ])

        result = []
        for item in resp.data:  # type: GetFundamentalsRsp.Fundamental
            r = {
                'symbol': item.symbol,
                'pub_date': utils.utc_datetime2beijing_datetime(item.pub_date.ToDatetime()),
                'end_date': utils.utc_datetime2beijing_datetime(item.end_date.ToDatetime()),
            }
            r.update(item.fields)
            result.append(r)

        return result

    def get_instruments(self, symbols=None, exchanges=None, sec_types=None, names=None, skip_suspended=True,
                        skip_st=True, fields=None):
        """
        查询最新交易标的信息,有基本数据及最新日频数据
        """
        self._init_addr()
        # todo 这里代码限定的太死了, 后面优化一下
        instrument_fields = {
            'symbol', 'sec_level', 'is_suspended', 'multiplier', 'margin_ratio',
            'settle_price',
            'position', 'pre_close', 'upper_limit', 'lower_limit', 'adj_factor',
            'created_at', 'trade_date'
        }

        info_fields = {
            'sec_type', 'exchange', 'sec_id', 'sec_name', 'sec_abbr',
            'price_tick',
            'listed_date', 'delisted_date'
        }

        all_fields = instrument_fields.union(info_fields)

        if isinstance(symbols, string_types):
            symbols = [s for s in map(str_lowerstrip, symbols.split(',')) if s]
        if not symbols:
            symbols = []

        if isinstance(exchanges, string_types):
            exchanges = [utils.to_exchange(s) for s in exchanges.split(',') if utils.to_exchange(s)]
        if not exchanges:
            exchanges = []

        if isinstance(sec_types, six.string_types):
            sec_types = [it.strip() for it in sec_types.split(',') if it.strip()]

        if isinstance(sec_types, int):
            sec_types = [sec_types]

        if isinstance(sec_types, list):
            sec_types = get_sec_type_str(sec_types)

        if not sec_types:
            sec_types = []

        if isinstance(names, string_types):
            names = [s for s in names.split(',') if s]
        if not names:
            names = []

        if not fields:
            filter_fields = all_fields
        elif isinstance(fields, string_types):
            filter_fields = {f for f in map(str_lowerstrip, fields.split(','))
                             if f in all_fields}
        else:
            filter_fields = {f for f in map(str_lowerstrip, fields) if
                             f in all_fields}

        if 'trade_date' in filter_fields:
            filter_fields.add('created_at')

        if not filter_fields:
            return []

        req = GetInstrumentsReq(symbols=','.join(symbols),
                                exchanges=','.join(exchanges),
                                sec_types=','.join(sec_types),
                                names=','.join(names), skip_st=skip_st,
                                skip_suspended=skip_suspended,
                                fields=','.join(filter_fields))
        resp = self.stub.GetInstruments(req, metadata=[
            (str('authorization'), context.token),
            (str('sdk-lang'), context.sdk_lang),
            (str('sdk-version'), context.sdk_version),
            (str('sdk-arch'), context.sdk_arch),
            (str('sdk-os'), context.sdk_os),
        ])
        result = []
        instrument_copy_field = filter_fields & instrument_fields
        info_copy_field = filter_fields & info_fields
        for ins in resp.data:  # type: Instrument
            row = dict()
            utils.protomessage2dict(ins, row, *instrument_copy_field)

            created_at_val = row.get('created_at', None)
            if isinstance(created_at_val, Datetime):
                row['trade_date'] = utils.utc_datetime2beijing_datetime(created_at_val)
                row.pop('created_at')
            utils.protomessage2dict(ins.info, row, *info_copy_field)

            listed_date_val = row.get('listed_date', None)
            if isinstance(listed_date_val, Datetime):
                row['listed_date'] = utils.utc_datetime2beijing_datetime(listed_date_val)

            delisted_date_val = row.get('delisted_date', None)
            if isinstance(delisted_date_val, Datetime):
                row['delisted_date'] = utils.utc_datetime2beijing_datetime(delisted_date_val)

            result.append(row)
        return result

    def get_history_instruments(self, symbols, fields=None, start_date=None, end_date=None):
        """
        返回指定的symbols的标的日指标数据
        """
        self._init_addr()
        symbols = load_to_list(symbols)
        start_date = utils.to_datestr(start_date)
        end_date = utils.to_datestr(end_date)

        if not start_date:
            start_date = ''
        if not end_date:
            end_date = ''

        req = GetHistoryInstrumentsReq(symbols=','.join(symbols),
                                       fields=fields,
                                       start_date=start_date, end_date=end_date)
        resp = self.stub.GetHistoryInstruments(req, metadata=[
            (str('authorization'), context.token),
            (str('sdk-lang'), context.sdk_lang),
            (str('sdk-version'), context.sdk_version),
            (str('sdk-arch'), context.sdk_arch),
            (str('sdk-os'), context.sdk_os),
        ])
        result = [protobuf_to_dict(res_order, including_default_value_fields=True) for res_order in resp.data]
        for info in result:
            created_at_val = info.get('created_at', None)
            if isinstance(created_at_val, Datetime):
                info['trade_date'] = utils.utc_datetime2beijing_datetime(created_at_val)
                info.pop('created_at')
        return result

    def get_instrumentinfos(self, symbols=None, exchanges=None, sec_types=None, names=None, fields=None):
        """
        查询交易标的基本信息
        如果没有数据的话,返回空列表. 有的话, 返回list[dict]这样的列表. 其中 listed_date, delisted_date 为 datetime 类型
        @:param fields: 可以是 'symbol, sec_type' 这样的字符串, 也可以是 ['symbol', 'sec_type'] 这样的字符list
        """
        self._init_addr()

        if isinstance(symbols, string_types):
            symbols = [s for s in symbols.split(',') if s]
        if not symbols:
            symbols = []

        all_fields = {
            'symbol', 'sec_type', 'exchange', 'sec_id', 'sec_name', 'sec_abbr', 'price_tick', 'listed_date',
            'delisted_date'
        }

        if not fields:
            filter_fields = all_fields
        elif isinstance(fields, string_types):
            filter_fields = {f for f in map(str_lowerstrip, fields.split(',')) if f in all_fields}
        else:
            filter_fields = [f for f in map(str_lowerstrip, fields) if f in all_fields]

        if not filter_fields:
            return []

        if isinstance(exchanges, string_types):
            exchanges = [utils.to_exchange(s) for s in exchanges.split(',') if utils.to_exchange(s)]
        if not exchanges:
            exchanges = []

        if isinstance(sec_types, six.string_types):
            sec_types = [it.strip() for it in sec_types.split(',') if it.strip()]

        if isinstance(sec_types, int):
            sec_types = [sec_types]

        if isinstance(sec_types, list):
            sec_types = get_sec_type_str(sec_types)

        if not sec_types:
            sec_types = []

        if isinstance(names, string_types):
            names = [s for s in names.split(',') if s]
        if not names:
            names = []

        req = GetInstrumentInfosReq(symbols=','.join(symbols), exchanges=','.join(exchanges),
                                    sec_types=','.join(sec_types), names=','.join(names),
                                    fields=','.join(filter_fields))
        resp = self.stub.GetInstrumentInfos(req, metadata=[
            (str('authorization'), context.token),
            (str('sdk-lang'), context.sdk_lang),
            (str('sdk-version'), context.sdk_version),
            (str('sdk-arch'), context.sdk_arch),
            (str('sdk-os'), context.sdk_os),
        ])
        result = []
        for ins in resp.data:  # type: InstrumentInfo
            row = dict()
            utils.protomessage2dict(ins, row, *filter_fields)
            listed_date_val = row.get('listed_date', None)
            if isinstance(listed_date_val, Datetime):
                row['listed_date'] = utils.utc_datetime2beijing_datetime(listed_date_val)

            delisted_date_val = row.get('delisted_date', None)
            if isinstance(delisted_date_val, Datetime):
                row['delisted_date'] = utils.utc_datetime2beijing_datetime(delisted_date_val)

            result.append(row)

        return result

    def get_history_constituents(self, index, start_date=None, end_date=None):
        # type: (TextNone, GmDate, GmDate) -> List[Dict[Text, Any]]
        """
        查询指数历史成分股
        返回的list每项是个字典,包含的key值有:
        trade_date: 交易日期(datetime类型)
        constituents: 一个字典. 每个股票的sybol做为key值, weight做为value值
        """
        self._init_addr()

        start_date = utils.to_datestr(start_date)
        end_date = utils.to_datestr(end_date)

        if not start_date:
            start_date = Date.today()
        else:
            start_date = Datetime.strptime(start_date, '%Y-%m-%d').date()

        if not end_date:
            end_date = Date.today()
        else:
            end_date = Datetime.strptime(end_date, '%Y-%m-%d').date()

        req = GetConstituentsReq(index=index, start_date=start_date.strftime('%Y-%m-%d'),
                                 end_date=end_date.strftime('%Y-%m-%d'))
        resp = self.stub.GetConstituents(req, metadata=[
            (str('authorization'), context.token),
            (str('sdk-lang'), context.sdk_lang),
            (str('sdk-version'), context.sdk_version),
            (str('sdk-arch'), context.sdk_arch),
            (str('sdk-os'), context.sdk_os),
        ])

        return [
            {'trade_date': utils.utc_datetime2beijing_datetime(item.created_at.ToDatetime()),
             'constituents': dict(item.constituents)}
            for item in resp.data
        ]

    def get_constituents(self, index, fields=None, df=False):
        """
        查询指数最新成分股. 指定 fields = 'symbol, weight'
        返回的list每项是个字典,包含的key值有:
        symbol 股票symbol
        weight 权重

        如果不指定 fields, 则返回的list每项是symbol字符串
        """
        self._init_addr()

        all_fields = ['symbol', 'weight']
        if not fields:
            filter_fields = {'symbol'}
        elif isinstance(fields, string_types):
            filter_fields = {f for f in map(str_lowerstrip, fields.split(',')) if f in all_fields}
        else:
            filter_fields = {f for f in map(str_lowerstrip, fields) if f in all_fields}

        req = GetConstituentsReq(index=index, start_date='', end_date='')
        resp = self.stub.GetConstituents(req, metadata=[
            (str('authorization'), context.token),
            (str('sdk-lang'), context.sdk_lang),
            (str('sdk-version'), context.sdk_version),
            (str('sdk-arch'), context.sdk_arch),
            (str('sdk-os'), context.sdk_os),
        ])
        if len(resp.data) > 0:
            filter_fields = list(filter_fields)
            if len(filter_fields) == 1 and filter_fields[0] == 'symbol':
                if not df:
                    return [k for k, v in resp.data[0].constituents.items()]
                else:
                    return [{'symbol': k} for k, v in resp.data[0].constituents.items()]
            else:
                return [{'symbol': k, 'weight': v} for k, v in resp.data[0].constituents.items()]
        else:
            return []

    def get_sector(self, code):
        """
        查询板块股票列表
        """
        # TODO 没有数据, 先不实现
        self._init_addr()

        return []

    def get_industry(self, code):
        """
        查询行业股票列表
        """
        self._init_addr()

        if not code:
            return []
        req = GetIndustryReq(code=code)
        resp = self.stub.GetIndustry(req, metadata=[
            (str('authorization'), context.token),
            (str('sdk-lang'), context.sdk_lang),
            (str('sdk-version'), context.sdk_version),
            (str('sdk-arch'), context.sdk_arch),
            (str('sdk-os'), context.sdk_os),
        ])
        return [r for r in resp.symbols]

    def get_concept(self, code):
        """
        查询概念股票列表
        """
        self._init_addr()

        if not code:
            return []
        req = GetConceptReq(code=code)
        resp = self.stub.GetConcept(req, metadata=[
            (str('authorization'), context.token),
            (str('sdk-lang'), context.sdk_lang),
            (str('sdk-version'), context.sdk_version),
            (str('sdk-arch'), context.sdk_arch),
            (str('sdk-os'), context.sdk_os),
        ])
        ds = [r for r in resp.symbols]
        return ds

    def get_trading_dates(self, exchange, start_date, end_date):
        # type: (Text, GmDate, GmDate) -> List[Text]
        """
        查询交易日列表
        如果指定的市场不存在, 返回空列表. 有值的话,返回 yyyy-mm-dd 格式的列表
        """
        self._init_addr()

        exchange = utils.to_exchange(exchange)
        sdate = utils.to_datestr(start_date)
        edate = utils.to_datestr(end_date)
        if not exchange:
            return []
        if not sdate:
            return []
        if not end_date:
            edate = Datetime.now().strftime('%Y-%m-%d')
        req = GetTradingDatesReq(exchange=exchange, start_date=sdate, end_date=edate)
        resp = self.stub.GetTradingDates(req, metadata=[
            (str('authorization'), context.token),
            (str('sdk-lang'), context.sdk_lang),
            (str('sdk-version'), context.sdk_version),
            (str('sdk-arch'), context.sdk_arch),
            (str('sdk-os'), context.sdk_os),
        ])

        if len(resp.dates) == 0:
            return []
        ds = []
        for t in resp.dates:  # type: Timestamp
            ds.append(utils.utc_datetime2beijing_datetime(t.ToDatetime()).strftime('%Y-%m-%d'))

        return ds

    def get_previous_trading_date(self, exchange, date):
        # type: (Text, GmDate) -> TextNone
        """
        返回指定日期的上一个交易日
        @:param exchange: 交易市场
        @:param date: 指定日期, 可以是datetime.date 或者 datetime.datetime 类型. 或者是 yyyy-mm-dd 或 yyyymmdd 格式的字符串
        @:return 返回下一交易日, 为 yyyy-mm-dd 格式的字符串, 如果不存在则返回None
        """
        self._init_addr()

        exchange = utils.to_exchange(exchange)
        date_str = utils.to_datestr(date)
        if not exchange or not date_str:
            return None

        req = GetPreviousTradingDateReq(exchange=exchange, date=date_str)
        resp = self.stub.GetPreviousTradingDate(req, metadata=[
            (str('authorization'), context.token),
            (str('sdk-lang'), context.sdk_lang),
            (str('sdk-version'), context.sdk_version),
            (str('sdk-arch'), context.sdk_arch),
            (str('sdk-os'), context.sdk_os),
        ])
        rdate = resp.date  # type: Timestamp
        if not rdate.ListFields():  # 这个说明查询结果没有
            return None
        return utils.utc_datetime2beijing_datetime(rdate.ToDatetime()).strftime('%Y-%m-%d')

    def get_next_trading_date(self, exchange, date):
        # type: (Text, GmDate) -> TextNone
        """
        返回指定日期的下一个交易日
        @:param exchange: 交易市场
        @:param date: 指定日期, 可以是datetime.date 或者 datetime.datetime 类型. 或者是 yyyy-mm-dd 或 yyyymmdd 格式的字符串
        @:return 返回下一交易日, 为 yyyy-mm-dd 格式的字符串, 如果不存在则返回None
        """
        self._init_addr()

        exchange = utils.to_exchange(exchange)
        date_str = utils.to_datestr(date)
        if not date_str or not exchange:
            return None

        req = GetNextTradingDateReq(exchange=exchange, date=date_str)
        resp = self.stub.GetNextTradingDate(req, metadata=[
            (str('authorization'), context.token),
            (str('sdk-lang'), context.sdk_lang),
            (str('sdk-version'), context.sdk_version),
            (str('sdk-arch'), context.sdk_arch),
            (str('sdk-os'), context.sdk_os),
        ])
        rdate = resp.date  # type: Timestamp
        if not rdate.ListFields():  # 这个说明查询结果没有
            return None
        return utils.utc_datetime2beijing_datetime(rdate.ToDatetime()).strftime('%Y-%m-%d')

    def get_dividend(self, symbol, start_date, end_date=None):
        # type: (Text, GmDate, GmDate) -> List[Dict[Text, Any]]
        """
        查询分红送配
        """
        self._init_addr()

        if not symbol or not start_date:
            return []
        sym_tmp = symbol.split('.')  # List[Text]
        sym_tmp[0] = sym_tmp[0].upper()
        symbol = '.'.join(sym_tmp)

        if not end_date:
            end_date = Datetime.now().strftime('%Y-%m-%d')
        start_date = utils.to_datestr(start_date)
        end_date = utils.to_datestr(end_date)

        req = GetDividendsReq(symbol=symbol, start_date=start_date, end_date=end_date)
        resp = self.stub.GetDividends(req, metadata=[
            (str('authorization'), context.token),
            (str('sdk-lang'), context.sdk_lang),
            (str('sdk-version'), context.sdk_version),
            (str('sdk-arch'), context.sdk_arch),
            (str('sdk-os'), context.sdk_os),
        ])
        result = []
        fields = ['symbol', 'cash_div', 'share_div_ratio', 'share_trans_ratio', 'allotment_ratio', 'allotment_price',
                  'created_at']
        for divi in resp.data:  # type: Dividend
            row = dict()
            utils.protomessage2dict(divi, row, *fields)
            created_at_val = row.get('created_at', None)
            if isinstance(created_at_val, Datetime):
                row['created_at'] = utils.utc_datetime2beijing_datetime(created_at_val)
            result.append(row)
        return result

    def get_continuous_contracts(self, csymbol, start_date=None, end_date=None):
        # type: (Text, GmDate, GmDate) -> List[Dict[Text, Any]]

        self._init_addr()

        start_date = utils.to_datestr(start_date)
        end_date = utils.to_datestr(end_date)

        req = GetContinuousContractsReq(csymbol=csymbol, start_date=start_date, end_date=end_date)
        resp = self.stub.GetContinuousContracts(req, metadata=[
            (str('authorization'), context.token),
            (str('sdk-lang'), context.sdk_lang),
            (str('sdk-version'), context.sdk_version),
            (str('sdk-arch'), context.sdk_arch),
            (str('sdk-os'), context.sdk_os),
        ])

        result = []
        for cc in resp.data:  # type: ContinuousContract
            row = {'symbol': cc.symbol, 'trade_date': utils.utc_datetime2beijing_datetime(cc.created_at.ToDatetime())}
            result.append(row)
        return result

    def get_fundamentals_n(self, table, symbols, end_date, fields=None, filter=None, order_by=None, count=1):
        """
        查询基本面财务数据,每个股票在end_date的前n条
        """
        self._init_addr()

        end_date = utils.to_datestr(end_date)

        if isinstance(symbols, string_types):
            symbols = [s.strip() for s in symbols.split(',') if s.strip()]

        req = GetFundamentalsNReq(table=table, end_date=end_date, fields=fields,
                                  symbols=','.join(symbols), filter=filter,
                                  order_by=order_by, count=count)

        resp = self.stub.GetFundamentalsN(req, metadata=[
            (str('authorization'), context.token),
            (str('sdk-lang'), context.sdk_lang),
            (str('sdk-version'), context.sdk_version),
            (str('sdk-arch'), context.sdk_arch),
            (str('sdk-os'), context.sdk_os),
        ])
        result = []
        for item in resp.data:  # type: GetFundamentalsRsp.Fundamental
            r = {
                'symbol': item.symbol,
                'pub_date': utils.utc_datetime2beijing_datetime(item.pub_date.ToDatetime()),
                'end_date': utils.utc_datetime2beijing_datetime(item.end_date.ToDatetime()),
            }
            r.update(item.fields)
            result.append(r)

        return result
