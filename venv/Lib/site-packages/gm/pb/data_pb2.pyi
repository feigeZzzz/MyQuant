from typing import Text, Dict
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.message import Message
from google.protobuf.internal.containers import RepeatedScalarFieldContainer, RepeatedCompositeFieldContainer

# noinspection PyAbstractClass
class SecurityType(object):
    SecurityType_Unknown = 0  # type: int
    SecurityType_Stock   = 1  # type: int
    SecurityType_Fund    = 2  # type: int
    SecurityType_Index   = 3  # type: int
    SecurityType_Future  = 4  # type: int
    SecurityType_Option  = 5  # type: int

# noinspection PyAbstractClass
class Quote(Message):
    bid_p = ...  # type: float
    bid_v = ...  # type: int
    ask_p = ...  # type: float
    ask_v = ...  # type: int
    def __init__(self, bid_p:float=0, bid_v:int=0, ask_p:float=0, ask_v:int=0): ...

# noinspection PyAbstractClass
class OrderBook(Message):
    symbol = ... # type: Text
    quotes = ... # type: RepeatedCompositeFieldContainer[Quote]
    created_at = ... # type: Timestamp

    def __init__(self, symbol:Text=0, quotes:RepeatedCompositeFieldContainer[Quote]=None, created_at:Timestamp=None): ...

# noinspection PyAbstractClass
class OrderBooks(Message):
    data = ... # type: RepeatedCompositeFieldContainer[OrderBook]

    def __init__(self, data:RepeatedCompositeFieldContainer[OrderBook]): ...

# noinspection PyAbstractClass
class Trade(Message):
    symbol = ... # type: Text
    price = ... # type: float
    last_volume = ... # type: int
    last_amount = ... # type: float
    cum_volume = ... # type: int
    cum_amount = ... # type: float
    trade_type = ... # type: int
    created_at = ... # type: Timestamp

    def __init__(self, symbol:Text='', price:float=0, last_volume:int=0, last_amount:float=0,
                 cum_volume:int=0, cum_amount:float=0, trade_type:int=0,
                 created_at:Timestamp=None):...

# noinspection PyAbstractClass
class Trades(Message):
    data = ... # type: RepeatedCompositeFieldContainer[Trade]

    def __init__(self, data:RepeatedCompositeFieldContainer[Trade]): ...

# noinspection PyAbstractClass
class Tick(Message):
    symbol = ... # type: Text

    open = ... # type: float
    high = ... # type: float
    low = ... # type: float
    price = ... # type: float

    quotes = ... # type: RepeatedCompositeFieldContainer[Quote]

    cum_volume = ... # type: int
    cum_amount = ... # type: float
    cum_position = ... # type: int
    last_amount = ... # type: float
    last_volume = ... # type: int
    trade_type = ... # type: int

    created_at = ... # type: Timestamp

    def __init__(self, symbol:Text='', open:float=0, high:float=0, low:float=0, price:float=0,
                 quotes:RepeatedCompositeFieldContainer[Quote]=None, cum_volume:int=0, cum_amount:float=0, cum_position:int=0,
                 last_amount:float=0, last_volume:int=0, trade_type:int=0, created_at:Timestamp=None): ...

# noinspection PyAbstractClass
class Ticks(Message):
    data = ... # type: RepeatedCompositeFieldContainer[Tick]

    def __init__(self, data:RepeatedCompositeFieldContainer[Tick]): ...

# noinspection PyAbstractClass
class Bar(Message):
    symbol = ... # type: Text
    frequency = ... # type: Text

    open = ... # type: float
    high = ... # type: float
    low = ... # type: float
    close = ... # type: float
    volume = ... # type: int
    amount = ... # type: float
    position = ... # type: int
    pre_close = ... # type: float

    bob = ... # type: Timestamp
    eob = ... # type: Timestamp

    def __init__(self, symbol:Text='', frequency:int=0, open:float=0, high:float=0, low:float=0,
                 close:float=0, volume:int=0, amount:float=0, position:int=0, pre_close:float=0,
                 bob:Timestamp=None, eob:Timestamp=None): ...

