# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import

from datetime import datetime

from typing import NoReturn, Text, Optional


class DictLikeExecRpt(dict):
    """
    A dict that allows for ExecRpt-like property access syntax.
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, item, value):
        self[item] = value

    def __str__(self):
        return super(DictLikeExecRpt, self).__str__()

    def __repr__(self):
        return super(DictLikeExecRpt, self).__repr__()

    @property
    def strategy_id(self):
        # type: ()->Text
        """
        策略ID
        """
        return self['strategy_id']

    @strategy_id.setter
    def strategy_id(self, value):
        # type: (Text) -> NoReturn
        self['strategy_id'] = value

    @property
    def account_id(self):
        # type: ()->Text
        """
        账号ID
        """
        return self['account_id']

    @account_id.setter
    def account_id(self, value):
        # type: (Text) -> NoReturn
        self['account_id'] = value

    @property
    def account_name(self):
        # type: ()->Text
        """
        账户登录名
        """
        return self['account_name']

    @account_name.setter
    def account_name(self, value):
        # type: (Text) -> NoReturn
        self['account_name'] = value

    @property
    def cl_ord_id(self):
        # type: ()->Text
        """
        委托客户端ID
        """
        return self['cl_ord_id']

    @cl_ord_id.setter
    def cl_ord_id(self, value):
        # type: (Text) -> NoReturn
        self['cl_ord_id'] = value

    @property
    def order_id(self):
        # type: ()->Text
        """
        委托柜台ID
        """
        return self['order_id']

    @order_id.setter
    def order_id(self, value):
        # type: (Text) -> NoReturn
        self['order_id'] = value

    @property
    def exec_id(self):
        # type: ()->Text
        """
        委托回报ID
        """
        return self['exec_id']

    @exec_id.setter
    def exec_id(self, value):
        # type: (Text) -> NoReturn
        self['exec_id'] = value

    @property
    def symbol(self):
        # type: ()->Text
        """
        symbol
        """
        return self['symbol']

    @symbol.setter
    def symbol(self, value):
        # type: (Text) -> NoReturn
        self['symbol'] = value

    @property
    def position_effect(self):
        # type: ()->int
        """
        开平标志，取值参考enum PositionEffect
        """
        return self['position_effect']

    @position_effect.setter
    def position_effect(self, value):
        # type: (int) -> NoReturn
        self['position_effect'] = value

    @property
    def side(self):
        # type: ()->int
        """
        买卖方向，取值参考enum OrderSide
        """
        return self['side']

    @side.setter
    def side(self, value):
        # type: (int) -> NoReturn
        self['side'] = value

    @property
    def ord_rej_reason(self):
        # type: ()->int
        """
        委托拒绝原因，取值参考enum OrderRejectReason
        """
        return self['ord_rej_reason']

    @ord_rej_reason.setter
    def ord_rej_reason(self, value):
        # type: (int) -> NoReturn
        self['ord_rej_reason'] = value

    @property
    def ord_rej_reason_detail(self):
        # type: ()->Text
        """
        委托拒绝原因描述
        """
        return self['ord_rej_reason_detail']

    @ord_rej_reason_detail.setter
    def ord_rej_reason_detail(self, value):
        # type: (Text) -> NoReturn
        self['ord_rej_reason_detail'] = value

    @property
    def exec_type(self):
        # type: ()->Text
        """
        执行回报类型, 取值参考enum ExecType
        """
        return self['exec_type']

    @exec_type.setter
    def exec_type(self, value):
        # type: (Text) -> NoReturn
        self['exec_type'] = value

    @property
    def price(self):
        # type: ()->float
        """
        委托成交价格
        """
        return self['price']

    @price.setter
    def price(self, value):
        # type: (float) -> NoReturn
        self['price'] = value

    @property
    def volume(self):
        # type: ()->int
        """
        委托成交量
        """
        return self['volume']

    @volume.setter
    def volume(self, value):
        # type: (int) -> NoReturn
        self['volume'] = value

    @property
    def amount(self):
        # type: ()->float
        """
        委托成交金额
        """
        return self['amount']

    @amount.setter
    def amount(self, value):
        # type: (float) -> NoReturn
        self['amount'] = value

    @property
    def commission(self):
        # type: ()->Text
        """
        委托成交手续费
        """
        return self['commission']

    @commission.setter
    def commission(self, value):
        # type: (Text) -> NoReturn
        self['commission'] = value

    @property
    def const(self):
        # type: ()->float
        """
        成本
        """
        return self['const']

    @const.setter
    def const(self, value):
        # type: (float) -> NoReturn
        self['const'] = value

    @property
    def created_at(self):
        # type: ()->Optional[datetime]
        """
        回报创建时间
        """
        return self['created_at']

    @created_at.setter
    def created_at(self, value):
        # type: (Optional[datetime]) -> NoReturn
        self['created_at'] = value


class DictLikeOrder(dict):
    """
    A dict that allows for Order-like property access syntax.
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, item, value):
        self[item] = value

    def __str__(self):
        return super(DictLikeOrder, self).__str__()

    def __repr__(self):
        return super(DictLikeOrder, self).__repr__()

    @property
    def strategy_id(self):
        # type: ()->Text
        """
        策略ID
        """
        return self['strategy_id']

    @strategy_id.setter
    def strategy_id(self, value):
        # type: (Text) -> NoReturn
        self['strategy_id'] = value

    @property
    def account_id(self):
        # type: ()->Text
        """
        账号ID
        """
        return self['account_id']

    @account_id.setter
    def account_id(self, value):
        # type: (Text) -> NoReturn
        self['account_id'] = value

    @property
    def account_name(self):
        # type: ()->Text
        """
        账户登录名
        """
        return self['account_name']

    @account_name.setter
    def account_name(self, value):
        # type: (Text) -> NoReturn
        self['account_name'] = value

    @property
    def cl_ord_id(self):
        # type: ()->Text
        """
        委托客户端ID
        """
        return self['cl_ord_id']

    @cl_ord_id.setter
    def cl_ord_id(self, value):
        # type: (Text) -> NoReturn
        self['cl_ord_id'] = value

    @property
    def order_id(self):
        # type: ()->Text
        """
        委托柜台ID
        """
        return self['order_id']

    @order_id.setter
    def order_id(self, value):
        # type: (Text) -> NoReturn
        self['order_id'] = value

    @property
    def ex_ord_id(self):
        # type: ()->Text
        """
        委托交易所ID
        """
        return self['ex_ord_id']

    @ex_ord_id.setter
    def ex_ord_id(self, value):
        # type: (Text) -> NoReturn
        self['ex_ord_id'] = value

    @property
    def symbol(self):
        # type: ()->Text
        """
        symbol
        """
        return self['symbol']

    @symbol.setter
    def symbol(self, value):
        # type: (Text) -> NoReturn
        self['symbol'] = value

    @property
    def side(self):
        # type: ()->int
        """
        买卖方向，取值参考enum OrderSide
        """
        return self['side']

    @side.setter
    def side(self, value):
        # type: (int) -> NoReturn
        self['side'] = value

    @property
    def position_effect(self):
        # type: ()->int
        """
        开平标志，取值参考enum PositionEffect
        """
        return self['position_effect']

    @position_effect.setter
    def position_effect(self, value):
        # type: (int) -> NoReturn
        self['position_effect'] = value

    @property
    def position_side(self):
        # type: ()->int
        """
        持仓方向，取值参考enum PositionSide
        """
        return self['position_side']

    @position_side.setter
    def position_side(self, value):
        # type: (int) -> NoReturn
        self['position_side'] = value

    @property
    def order_type(self):
        # type: ()->int
        """
        委托类型，取值参考enum OrderType
        """
        return self['order_type']

    @order_type.setter
    def order_type(self, value):
        # type: (int) -> NoReturn
        self['order_type'] = value

    @property
    def order_duration(self):
        # type: ()->int
        """
        委托时间属性，取值参考enum OrderDuration
        """
        return self['order_duration']

    @order_duration.setter
    def order_duration(self, value):
        # type: (int) -> NoReturn
        self['order_duration'] = value

    @property
    def order_qualifier(self):
        # type: ()->int
        """
        委托成交属性，取值参考enum OrderQualifier
        """
        return self['order_qualifier']

    @order_qualifier.setter
    def order_qualifier(self, value):
        # type: (int) -> NoReturn
        self['order_qualifier'] = value

    @property
    def order_src(self):
        # type: ()->int
        """
        委托来源，取值参考enum OrderSrc
        """
        return self['order_src']

    @order_src.setter
    def order_src(self, value):
        # type: (int) -> NoReturn
        self['order_src'] = value

    @property
    def status(self):
        # type: ()->int
        """
        委托状态，取值参考enum OrderStatus
        """
        return self['status']

    @status.setter
    def status(self, value):
        # type: (int) -> NoReturn
        self['status'] = value

    @property
    def ord_rej_reason(self):
        # type: ()->int
        """
        委托拒绝原因，取值参考enum OrderRejectReason
        """
        return self['ord_rej_reason']

    @ord_rej_reason.setter
    def ord_rej_reason(self, value):
        # type: (int) -> NoReturn
        self['ord_rej_reason'] = value

    @property
    def ord_rej_reason_detail(self):
        # type: ()->int
        """
        委托拒绝原因描述
        """
        return self['ord_rej_reason_detail']

    @ord_rej_reason_detail.setter
    def ord_rej_reason_detail(self, value):
        # type: (int) -> NoReturn
        self['ord_rej_reason_detail'] = value

    @property
    def price(self):
        # type: ()->float
        """
        委托价格
        """
        return self['price']

    @price.setter
    def price(self, value):
        # type: (float) -> NoReturn
        self['price'] = value

    @property
    def stop_price(self):
        # type: ()->float
        """
        委托止损/止盈触发价格
        """
        return self['stop_price']

    @stop_price.setter
    def stop_price(self, value):
        # type: (float) -> NoReturn
        self['stop_price'] = value

    @property
    def order_style(self):
        # type: ()->int
        """
        委托风格，取值参考 enum OrderStyle
        """
        return self['order_style']

    @order_style.setter
    def order_style(self, value):
        # type: (int) -> NoReturn
        self['order_style'] = value

    @property
    def volume(self):
        # type: ()->int
        """
        委托量
        """
        return self['volume']

    @volume.setter
    def volume(self, value):
        # type: (int) -> NoReturn
        self['volume'] = value

    @property
    def value(self):
        # type: ()->float
        """
        委托额
        """
        return self['value']

    @value.setter
    def value(self, value):
        # type: (float) -> NoReturn
        self['value'] = value

    @property
    def percent(self):
        # type: ()->float
        """
        委托百分比
        """
        return self['percent']

    @percent.setter
    def percent(self, value):
        # type: (float) -> NoReturn
        self['percent'] = value

    @property
    def target_volume(self):
        # type: ()->int
        """
        委托目标量
        """
        return self['target_volume']

    @target_volume.setter
    def target_volume(self, value):
        # type: (int) -> NoReturn
        self['target_volume'] = value

    @property
    def target_value(self):
        # type: ()->float
        """
        委托目标额
        """
        return self['target_value']

    @target_value.setter
    def target_value(self, value):
        # type: (float) -> NoReturn
        self['target_value'] = value

    @property
    def target_percent(self):
        # type: ()->float
        """
        委托目标百分比
        """
        return self['target_percent']

    @target_percent.setter
    def target_percent(self, value):
        # type: (float) -> NoReturn
        self['target_percent'] = value

    @property
    def filled_volume(self):
        # type: ()->int
        """
        已成量
        """
        return self['filled_volume']

    @filled_volume.setter
    def filled_volume(self, value):
        # type: (int) -> NoReturn
        self['filled_volume'] = value

    @property
    def filled_vwap(self):
        # type: ()->float
        """
        已成均价
        """
        return self['filled_vwap']

    @filled_vwap.setter
    def filled_vwap(self, value):
        # type: (float) -> NoReturn
        self['filled_vwap'] = value

    @property
    def filled_amount(self):
        # type: ()->float
        """
        已成金额
        """
        return self['filled_amount']

    @filled_amount.setter
    def filled_amount(self, value):
        # type: (float) -> NoReturn
        self['filled_amount'] = value

    @property
    def filled_commission(self):
        # type: ()->float
        """
        已成手续费
        """
        return self['filled_commission']

    @filled_commission.setter
    def filled_commission(self, value):
        # type: (float) -> NoReturn
        self['filled_commission'] = value

    @property
    def created_at(self):
        # type: ()->Optional[datetime]
        """
        委托创建时间
        """
        return self['created_at']

    @created_at.setter
    def created_at(self, value):
        # type: (Optional[datetime]) -> NoReturn
        self['created_at'] = value

    @property
    def updated_at(self):
        # type: ()->Optional[datetime]
        """
        委托更新时间
        """
        return self['updated_at']

    @updated_at.setter
    def updated_at(self, value):
        # type: (Optional[datetime]) -> NoReturn
        self['updated_at'] = value


