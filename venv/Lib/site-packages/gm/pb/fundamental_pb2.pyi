from typing import Text, Dict
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.message import Message
from google.protobuf.internal.containers import RepeatedScalarFieldContainer, RepeatedCompositeFieldContainer

# noinspection PyAbstractClass
class GetFundamentalsReq(Message):
    table = ...  # type: Text
    fields = ... # type: Text
    filter = ... # type: Text
    symbols = ... # type: Text
    start_date = ... # type: Text
    end_date = ... # type: Text
    order_by = ... # type: Text
    limit = ... # type: int

    def __init__(self, table:Text, symbols:Text, end_date:Text, start_date:Text='', fields:Text='',  filter:Text='', order_by:Text='', limit:int=None): ...


# noinspection PyAbstractClass
class GetFundamentalsNReq(Message):
    table = ...  # type: Text
    fields = ... # type: Text
    filter = ... # type: Text
    symbols = ... # type: Text
    end_date = ... # type: Text
    order_by = ... # type: Text
    count = ... # type: int

    def __init__(self, table:Text, symbols:Text, end_date:Text, count:int, fields:Text='', filter:Text='', order_by:Text=''): ...

# noinspection PyAbstractClass
class GetFundamentalsRsp(Message):
    class Fundamental(Message):
        symbol = ... # type: Text
        fields = ... # type: Dict[Text, float]
        pub_date = ... # type: Timestamp
        end_date = ... # type: Timestamp

        def __init__(self, symbol:Text='', fields:Dict[Text, float]=None, pub_date:Timestamp=None, end_date:Timestamp=None): ...

    data = ... # type: RepeatedCompositeFieldContainer[Fundamental]
    def __init__(self, data: RepeatedCompositeFieldContainer[Fundamental]=None):...


# noinspection PyAbstractClass
class GetInstrumentInfosReq(Message):
    symbols = ... # type: Text
    exchanges = ... # type: Text
    sec_types = ... # type: Text
    names = ... # type: Text
    fields = ... # type: Text

    def __init__(self, symbols:Text='', exchanges:Text='', sec_types:Text='', names:Text='', fields:Text=''): ...

# noinspection PyAbstractClass
class GetInstrumentsReq(Message):
    symbols = ... # type:Text
    exchanges = ... # type:Text
    sec_types = ... # type:Text
    names = ... # type:Text
    skip_suspended = ...  # type: bool
    skip_st = ...  # type: bool
    fields = ...  # type: Text

    def __init__(self, symbols:Text='', exchanges:Text='', sec_types:Text='', names:Text='', skip_suspended:bool=False,
                 skip_st:bool=False, fields:Text=''): ...

# noinspection PyAbstractClass
class GetHistoryInstrumentsReq(Message):
    symbols = ... # type: Text
    fields = ... # type: Text
    start_date = ... # type: Text
    end_date = ... # type: Text

    def __init__(self, symbols:Text='', fields:Text='', start_date:Text='', end_date:Text=''):...

# noinspection PyAbstractClass
class GetConstituentsReq(Message):
    index = ...  # type: Text
    fields = ...  # type: Text
    start_date = ...  # type: Text
    end_date = ...  # type: Text

    def __init__(self, index:Text='', fields:Text='', start_date:Text='', end_date:Text=''): ...

# noinspection PyAbstractClass
class GetSectorReq(Message):
    code = ...  # type: Text
    def __init__(self, code:Text=''): ...

# noinspection PyAbstractClass
class GetSectorRsp(Message):
    symbols = ... # type: RepeatedScalarFieldContainer[Text]
    def __init__(self, symbols:RepeatedScalarFieldContainer[Text]=None): ...

# noinspection PyAbstractClass
class GetIndustryReq(Message):
    code = ...  # type: Text
    def __init__(self, code:Text=''): ...

# noinspection PyAbstractClass
class GetIndustryRsp(Message):
    symbols = ... # type: RepeatedScalarFieldContainer[Text]
    def __init__(self, symbols:RepeatedScalarFieldContainer[Text]=None): ...

# noinspection PyAbstractClass
class GetConceptReq(Message):
    code = ...  # type: Text
    def __init__(self, code:Text=''): ...

# noinspection PyAbstractClass
class GetConceptRsp(Message):
    symbols = ... # type: RepeatedScalarFieldContainer[Text]
    def __init__(self, symbols:RepeatedScalarFieldContainer[Text]=None): ...

# noinspection PyAbstractClass
class GetTradingDatesReq(Message):
    exchange = ...  # type: Text
    start_date = ...  # type: Text
    end_date = ...  # type: Text
    def __init__(self, exchange:Text='', start_date:Text='', end_date:Text=''): ...

# noinspection PyAbstractClass
class GetTradingDatesRsp(Message):
    dates = ... # type: RepeatedCompositeFieldContainer[Timestamp]
    def __init__(self, dates:RepeatedCompositeFieldContainer[Timestamp]=None): ...

# noinspection PyAbstractClass
class GetPreviousTradingDateReq(Message):
    exchange = ...  # type: Text
    date = ...  # type: Text
    def __init__(self, exchange:Text='', date:Text=''): ...

# noinspection PyAbstractClass
class GetPreviousTradingDateRsp(Message):
    date = ... # type: Timestamp
    def __init__(self, date:Timestamp=None): ...

# noinspection PyAbstractClass
class GetNextTradingDateReq(Message):
    exchange = ...  # type: Text
    date = ...  # type: Text
    def __init__(self, exchange:Text='', date:Text=''): ...

# noinspection PyAbstractClass
class GetNextTradingDateRsp(Message):
    date = ... # type: Timestamp
    def __init__(self, date:Timestamp=None): ...

# noinspection PyAbstractClass
class GetDividendsReq(Message):
    symbol = ...  # type: Text
    start_date = ...  # type: Text
    end_date = ...  # type: Text
    def __init__(self, symbol:Text='', start_date:Text='', end_date:Text=''): ...

# noinspection PyAbstractClass
class GetDividendsSnapshotReq(Message):
    symbols = ...  # type: RepeatedCompositeFieldContainer[Text]
    date = ...  # type: Text
    def __init__(self, symbols:RepeatedCompositeFieldContainer[Text]=None, date:Text=''): ...

# noinspection PyAbstractClass
class GetContinuousContractsReq(Message):
    csymbol = ... # type: Text
    start_date = ... # type: Text
    end_date = ... # type: Text

    def __init__(self, csymbol:Text='', start_date:Text='', end_date:Text=''):...