# noinspection PyAbstractClass
class Bars(Message):
    data = ... # type: RepeatedCompositeFieldContainer[Bar]

    def __init__(self, data:RepeatedCompositeFieldContainer[Bar]=None): ...

# noinspection PyAbstractClass
class InstrumentInfo(Message):
    symbol = ... # type: Text
    sec_type = ... # type: int
    exchange = ... # type: Text
    sec_id = ... # type: Text
    sec_name = ... # type: Text
    sec_abbr = ... # type: Text
    price_tick = ... # type: Text

    listed_date = ... # type: Timestamp
    delisted_date = ... # type: Timestamp


    def __init__(self, symbol:Text='', sec_type:int=0, exchange:Text='', sec_id:Text='', sec_name:Text='',
                 sec_abbr: Text='', price_tick: Text='', listed_date:Timestamp=None, delisted_date:Timestamp=None): ...

# noinspection PyAbstractClass
class InstrumentInfos(Message):
    data = ... # type: RepeatedCompositeFieldContainer[InstrumentInfo]

    def __init__(self, data:RepeatedCompositeFieldContainer[InstrumentInfo]=None):...

# noinspection PyAbstractClass
class Instrument(Message):
    symbol = ... # type: Text
    sec_level = ... # type: int
    is_suspended = ... # type: int
    multiplier = ... # type: float
    margin_ratio = ... # type: float

    settle_price = ... # type: float
    position = ... # type: int
    pre_close = ... # type: float
    pre_settle = ... # type: float
    upper_limit = ... # type: float
    lower_limit = ... # type: float
    adj_factor = ... # type: float

    info = ... # type: InstrumentInfo

    created_at = ... # type: Timestamp

    def __init__(self, symbol:Text='', sec_level:int=0, is_suspended:int=0, multiplier:float=0, margin_ratio:float=0,
                 settle_price:float=0, position:int=0, pre_close:float=0, pre_settle:float=0, upper_limit:float=0, lower_limit:float=0,
                 adj_factor:float=0, info: InstrumentInfo=None, created_at:Timestamp=None): ...

# noinspection PyAbstractClass
class Instruments(Message):
    data = ... # type: RepeatedCompositeFieldContainer[Instrument]

    def __init__(self, data:RepeatedCompositeFieldContainer[Instrument]=None): ...

# noinspection PyAbstractClass
class Dividend(Message):
    symbol = ... # type: Text
    cash_div = ... # type: float
    share_div_ratio = ... # type: float
    share_trans_ratio = ... # type: float
    allotment_ratio = ... # type: float
    allotment_price = ... # type: float

    created_at = ... # type: Timestamp

    def __init__(self, symbol:Text='', cash_div:float=0, share_div_ratio:float=0, share_trans_ratio:float=0,
                 allotment_ratio:float=0, allotment_price:float=0): ...

# noinspection PyAbstractClass
class Dividends(Message):
    data = ... # type: RepeatedCompositeFieldContainer[Dividend]

    def __init__(self, data:RepeatedCompositeFieldContainer[Dividend]=None): ...

# noinspection PyAbstractClass
class ContinuousContract(Message):
    symbol = ... # type: Text
    created_at = ... # type: Timestamp

    def __init__(self, symbol:Text='', created_at:Timestamp=None): ...

# noinspection PyAbstractClass
class ContinuousContracts(Message):
    data = ... # type: RepeatedCompositeFieldContainer[ContinuousContract]

    def __init__(self, data=RepeatedCompositeFieldContainer[ContinuousContract]): ...

# noinspection PyAbstractClass
class Constituent(Message):
    constituents = ... # type: Dict[Text, float]
    created_at = ... # type: Timestamp

    def __init__(self, constituents:Dict[Text, float], created_at:Timestamp): ...

# noinspection PyAbstractClass
class Constituents(Message):
    data = ... # type: RepeatedCompositeFieldContainer[Constituent]

    def __init__(self, data:RepeatedCompositeFieldContainer[Constituent]=None): ...
