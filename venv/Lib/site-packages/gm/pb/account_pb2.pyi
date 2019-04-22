# coding=utf-8
from google.protobuf.internal.containers import RepeatedCompositeFieldContainer
from google.protobuf.internal.containers import RepeatedScalarFieldContainer
from google.protobuf.message import Message
from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper
from typing import Text, Dict

from google.protobuf.timestamp_pb2 import Timestamp

from gm.pb.common_pb2 import ConnectionStatus, ConnectionAddress

ExecType_Unknown = 0
ExecType_New = 1                      #已报
ExecType_DoneForDay = 4               #
ExecType_Canceled = 5                 #已撤销
ExecType_PendingCancel = 6            #待撤销
ExecType_Stopped = 7                  #
ExecType_Rejected = 8                 #已拒绝
ExecType_Suspended = 9                #挂起
ExecType_PendingNew = 10              #待报
ExecType_Calculated = 11              #
ExecType_Expired = 12                 #过期
ExecType_Restated = 13                #
ExecType_PendingReplace = 14          #
ExecType_Trade = 15                   #成交
ExecType_TradeCorrect = 16            #
ExecType_TradeCancel = 17             #
ExecType_OrderStatus = 18             #委托状态
ExecType_CancelRejected = 19          #撤单被拒绝


OrderStatus_Unknown = 0
OrderStatus_New = 1                   #已报
OrderStatus_PartiallyFilled = 2       #部成
OrderStatus_Filled = 3                #已成
OrderStatus_DoneForDay = 4            #
OrderStatus_Canceled = 5              #已撤
OrderStatus_PendingCancel = 6         #待撤
OrderStatus_Stopped = 7               #
OrderStatus_Rejected = 8              #已拒绝
OrderStatus_Suspended = 9             #挂起
OrderStatus_PendingNew = 10           #待报
OrderStatus_Calculated = 11           #
OrderStatus_Expired = 12              #已过期
OrderStatus_AcceptedForBidding = 13   #
OrderStatus_PendingReplace = 14       #

OrderRejectReason_Unknown = 0                           #未知原因
OrderRejectReason_RiskRuleCheckFailed = 1               #不符合风控规则
OrderRejectReason_NoEnoughCash = 2                      #资金不足
OrderRejectReason_NoEnoughPosition = 3                  #仓位不足
OrderRejectReason_IllegalAccountId = 4                  #非法账户ID
OrderRejectReason_IllegalStrategyId = 5                 #非法策略ID
OrderRejectReason_IllegalSymbol = 6                     #非法交易代码
OrderRejectReason_IllegalVolume = 7                     #非法委托量
OrderRejectReason_IllegalPrice = 8                      #非法委托价
OrderRejectReason_AccountDisabled = 10                  #交易账号被禁止交易
OrderRejectReason_AccountDisconnected = 11              #交易账号未连接
OrderRejectReason_AccountLoggedout = 12                 #交易账号未登录
OrderRejectReason_NotInTradingSession = 13              #非交易时段
OrderRejectReason_OrderTypeNotSupported = 14            #委托类型不支持
OrderRejectReason_Throttle = 15                         #流控限制
OrderRejectReason_SymbolSusppended = 16                 #交易代码停牌
OrderRejectReason_Internal = 999                        #内部错误

CancelOrderRejectReason_OrderFinalized = 101            #委托已完成
CancelOrderRejectReason_UnknownOrder = 102              #未知委托
CancelOrderRejectReason_BrokerOption = 103              #柜台设置
CancelOrderRejectReason_AlreadyInPendingCancel = 104    #委托撤销中

OrderSide_Unknown = 0
OrderSide_Buy     = 1    #买入
OrderSide_Sell    = 2    #卖出


OrderType_Unknown = 0
OrderType_Limit   = 1    #限价委托
OrderType_Market  = 2    #市价委托
OrderType_Stop    = 3    #止损止盈委托

OrderDuration_Unknown = 0
OrderDuration_FAK     = 1  #即时成交剩余撤销(fill and kill)
OrderDuration_FOK     = 2  #即时全额成交或撤销(fill or kill)
OrderDuration_GFD     = 3  #当日有效(good for day)
OrderDuration_GFS     = 4  #本节有效(good for section)
OrderDuration_GTD     = 5  #指定日期前有效(goodl till date)
OrderDuration_GTC     = 6  #撤销前有效(good till cancel)
OrderDuration_GFA     = 7  #集合竞价前有效(good for auction)