class DictLikeIndicator(dict):
    """
    A dict that allows for Indicator-like property access syntax.
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, item, value):
        self[item] = value

    def __str__(self):
        return super(DictLikeIndicator, self).__str__()

    def __repr__(self):
        return super(DictLikeIndicator, self).__repr__()

    @property
    def account_id(self):
        # type: ()->Text
        """
        账号ID
        """
        return self['account_id']

    @account_id.setter
    def account_id(self, value):
        # type: (Text) -> NoReturn
        self['account_id'] = value

    @property
    def pnl_ratio(self):
        # type: ()->float
        """
        累计收益率(pnl/cum_inout)
        """
        return self['pnl_ratio']

    @pnl_ratio.setter
    def pnl_ratio(self, value):
        # type: (float) -> NoReturn
        self['pnl_ratio'] = value

    @property
    def pnl_ratio_annual(self):
        # type: ()->float
        """
        年化收益率
        """
        return self['pnl_ratio_annual']

    @pnl_ratio_annual.setter
    def pnl_ratio_annual(self, value):
        # type: (float) -> NoReturn
        self['pnl_ratio_annual'] = value

    @property
    def sharp_ratio(self):
        # type: ()->float
        """
        夏普比率
        """
        return self['sharp_ratio']

    @sharp_ratio.setter
    def sharp_ratio(self, value):
        # type: (float) -> NoReturn
        self['sharp_ratio'] = value

    @property
    def max_drawdown(self):
        # type: ()->float
        """
        最大回撤
        """
        return self['max_drawdown']

    @max_drawdown.setter
    def max_drawdown(self, value):
        # type: (float) -> NoReturn
        self['max_drawdown'] = value

    @property
    def risk_ratio(self):
        # type: ()->float
        """
        风险比率
        """
        return self['risk_ratio']

    @risk_ratio.setter
    def risk_ratio(self, value):
        # type: (float) -> NoReturn
        self['risk_ratio'] = value

    @property
    def open_count(self):
        # type: ()->int
        """
        开仓次数
        """
        return self['open_count']

    @open_count.setter
    def open_count(self, value):
        # type: (int) -> NoReturn
        self['open_count'] = value

    @property
    def close_count(self):
        # type: ()->int
        """
        平仓次数
        """
        return self['close_count']

    @close_count.setter
    def close_count(self, value):
        # type: (int) -> NoReturn
        self['close_count'] = value

    @property
    def win_count(self):
        # type: ()->int
        """
        盈利次数
        """
        return self['win_count']

    @win_count.setter
    def win_count(self, value):
        # type: (int) -> NoReturn
        self['win_count'] = value

    @property
    def lose_count(self):
        # type: ()->int
        """
        亏损次数
        """
        return self['lose_count']

    @lose_count.setter
    def lose_count(self, value):
        # type: (int) -> NoReturn
        self['lose_count'] = value

    @property
    def win_ratio(self):
        # type: ()->float
        """
        胜率
        """
        return self['win_ratio']

    @win_ratio.setter
    def win_ratio(self, value):
        # type: (float) -> NoReturn
        self['win_ratio'] = value

    @property
    def calmar_ratio(self):
        # type: ()->float
        """
        卡玛比率
        """
        return self['calmar_ratio']

    @calmar_ratio.setter
    def calmar_ratio(self, value):
        # type: (float) -> NoReturn
        self['calmar_ratio'] = value

    @property
    def created_at(self):
        # type: ()->Optional[datetime]
        """

        """
        return self['created_at']

    @created_at.setter
    def created_at(self, value):
        # type: (Optional[datetime]) -> NoReturn
        self['created_at'] = value

    @property
    def updated_at(self):
        # type: ()->Optional[datetime]
        """

        """
        return self['updated_at']

    @updated_at.setter
    def updated_at(self, value):
        # type: (Optional[datetime]) -> NoReturn
        self['updated_at'] = value


class DictLikeParameter(dict):
    """
    A dict that allows for Parameter-like property access syntax.
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, item, value):
        self[item] = value

    def __str__(self):
        return super(DictLikeParameter, self).__str__()

    def __repr__(self):
        return super(DictLikeParameter, self).__repr__()

    @property
    def key(self):
        # type: ()->Text
        """

        """
        return self['key']

    @key.setter
    def key(self, value):
        # type: (Text) -> NoReturn
        self['key'] = value

    @property
    def value(self):
        # type: ()->float
        """

        """
        return self['value']

    @value.setter
    def value(self, value):
        # type: (float) -> NoReturn
        self['value'] = value

    @property
    def min(self):
        # type: ()->float
        """

        """
        return self['min']

    @min.setter
    def min(self, value):
        # type: (float) -> NoReturn
        self['min'] = value

    @property
    def max(self):
        # type: ()->float
        """

        """
        return self['max']

    @max.setter
    def max(self, value):
        # type: (float) -> NoReturn
        self['max'] = value

    @property
    def name(self):
        # type: ()->Text
        """

        """
        return self['name']

    @name.setter
    def name(self, value):
        # type: (Text) -> NoReturn
        self['name'] = value

    @property
    def intro(self):
        # type: ()->Text
        """

        """
        return self['intro']

    @intro.setter
    def intro(self, value):
        # type: (Text) -> NoReturn
        self['intro'] = value

    @property
    def group(self):
        # type: ()->Text
        """

        """
        return self['group']

    @group.setter
    def group(self, value):
        # type: (Text) -> NoReturn
        self['group'] = value

    @property
    def readonly(self):
        # type: ()->bool
        """

        """
        return self['readonly']

    @readonly.setter
    def readonly(self, value):
        # type: (bool) -> NoReturn
        self['readonly'] = value


