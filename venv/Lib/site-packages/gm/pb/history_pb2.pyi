from typing import Text, Dict
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.message import Message
from google.protobuf.internal.containers import RepeatedScalarFieldContainer, RepeatedCompositeFieldContainer


# noinspection PyAbstractClass
class GetCurrentTicksReq(Message):
    symbols = ...  # type: Text
    fields = ...  # type: Text

    def __init__(self, symbols: Text, fields: Text): ...


# noinspection PyAbstractClass
class GetHistoryTicksReq(Message):
    symbols = ...  # type: Text
    start_time = ...  # type: Text
    end_time = ...  # type: Text
    fields = ...  # type: Text
    skip_suspended = ...  # type: bool
    fill_missing = ...  # type: Text
    adjust = ...  # type: int
    adjust_end_time = ...  # type: Text

    def __init__(self, symbols: Text = '', start_time: Text = '', end_time: Text = '', fields: Text = '',
                 skip_suspended: bool = None, fill_missing: Text = '', adjust: int = None,
                 adjust_end_time: Text = ''): ...


# noinspection PyAbstractClass
class GetHistoryBarsReq(Message):
    symbols = ...  # type: Text
    frequency = ...  # type: Text
    start_time = ...  # type: Text
    end_time = ...  # type: Text
    fields = ...  # type: Text
    skip_suspended = ...  # type: bool
    fill_missing = ...  # type: Text
    adjust = ...  # type: int
    adjust_end_time = ...  # type: Text

    def __init__(self, symbols: Text = '', frequency: Text = '', start_time: Text = '',
                 end_time: Text = '', fields: Text = '', skip_suspended: bool = None,
                 fill_missing: Text = '', adjust: int = None, adjust_end_time: Text = '', ): ...


# noinspection PyAbstractClass
class GetHistoryTicksNReq(Message):
    symbol = ...  # type: Text
    count = ...  # type: int
    end_time = ...  # type: Text
    fields = ...  # type: Text
    skip_suspended = ...  # type: bool
    fill_missing = ...  # type: Text
    adjust = ...  # type: int
    adjust_end_time = ...  # type: Text

    def __init__(self, symbol: Text = '', count: int = None, end_time: Text = '',
                 fields: Text = '', skip_suspended: bool = None, fill_missing: Text = '',
                 adjust: int = None, adjust_end_time: Text = None): ...


# noinspection PyAbstractClass
class GetHistoryBarsNReq(Message):
    symbol = ...  # type: Text
    frequency = ...  # type: Text
    count = ...  # type: int
    end_time = ...  # type: Text
    fields = ...  # type: Text
    skip_suspended = ...  # type: bool
    fill_missing = ...  # type: Text
    adjust = ...  # type: int
    adjust_end_time = ...  # type: Text

    def __init__(self, symbol: Text = '', frequency: Text = '', count: int = None,
                 end_time: Text = '', fields: Text = '', skip_suspended: bool = None,
                 fill_missing: Text = '', adjust: int = None, adjust_end_time: Text = '',
                 ): ...


# noinspection PyAbstractClass
class GetBenchmarkReturnReq(Message):
    symbol = ...  # type: Text
    frequency = ...  # type: Text
    start_time = ...  # type: Text
    end_time = ...  # type: Text
    adjust = ...  # type: int
    adjust_end_time = ...  # type: Text

    def __init__(self, symbol: Text = '',
                 frequency: Text = '',
                 start_time: Text = '',
                 end_time: Text = '',
                 adjust: int = None,
                 adjust_end_time: Text = '',
                 ): ...


# noinspection PyAbstractClass
class GetBenchmarkReturnRsp(Message):
    class BenchmarkReturn(Message):
        ratio = ...  # type: float
        created_at = ...  # type: Timestamp

        def __init__(self, ratio: float = None, end_date: created_at = None): ...

    data = ...  # type: RepeatedCompositeFieldContainer[GetBenchmarkReturnRsp]

    def __init__(self, data: RepeatedCompositeFieldContainer[GetBenchmarkReturnRsp] = None): ...