OrderQualifier_Unknown = 0
OrderQualifier_BOC     = 1  #对方最优价格(best of counterparty)
OrderQualifier_BOP     = 2  #己方最优价格(best of party)
OrderQualifier_B5TC    = 3  #最优五档剩余撤销(best 5 then cancel)
OrderQualifier_B5TL    = 4  #最优五档剩余转限价(best 5 then limit)

OrderStyle_Unknown = 0
OrderStyle_Volume = 1
OrderStyle_Value = 2
OrderStyle_Percent = 3
OrderStyle_TargetVolume = 4
OrderStyle_TargetValue = 5
OrderStyle_TargetPercent = 6

PositionSide_Unknown  = 0
PositionSide_Long     = 1   #多方向
PositionSide_Short    = 2   #空方向

PositionEffect_Unknown        = 0
PositionEffect_Open           = 1     #开仓
PositionEffect_Close          = 2     #平仓,具体语义取决于对应的交易所
PositionEffect_CloseToday     = 3     #平今仓
PositionEffect_CloseYesterday = 4     #平昨仓

CashPositionChangeReason_Unknown = 0
CashPositionChangeReason_Trade   = 1  #交易
CashPositionChangeReason_Inout   = 2  #出入金/出入持仓


# noinspection PyAbstractClass
class ExecType(EnumTypeWrapper):
    pass


# noinspection PyAbstractClass
class OrderStatus(EnumTypeWrapper):
    pass


# noinspection PyAbstractClass
class OrderRejectReason(EnumTypeWrapper):
    pass


# noinspection PyAbstractClass
class OrderSide(EnumTypeWrapper):
    pass


# noinspection PyAbstractClass
class OrderType(EnumTypeWrapper):
    pass


# noinspection PyAbstractClass
class OrderDuration(EnumTypeWrapper):
    pass


# noinspection PyAbstractClass
class OrderQualifier(EnumTypeWrapper):
    pass


# noinspection PyAbstractClass
class OrderStyle(EnumTypeWrapper):
    pass


# noinspection PyAbstractClass
class PositionSide(EnumTypeWrapper):
    pass


# noinspection PyAbstractClass
class PositionEffect(EnumTypeWrapper):
    pass


# noinspection PyAbstractClass
class CashPositionChangeReason(EnumTypeWrapper):
    pass


# 委托定义
# noinspection PyAbstractClass
class Order(Message):
    # 策略ID
    strategy_id = ... # type: Text
    # 账号ID
    account_id = ... # type: Text
    # 账户登录名
    account_name = ... # type: Text

    # 委托客户端ID
    cl_ord_id = ... # type: Text
    # 委托柜台ID
    order_id = ... # type: Text
    # 委托交易所ID
    ex_ord_id = ... # type: Text

    # symbol
    symbol = ... # type: Text
    # 买卖方向，取值参考enum OrderSide
    side = ... # type: int
    # 开平标志，取值参考enum PositionEffect
    position_effect = ... # type: int
    # 持仓方向，取值参考enum PositionSide
    position_side = ... # type: int

    # 委托类型，取值参考enum OrderType
    order_type = ... # type: int
    # 委托时间属性，取值参考enum OrderDuration
    order_duration = ... # type: int
    # 委托成交属性，取值参考enum OrderQualifier
    order_qualifier = ... # type: int
    # 委托来源，取值参考enum OrderSrc
    order_src = ... # type: int

    # 委托状态，取值参考enum OrderStatus
    status = ... # type: int
    # 委托拒绝原因，取值参考enum OrderRejectReason
    ord_rej_reason = ... # type: int
    # 委托拒绝原因描述
    ord_rej_reason_detail = ... # type: int

    # 委托价格
    price = ... # type: float
    # 委托止损/止盈触发价格
    stop_price = ... # type: float

    # 委托风格，取值参考 enum OrderStyle
    order_style = ... # type: int
    # 委托量
    volume = ... # type: int
    # 委托额
    value = ... # type: float
    # 委托百分比
    percent = ... # type: float
    # 委托目标量
    target_volume = ... # type: int
    # 委托目标额
    target_value = ... # type: float
    # 委托目标百分比
    target_percent = ... # type: float

    # 已成量
    filled_volume = ... # type: int
    # 已成均价
    filled_vwap = ... # type: float
    # 已成金额
    filled_amount = ... # type: float
    # 已成手续费
    filled_commission = ... # type: float

    # 委托创建时间
    created_at = ... # type: Timestamp
    # 委托更新时间
    updated_at = ... # type: Timestamp


