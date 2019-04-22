from typing import Text, Dict
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.duration_pb2 import Duration
from google.protobuf.message import Message
from google.protobuf.internal.containers import RepeatedScalarFieldContainer, RepeatedCompositeFieldContainer

from gm.pb.account_pb2 import Position


# noinspection PyAbstractClass
class Indicator(Message):
    # 账号ID
    account_id = ...  # type: Text
    # 累计收益率(pnl/cum_inout)
    pnl_ratio = ...  # type: float
    # 年化收益率
    pnl_ratio_annual = ...  # type: float
    # 夏普比率
    sharp_ratio = ...  # type: float
    # 最大回撤
    max_drawdown = ...  # type: float
    # 风险比率
    risk_ratio = ...  # type: float
    # 开仓次数
    open_count = ...  # type: int
    # 平仓次数
    close_count = ...  # type: int
    # 盈利次数
    win_count = ...  # type: int
    # 亏损次数
    lose_count = ...  # type: int
    # 胜率
    win_ratio = ...  # type: float
    # 卡玛比率
    calmar_ratio = ...  # type: float
    created_at = ...  # type: Timestamp
    updated_at = ...  # type: Timestamp

    def __init__(self,
                 account_id: Text = '',
                 pnl_ratio: float = None,
                 pnl_ratio_annual: float = None,
                 sharp_ratio: float = None,
                 max_drawdown: float = None,
                 risk_ratio: float = None,
                 open_count: int = None,
                 close_count: int = None,
                 win_count: int = None,
                 lose_count: int = None,
                 win_ratio: float = None,
                 calmar_ratio: float = None,
                 created_at: Timestamp = None,
                 updated_at: Timestamp = None
                 ): ...


# noinspection PyAbstractClass
class Indicators(Message):
    data = ...  # type: RepeatedCompositeFieldContainer[Indicator]

    def __init__(self, data: RepeatedCompositeFieldContainer[Indicator] = None): ...


# noinspection PyAbstractClass
class IndicatorDuration(Message):
    # 账号ID
    account_id = ...  # type: Text
    pnl_ratio = ...  # type: float
    pnl = ...  # type: float
    fpnl = ...  # type: float
    frozen = ...  # type: float
    cash = ...  # type: float
    nav = ...  # type: float
    positions = ...  # type: RepeatedCompositeFieldContainer[Position]
    # 周期累计盈亏
    cum_pnl = ...  # type: float
    # 周期累计买入额
    cum_buy = ...  # type: float
    # 周期累计卖出额
    cum_sell = ...  # type: float
    # 周期累计手续费
    cum_commission = ...  # type: float
    duration = ...  # type: Duration
    created_at = ...  # type: Timestamp
    updated_at = ...  # type: Timestamp

    def __init__(self,
                 account_id: Text = None,
                 pnl_ratio: float = None,
                 pnl: float = None,
                 fpnl: float = None,
                 frozen: float = None,
                 cash: float = None,
                 nav: float = None,
                 positions: RepeatedCompositeFieldContainer[Position] = None,
                 cum_pnl: float = None,
                 cum_buy: float = None,
                 cum_sell: float = None,
                 cum_commission: float = None,
                 duration: Duration = None,
                 created_at: Timestamp = None,
                 updated_at: Timestamp = None
                 ): ...


# noinspection PyAbstractClass
class IndicatorDurations(Message):
    data = ...  # type: RepeatedCompositeFieldContainer[IndicatorDuration]

    def __init__(self, data: RepeatedCompositeFieldContainer[IndicatorDuration] = None): ...