class DictLikeAccountStatus(dict):
    """
    A dict that allows for AccountStatus-like property access syntax.
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, item, value):
        self[item] = value

    def __str__(self):
        return super(DictLikeAccountStatus, self).__str__()

    def __repr__(self):
        return super(DictLikeAccountStatus, self).__repr__()

    @property
    def account_id(self):
        # type: ()->Text

        return self['account_id']

    @account_id.setter
    def account_id(self, value):
        # type: (Text) -> NoReturn
        self['account_id'] = value

    @property
    def account_name(self):
        # type: ()->Text

        return self['account_name']

    @account_name.setter
    def account_name(self, value):
        # type: (Text) -> NoReturn
        self['account_name'] = value

    @property
    def status(self):
        # type: ()->DictLikeConnectionStatus

        return self['status']

    @status.setter
    def status(self, value):
        # type: (DictLikeConnectionStatus) -> NoReturn
        self['status'] = value


class DictLikeConnectionStatus(dict):
    """
    A dict that allows for ConnectionStatus-like property access syntax.
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, item, value):
        self[item] = value

    def __str__(self):
        return super(DictLikeConnectionStatus, self).__str__()

    def __repr__(self):
        return super(DictLikeConnectionStatus, self).__repr__()

    @property
    def state(self):
        # type: ()->int

        return self['state']

    @state.setter
    def state(self, value):
        # type: (int) -> NoReturn
        self['state'] = value

    @property
    def error(self):
        # type: ()->DictLikeError

        return self['error']

    @error.setter
    def error(self, value):
        # type: (DictLikeError) -> NoReturn
        self['error'] = value


class DictLikeError(dict):
    """
    A dict that allows for Error-like property access syntax.
    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, item, value):
        self[item] = value

    def __str__(self):
        return super(DictLikeError, self).__str__()

    def __repr__(self):
        return super(DictLikeError, self).__repr__()

    @property
    def code(self):
        # type: ()->int

        return self['code']

    @code.setter
    def code(self, value):
        # type: (int) -> NoReturn
        self['code'] = value

    @property
    def type(self):
        # type: ()->Text

        return self['type']

    @type.setter
    def type(self, value):
        # type: (Text) -> NoReturn
        self['type'] = value

    @property
    def info(self):
        # type: ()->Text

        return self['info']

    @info.setter
    def info(self, value):
        # type: (Text) -> NoReturn
        self['info'] = value
