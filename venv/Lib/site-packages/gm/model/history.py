# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import

import grpc
import pandas as pd

from gm.constant import HISTORY_ADDR
from gm.csdk.c_sdk import py_gmi_get_serv_addr
from gm.enum import ADJUST_NONE
from gm.model.storage import context
from gm.pb.history_pb2 import GetHistoryBarsReq, \
    GetHistoryTicksReq, GetHistoryBarsNReq, \
    GetHistoryTicksNReq
from gm.pb.history_pb2_grpc import HistoryServiceStub
from gm.pb_to_dict import protobuf_to_dict
from gm.utils import standard_fields

MAX_MESSAGE_LENGTH = 1024 * 1024 * 128

class HistoryApi(object):
    def __init__(self):
        self.addr = None

    def _init_addr(self):
        addr = py_gmi_get_serv_addr(HISTORY_ADDR)
        if not addr:
            raise EnvironmentError("获取不到数据服务地址")

        if not self.addr:
            self.addr = addr
            channel = grpc.insecure_channel(self.addr, options=[
                (str('grpc.max_send_message_length'), MAX_MESSAGE_LENGTH),
                (str('grpc.max_receive_message_length'), MAX_MESSAGE_LENGTH)])
            self.stub = HistoryServiceStub(channel)

    def reset_addr(self):
        self.addr = None

    def get_history_bars(self, symbols, frequency, start_time, end_time,
                         fields=None,
                         skip_suspended=True, fill_missing=None,
                         adjust=ADJUST_NONE, adjust_end_time='', df=False):
        self._init_addr()

        req = GetHistoryBarsReq(symbols=symbols, frequency=frequency,
                                start_time=start_time, end_time=end_time,
                                fields=fields, skip_suspended=skip_suspended,
                                fill_missing=fill_missing, adjust=adjust,
                                adjust_end_time=adjust_end_time)
        resp = self.stub.GetHistoryBars(req, metadata=[
            (str('authorization'), context.token),
            (str('grpc-internal-encoding-request'), str('gzip')),
            (str('sdk-lang'), context.sdk_lang),
            (str('sdk-version'), context.sdk_version),
            (str('sdk-arch'), context.sdk_arch),
            (str('sdk-os'), context.sdk_os),
        ])

        datas = [protobuf_to_dict(bar, is_utc_time=True,
                                  including_default_value_fields=True) for bar
                 in resp.data]
        fields_str, fields_list = standard_fields(fields, letter_upper=False)
        if not fields_list:
            datas = datas if not df else pd.DataFrame(datas)
            return datas

        else:
            result = []
            for data in datas:
                info = {}
                for field in fields_list:
                    info[field] = data.get(field)
                result.append(info)

            result = result if not df else pd.DataFrame(result)
            return result

    def get_history_ticks(self, symbols, start_time, end_time, fields=None,
                          skip_suspended=True, fill_missing=None,
                          adjust=ADJUST_NONE, adjust_end_time='', df=False):
        self._init_addr()

        req = GetHistoryTicksReq(symbols=symbols, start_time=start_time,
                                 end_time=end_time,
                                 fields=fields, skip_suspended=skip_suspended,
                                 fill_missing=fill_missing, adjust=adjust,
                                 adjust_end_time=adjust_end_time)
        resp = self.stub.GetHistoryTicks(req, metadata=[
            (str('authorization'), context.token),
            (str('grpc-internal-encoding-request'), str('gzip')),
            (str('sdk-lang'), context.sdk_lang),
            (str('sdk-version'), context.sdk_version),
            (str('sdk-arch'), context.sdk_arch),
            (str('sdk-os'), context.sdk_os),
        ])

        datas = [protobuf_to_dict(bar, is_utc_time=True,
                                  including_default_value_fields=True) for bar
                 in resp.data]

        fields_str, fields_list = standard_fields(fields, letter_upper=False)
        if not fields_list:
            datas = datas if not df else pd.DataFrame(datas)
            return datas

        else:
            result = []
            for data in datas:
                info = {}
                for field in fields_list:
                    info[field] = data.get(field)
                result.append(info)

            result = result if not df else pd.DataFrame(result)
            return result

    def get_history_n_bars(self, symbol, frequency, count, end_time=None,
                           fields=None, skip_suspended=None, fill_missing=None,
                           adjust=ADJUST_NONE, adjust_end_time='', df=False):
        self._init_addr()

        req = GetHistoryBarsNReq(symbol=symbol, frequency=frequency,
                                 count=count, end_time=end_time, fields=fields,
                                 skip_suspended=skip_suspended,
                                 fill_missing=fill_missing, adjust=adjust,
                                 adjust_end_time=adjust_end_time)

        resp = self.stub.GetHistoryBarsN(req, metadata=[
            (str('authorization'), context.token),
            (str('grpc-internal-encoding-request'), str('gzip')),
            (str('sdk-lang'), context.sdk_lang),
            (str('sdk-version'), context.sdk_version),
            (str('sdk-arch'), context.sdk_arch),
            (str('sdk-os'), context.sdk_os),
        ])
        datas = [protobuf_to_dict(bar, is_utc_time=True,
                                  including_default_value_fields=True) for bar
                 in resp.data]
        fields_str, fields_list = standard_fields(fields, letter_upper=False)
        if not fields_list:
            datas = datas if not df else pd.DataFrame(datas)
            return datas

        else:
            result = []
            for data in datas:
                info = {}
                for field in fields_list:
                    info[field] = data.get(field)
                result.append(info)

            result = result if not df else pd.DataFrame(result)
            return result

    def get_history_n_ticks(self, symbol, count, end_time=None, fields=None,
                            skip_suspended=None,
                            fill_missing=None, adjust=ADJUST_NONE,
                            adjust_end_time='', df=False):
        self._init_addr()

        req = GetHistoryTicksNReq(symbol=symbol, count=count, end_time=end_time,
                                  fields=fields,
                                  skip_suspended=skip_suspended,
                                  fill_missing=fill_missing, adjust=adjust,
                                  adjust_end_time=adjust_end_time)

        resp = self.stub.GetHistoryTicksN(req, metadata=[
            (str('authorization'), context.token),
            (str('grpc-internal-encoding-request'), str('gzip')),
            (str('sdk-lang'), context.sdk_lang),
            (str('sdk-version'), context.sdk_version),
            (str('sdk-arch'), context.sdk_arch),
            (str('sdk-os'), context.sdk_os),
        ])
        datas = [protobuf_to_dict(bar, is_utc_time=True,
                                  including_default_value_fields=True) for bar
                 in resp.data]
        fields_str, fields_list = standard_fields(fields, letter_upper=False)
        if not fields_list:
            datas = datas if not df else pd.DataFrame(datas)
            return datas

        else:
            result = []
            for data in datas:
                info = {}
                for field in fields_list:
                    info[field] = data.get(field)
                result.append(info)

            result = result if not df else pd.DataFrame(result)
            return result