# 委托集合
# noinspection PyAbstractClass
class Orders(Message):
    data = ... # type: RepeatedCompositeFieldContainer[Order]
    is_combined = ... # type: int
    properties = ... # type: Dict[Text, Text]


# 委托执行回报定义
# noinspection PyAbstractClass
class ExecRpt(Message):
    # 策略ID
    strategy_id = ... # type: Text
    # 账号ID
    account_id = ... # type: Text
    # 账户登录名
    account_name = ... # type: Text

    # 委托客户端ID
    cl_ord_id = ... # type: Text
    # 委托柜台ID
    order_id = ... # type: Text
    # 委托回报ID
    exec_id = ... # type: Text

    symbol = ... # type: Text

    # 开平标志，取值参考enum PositionEffect
    position_effect = ... # type: int
    # 买卖方向，取值参考enum OrderSide
    side = ... # type: int
    # 委托拒绝原因，取值参考enum OrderRejectReason
    ord_rej_reason = ... # type: int
    # 委托拒绝原因描述
    ord_rej_reason_detail = ... # type: Text
    # 执行回报类型, 取值参考enum ExecType
    exec_type = ... # type: int

    # 委托成交价格
    price = ... # type: float
    # 委托成交量
    volume = ... # type: int
    # 委托成交金额
    amount = ... # type: float
    # 委托成交手续费
    commission = ... # type: float

    const = ... # type: float

    # 回报创建时间
    created_at = ... # type: Timestamp


# 成交回报集合
# noinspection PyAbstractClass
class ExecRpts(Message):
    data = ... # type: RepeatedCompositeFieldContainer[ExecRpt]


# 资金定义
# noinspection PyAbstractClass
class Cash(Message):
    # 账号ID
    account_id = ... # type: Text
    # 账户登录名
    account_name = ... # type: Text

    # 币种
    currency = ... # type: int

    # 净值(cum_inout + cum_pnl + fpnl - cum_commission)
    nav = ... # type: float
    # 净收益(nav-cum_inout)
    pnl = ... # type: float
    # 浮动盈亏(sum(each position fpnl))
    fpnl = ... # type: float
    # 持仓占用资金
    frozen = ... # type: float
    # 挂单冻结资金
    order_frozen = ... # type: float
    # 可用资金
    available = ... # type: float

    # 累计出入金
    cum_inout = ... # type: float
    # 累计交易额
    cum_trade = ... # type: float
    # 累计平仓收益(没扣除手续费)
    cum_pnl = ... # type: float
    # 累计手续费
    cum_commission = ... # type: float

    # 上一次交易额
    last_trade = ... # type: float
    # 上一次收益
    last_pnl = ... # type: float
    # 上一次手续费
    last_commission = ... # type: float
    # 上一次出入金
    last_inout = ... # type: float
    # 资金变更原因，取值参考enum CashPositionChangeReason
    change_reason = ... # type: int
    # 触发资金变更事件的ID
    change_event_id = ... # type: Text

    # 资金初始时间
    created_at = ... # type: Timestamp
    # 资金变更时间
    updated_at = ... # type: Timestamp


# 资金集合
# noinspection PyAbstractClass
class Cashes(Message):
    data = ... # type: RepeatedCompositeFieldContainer[Cash]


