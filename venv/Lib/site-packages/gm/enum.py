# coding=utf8
from __future__ import print_function, absolute_import, unicode_literals

ExecType_Unknown = 0
ExecType_New = 1  # 已报
ExecType_DoneForDay = 4  #
ExecType_Canceled = 5  # 已撤销
ExecType_PendingCancel = 6  # 待撤销
ExecType_Stopped = 7  #
ExecType_Rejected = 8  # 已拒绝
ExecType_Suspended = 9  # 挂起
ExecType_PendingNew = 10  # 待报
ExecType_Calculated = 11  #
ExecType_Expired = 12  # 过期
ExecType_Restated = 13  #
ExecType_PendingReplace = 14  #
ExecType_Trade = 15  # 成交
ExecType_TradeCorrect = 16  #
ExecType_TradeCancel = 17  #
ExecType_OrderStatus = 18  # 委托状态
ExecType_CancelRejected = 19  # 撤单被拒绝

OrderStatus_Unknown = 0
OrderStatus_New = 1  # 已报
OrderStatus_PartiallyFilled = 2  # 部成
OrderStatus_Filled = 3  # 已成
OrderStatus_DoneForDay = 4  #
OrderStatus_Canceled = 5  # 已撤
OrderStatus_PendingCancel = 6  # 待撤
OrderStatus_Stopped = 7  #
OrderStatus_Rejected = 8  # 已拒绝
OrderStatus_Suspended = 9  # 挂起
OrderStatus_PendingNew = 10  # 待报
OrderStatus_Calculated = 11  #
OrderStatus_Expired = 12  # 已过期
OrderStatus_AcceptedForBidding = 13  #
OrderStatus_PendingReplace = 14  #

OrderRejectReason_Unknown = 0  # 未知原因
OrderRejectReason_RiskRuleCheckFailed = 1  # 不符合风控规则
OrderRejectReason_NoEnoughCash = 2  # 资金不足
OrderRejectReason_NoEnoughPosition = 3  # 仓位不足
OrderRejectReason_IllegalAccountId = 4  # 非法账户ID
OrderRejectReason_IllegalStrategyId = 5  # 非法策略ID
OrderRejectReason_IllegalSymbol = 6  # 非法交易标的
OrderRejectReason_IllegalVolume = 7  # 非法委托量
OrderRejectReason_IllegalPrice = 8  # 非法委托价
OrderRejectReason_AccountDisabled = 10  # 交易账号被禁止交易
OrderRejectReason_AccountDisconnected = 11  # 交易账号未连接
OrderRejectReason_AccountLoggedout = 12  # 交易账号未登录
OrderRejectReason_NotInTradingSession = 13  # 非交易时段
OrderRejectReason_OrderTypeNotSupported = 14  # 委托类型不支持
OrderRejectReason_Throttle = 15  # 流控限制

CancelOrderRejectReason_OrderFinalized = 101  # 委托已完成
CancelOrderRejectReason_UnknownOrder = 102  # 未知委托
CancelOrderRejectReason_BrokerOption = 103  # 柜台设置
CancelOrderRejectReason_AlreadyInPendingCancel = 104  # 委托撤销中

OrderSide_Unknown = 0
OrderSide_Buy = 1  # 买入
OrderSide_Sell = 2  # 卖出

OrderType_Unknown = 0
OrderType_Limit = 1  # 限价委托
OrderType_Market = 2  # 市价委托
OrderType_Stop = 3  # 止损止盈委托

OrderDuration_Unknown = 0
OrderDuration_FAK = 1  # 即时成交剩余撤销(fill and kill)
OrderDuration_FOK = 2  # 即时全额成交或撤销(fill or kill)
OrderDuration_GFD = 3  # 当日有效(good for day)
OrderDuration_GFS = 4  # 本节有效(good for section)
OrderDuration_GTD = 5  # 指定日期前有效(goodltilldate)
OrderDuration_GTC = 6  # 撤销前有效(goodtillcancel)
OrderDuration_GFA = 7  # 集合竞价前有效(good for auction)

OrderQualifier_Unknown = 0
OrderQualifier_BOC = 1  # 对方最优价格(best of counterparty)
OrderQualifier_BOP = 2  # 己方最优价格(best of party)
OrderQualifier_B5TC = 3  # 最优五档剩余撤销(best 5 then cancel)
OrderQualifier_B5TL = 4  # 最优五档剩余转限价(best 5 then limit)

OrderStyle_Unknown = 0
OrderStyle_Volume = 1
OrderStyle_Value = 2
OrderStyle_Percent = 3
OrderStyle_TargetVolume = 4
OrderStyle_TargetValue = 5
OrderStyle_TargetPercent = 6

PositionSide_Unknown = 0
PositionSide_Long = 1  # 多方向
PositionSide_Short = 2  # 空方向

PositionEffect_Unknown = 0
PositionEffect_Open = 1  # 开仓
PositionEffect_Close = 2  # 平仓, 具体语义取决于对应的交易所
PositionEffect_CloseToday = 3  # 平今仓
PositionEffect_CloseYesterday = 4  # 平昨仓

CashPositionChangeReason_Unknown = 0
CashPositionChangeReason_Trade = 1  # 交易
CashPositionChangeReason_Inout = 2  # 出入金 / 出入持仓

MODE_UNKNOWN = 0
MODE_LIVE = 1
MODE_BACKTEST = 2

ADJUST_NONE = 0
ADJUST_PREV = 1
ADJUST_POST = 2

SEC_TYPE_STOCK = 1
SEC_TYPE_FUND = 2
SEC_TYPE_INDEX = 3
SEC_TYPE_FUTURE = 4
SEC_TYPE_OPTION = 5
SEC_TYPE_CONFUTURE = 10
