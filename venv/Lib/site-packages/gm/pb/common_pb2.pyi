# coding=utf-8
from __future__ import unicode_literals

from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.message import Message
from google.protobuf.internal.containers import RepeatedScalarFieldContainer, RepeatedCompositeFieldContainer
from typing import Text, Dict


# noinspection PyAbstractClass
class Property(Message):
    key = ...  # type: Text
    val = ...  # type: Text
    name = ...  # type: Text
    index = ...  # type: int
    visible = ...  # type: bool

    def __init__(self,
                 key: Text = None,
                 val: Text = None,
                 name: Text = None,
                 index: int = None,
                 visible: bool = None
                 ): ...


# noinspection PyAbstractClass
class Filter(Message):
    fields = ...  # type: Text
    filter = ...  # type: Text
    sort = ...  # type: Text
    limit = ...  # type: int
    page = ...  # type: int
    pagesize = ...  # type: int
    fromdate = ...  # type: Text
    todate = ...  # type: Text

    def __init__(self, fields: Text = None, filter: Text = None, sort: Text = None, limit: int = None, page: int = None,
                 pagesize: int = None, fromdate: Text = None, todate: Text = None): ...


# noinspection PyAbstractClass
class Error(Message):
    code = ...  # type: int
    type = ...  # type: Text
    info = ...  # type: Text

    def __init__(self, code: int = None, type: Text = None, info: Text = None): ...


# noinspection PyAbstractClass
class ConnectionAddress(Message):
    title = ...  # type: Text
    address = ...  # type: Dict[Text, Text]

    def __init__(self, title: Text = None, address: Dict[Text, Text] = None): ...


# noinspection PyAbstractClass
class ConnectionStatus(Message):
    State_UNKNOWN = 0  # 未知
    State_CONNECTING = 1  # 连接中
    State_CONNECTED = 2  # 已连接
    State_LOGGEDIN = 3  # 已登录
    State_DISCONNECTING = 4  # 断开中
    State_DISCONNECTED = 5  # 已断开
    State_ERROR = 6  # 错误

    state = ...  # type: int
    error = ...  # type: Error

    def __init__(self, state: int = None, error: Error = None): ...


# noinspection PyAbstractClass
class Log(Message):
    source = ...  # type: Text
    level = ...  # type: Text
    msg = ...  # type: Text
    owner_id = ...  # type: Text
    created_at = ...  # type: Timestamp

    def __init__(self, source: Text = None, level: Text = None, msg: Text = None, owner_id: Text = None,
                 created_at: Timestamp = None): ...


# noinspection PyAbstractClass
class Logs(Message):
    data = ...  # type: RepeatedCompositeFieldContainer[Log]

    def __init__(self, data: RepeatedCompositeFieldContainer[Log] = None): ...


# noinspection PyAbstractClass
class Heartbeat(Message):
    created_at = ...  # type: Timestamp

    def __init__(self, created_at: Timestamp = None): ...