# 持仓定义
# noinspection PyAbstractClass
class Position(Message):
    # 账号ID
    account_id = ... # type: Text
    # 账户登录名
    account_name = ... # type: Text

    symbol = ... # type: Text
    # 持仓方向，取值参考enum PositionSide
    side = ... # type: int
    # 总持仓量 昨持仓量(volume-volume_today)
    volume = ... # type: int
    # 今日持仓量
    volume_today = ... # type: int
    # 持仓均价
    vwap = ... # type: float
    # 持仓额(volume*vwap*multiplier)
    amount = ... # type: float

    # 当前行情价格
    price = ... # type: float
    # 持仓浮动盈亏((price-vwap)*volume*multiplier)
    fpnl = ... # type: float
    # 持仓成本(vwap*volume*multiplier*margin_ratio)
    cost = ... # type: float
    # 挂单冻结仓位
    order_frozen = ... # type: int
    # 挂单冻结今仓仓位
    order_frozen_today = ... # type: int
    # 可平总仓位(volume-order_frozen) 可平昨仓位(available-available_today)
    available = ... # type: int
    # 可平今仓位(volume_today-order_frozen_today)
    available_today = ... # type: int

    # 上一次成交价
    last_price = ... # type: float
    # 上一次成交量
    last_volume = ... # type: int
    # 上一次出入持仓量
    last_inout = ... # type: int
    # 仓位变更原因，取值参考enum CashPositionChangeReason
    change_reason = ... # type: int
    # 触发资金变更事件的ID
    change_event_id = ... # type: Text

    # 持仓区间有分红配送
    has_dividend = ... # type: int

    # 建仓时间
    created_at = ... # type: Timestamp
    # 仓位变更时间
    updated_at = ... # type: Timestamp


# 持仓集合
# noinspection PyAbstractClass
class Positions(Message):
    data = ... # type: RepeatedCompositeFieldContainer[Position]


# noinspection PyAbstractClass
class Account(Message):
    account_id = ... # type: Text
    account_name = ... # type: Text
    title = ... # type: Text
    intro = ... # type: Text
    comment = ... # type: Text

    created_at = ... # type: Timestamp
    updated_at = ... # type: Timestamp


# noinspection PyAbstractClass
class Accounts(Message):
    data = ... # type: RepeatedCompositeFieldContainer[Account]


# noinspection PyAbstractClass
class AccountStatus(Message):
    account_id = ... # type: Text
    account_name = ... # type: Text
    status = ... # type: ConnectionStatus


# noinspection PyAbstractClass
class AccountStatuses(Message):
    data = ... # type: RepeatedCompositeFieldContainer[AccountStatus]


# 账号通道
# noinspection PyAbstractClass
class AccountChannel(Message):
    Mode_Unknown     = 0
    Mode_Local       = 1
    Mode_Remote      = 2
    Mode_RemoteShare = 3

    Type_Unknown    = 0
    Type_Simulate   = 1
    Type_Live       = 2

    # 通道ID: CTP,飞马,SimNow,金证,恒生等
    channel_id = ... # type: Text
    # 通道名称
    title = ... # type: Text

    # 通道描述
    intro = ... # type: Text
    # 通道接入模式: local/remote/remote_share
    mode = ... # type: int
    # 通道支持的交易所
    exchanges = ... # type: RepeatedScalarFieldContainer[Text]
    # 通道支持的证券类型: A股，期货，期权等
    sec_types = ... # type: RepeatedScalarFieldContainer[int]

    # 通道默认连接地址
    conn_addr = ... # type: RepeatedCompositeFieldContainer[ConnectionAddress]
    # 不允许用户修改连接地址
    conn_addr_fixed = ... # type: bool
    # 通道默认的其他配置
    conn_conf = ... # type: Dict[Text, Text]
    # 通道默认的仿真/实盘属性
    conn_type = ... # type: int


# noinspection PyAbstractClass
class AccountChannels(Message):
    data = ... # type: RepeatedCompositeFieldContainer[AccountChannel]


# noinspection PyAbstractClass
class AccountConnection(Message):
    account = ... # type: Account
    channel_id = ... # type: Text

    conn_addr = ... # type: ConnectionAddress
    conn_conf = ... # type: Dict[Text, Text]

    # 连接的仿真/实盘属性
    conn_type = ... # type: int

# noinspection PyAbstractClass
class AccountConnections(Message):
    data = ... # type: RepeatedCompositeFieldContainer[AccountConnection]
