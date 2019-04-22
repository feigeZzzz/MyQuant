# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import

import six
from typing import Text, List, Dict, NoReturn, Any, Union

from gm.csdk.c_sdk import py_gmi_place_order, py_gmi_get_unfinished_orders, py_gmi_get_orders, \
    py_gmi_cancel_all_orders, py_gmi_close_all_positions, py_gmi_cancel_order, py_gmi_get_execution_reports, \
    c_status_fail
from gm.enum import OrderQualifier_Unknown, OrderDuration_Unknown
from gm.model.storage import context
from gm.pb.account_pb2 import Order, Orders, OrderStyle_Volume, OrderStyle_Value, OrderStyle_Percent, \
    OrderStyle_TargetVolume, OrderStyle_TargetValue, OrderStyle_TargetPercent, ExecRpts
from gm.pb.trade_pb2 import GetUnfinishedOrdersReq, GetOrdersReq, CancelAllOrdersReq, CloseAllPositionsReq, \
    GetExecrptsReq
from gm.pb_to_dict import protobuf_to_dict
from gm.utils import load_to_list, datetime2timestamp


def _inner_place_order(o):
    # type: (Order) ->List[Dict[Text, Any]]
    """
    下单并返回order的信息. 同步调用, 在下单返回的order 的 client_order_id 将会有值.
    下单出错的话, 返回空的list
    """
    # 在回测模式且wait_group=True时, 设置这个created_at, 也就是通知c底层要根据这个时间设置price
    if context.is_backtest_model() and context.has_wait_group:
        o.created_at.seconds = datetime2timestamp(context.now)

    orders = Orders()
    orders.data.extend([o])

    req = orders.SerializeToString()
    status, result = py_gmi_place_order(req)
    if c_status_fail(status, 'py_gmi_place_order'):
        return []

    if not result:
        return []

    res = Orders()
    res.ParseFromString(result)

    return [protobuf_to_dict(res_order, including_default_value_fields=True) for res_order in res.data]


def order_volume(symbol, volume, side, order_type, position_effect,
                 price=0, order_duration=OrderDuration_Unknown, order_qualifier=OrderQualifier_Unknown, account=''):
    # type: (Text, float, int, int, int, float, int, int, Text) ->List[Dict[Text, Any]]
    """
    按指定量委托
    """
    order_style = OrderStyle_Volume
    account_id = get_account_id(account)

    o = Order()
    o.symbol = symbol
    o.volume = volume
    o.price = price
    o.side = side
    o.order_type = order_type
    o.position_effect = position_effect
    o.order_style = order_style
    o.order_qualifier = order_qualifier
    o.order_duration = order_duration
    o.account_id = account_id

    return _inner_place_order(o)


def order_value(symbol, value, side, order_type, position_effect,
                price=0, order_duration=OrderDuration_Unknown, order_qualifier=OrderQualifier_Unknown, account=''):
    # type:(Text, float, int, int, int, float, int, int, Text) ->List[Dict[Text, Any]]
    """
    按指定价值委托
    """
    order_style = OrderStyle_Value
    account_id = get_account_id(account)

    o = Order()
    o.symbol = symbol
    o.value = value
    o.price = price
    o.side = side
    o.order_type = order_type
    o.position_effect = position_effect
    o.order_style = order_style
    o.order_qualifier = order_qualifier
    o.order_duration = order_duration
    o.account_id = account_id

    return _inner_place_order(o)


def order_percent(symbol, percent, side, order_type, position_effect,
                  price=0, order_duration=OrderDuration_Unknown, order_qualifier=OrderQualifier_Unknown, account=''):
    # type: (Text, float, int, int, int, float, int, int, Text)->List[Dict[Text, Any]]
    """
    按指定比例委托
    """
    order_style = OrderStyle_Percent
    account_id = get_account_id(account)

    o = Order()
    o.symbol = symbol
    o.percent = percent
    o.price = price
    o.side = side
    o.order_type = order_type
    o.position_effect = position_effect
    o.order_qualifier = order_qualifier
    o.order_duration = order_duration
    o.order_style = order_style
    o.account_id = account_id

    return _inner_place_order(o)


def order_target_volume(symbol, volume, position_side, order_type, price=0, order_duration=OrderDuration_Unknown,
                        order_qualifier=OrderQualifier_Unknown, account=''):
    # type: (Text, float, int, int, float, int, int, Text) ->List[Dict[Text, Any]]
    """
    调仓到目标持仓量
    """
    order_style = OrderStyle_TargetVolume
    account_id = get_account_id(account)

    o = Order()
    o.symbol = symbol
    o.target_volume = volume
    o.price = price
    o.position_side = position_side
    o.order_type = order_type
    o.order_qualifier = order_qualifier
    o.order_duration = order_duration
    o.order_style = order_style
    o.account_id = account_id

    return _inner_place_order(o)


def order_target_value(symbol, value, position_side, order_type, price=0,
                       order_duration=OrderDuration_Unknown, order_qualifier=OrderQualifier_Unknown, account=''):
    # type: (Text, float, int, int, float, int, int, Text) ->List[Dict[Text, Any]]
    """
    调仓到目标持仓额
    """
    order_style = OrderStyle_TargetValue
    account_id = get_account_id(account)

    o = Order()
    o.symbol = symbol
    o.target_value = value
    o.price = price
    o.position_side = position_side
    o.order_type = order_type
    o.order_qualifier = order_qualifier
    o.order_duration = order_duration
    o.order_style = order_style
    o.account_id = account_id

    return _inner_place_order(o)


def order_target_percent(symbol, percent, position_side, order_type, price=0, order_duration=OrderDuration_Unknown,
                         order_qualifier=OrderQualifier_Unknown, account=''):
    # type: (Text, float, int, int, float, int, int, Text) ->List[Dict[Text, Any]]
    """
    调仓到目标持仓比例
    """
    order_style = OrderStyle_TargetPercent
    account_id = get_account_id(account)

    o = Order()
    o.symbol = symbol
    o.target_percent = percent
    o.price = price
    o.position_side = position_side
    o.order_type = order_type
    o.order_qualifier = order_qualifier
    o.order_duration = order_duration
    o.order_style = order_style
    o.account_id = account_id

    return _inner_place_order(o)


def get_unfinished_orders():
    # type: ()->List[Dict[Text, Any]]
    """
    查询所有未结委托
    """
    unfinished_orders = []
    for account in six.itervalues(context.accounts):
        req = GetUnfinishedOrdersReq()
        req.account_id = account.id
        req = req.SerializeToString()
        status, result = py_gmi_get_unfinished_orders(req)
        if c_status_fail(status, 'py_gmi_get_unfinished_orders'):
            return []

        res = Orders()
        res.ParseFromString(result)
        unfinished_orders.extend(
            [protobuf_to_dict(res_order, including_default_value_fields=True) for res_order in res.data])

    return unfinished_orders


def get_orders():
    # type: () ->List[Dict[Text, Any]]
    """
    查询日内全部委托
    """
    all_orders = []
    for account in six.itervalues(context.accounts):
        req = GetOrdersReq()
        req.account_id = account.id
        req = req.SerializeToString()
        status, result = py_gmi_get_orders(req)
        if c_status_fail(status, 'py_gmi_get_orders'):
            return []

        if not result:
            return []

        res = Orders()
        res.ParseFromString(result)

        all_orders.extend([protobuf_to_dict(res_order, including_default_value_fields=True) for res_order in res.data])

    return all_orders


def order_cancel_all():
    # type: () ->NoReturn
    """
    撤销所有委托
    """
    req = CancelAllOrdersReq()
    for account in six.itervalues(context.accounts):
        req.account_ids.extend([account.id])

    req = req.SerializeToString()
    py_gmi_cancel_all_orders(req)


def order_close_all():
    # type: () ->List[Dict[Text, Any]]
    """
    平当前所有可平持仓
    """
    req = CloseAllPositionsReq()
    for account in six.itervalues(context.accounts):
        req.account_ids.extend([account.id])

    req = req.SerializeToString()
    status, result = py_gmi_close_all_positions(req)
    if c_status_fail(status, 'py_gmi_close_all_positions'):
        return []

    if not result:
        return []

    res = Orders()
    res.ParseFromString(result)

    return [protobuf_to_dict(res_order, including_default_value_fields=True) for res_order in res.data]


def order_cancel(wait_cancel_orders):
    # type: (Union[Dict[Text,Any], List[Dict[Text, Any]]]) ->NoReturn
    """
    撤销委托. 传入单个字典. 或者list字典. 每个字典包含key: cl_ord_id, account_id
    """
    wait_cancel_orders = load_to_list(wait_cancel_orders)

    orders = Orders()

    for wait_cancel_order in wait_cancel_orders:
        order = orders.data.add()
        order.cl_ord_id = wait_cancel_order.get('cl_ord_id')
        order.account_id = wait_cancel_order.get('account_id')

    req = orders.SerializeToString()
    py_gmi_cancel_order(req)


def order_batch(order_infos, combine=False, account=''):
    """
    批量委托接口
    """
    orders = Orders()
    for order_info in order_infos:
        order_info['account_id'] = get_account_id(account)
        order = orders.data.add()
        [setattr(order, k, order_info[k]) for k in order_info]
        if context.is_backtest_model():
            order.created_at.seconds = datetime2timestamp(context.now)

    req = orders.SerializeToString()
    status, result = py_gmi_place_order(req)
    if c_status_fail(status, 'py_gmi_place_order'):
        return []

    if not result:
        return []

    res = Orders()
    res.ParseFromString(result)

    return [protobuf_to_dict(res_order, including_default_value_fields=True) for res_order in res.data]


def get_account_id(name_or_id):
    # type: (Text) ->Text
    for one in six.itervalues(context.accounts):
        if one.match(name_or_id):
            return one.id

    # 都没有匹配上, 等着后端去拒绝
    return name_or_id


def get_execution_reports():
    # type: () -> List[Dict[Text, Any]]
    """
    返回执行回报
    """
    reports = []
    for account in six.itervalues(context.accounts):
        req = GetExecrptsReq()
        req.account_id = account.id
        req = req.SerializeToString()
        status, result = py_gmi_get_execution_reports(req)
        if c_status_fail(status, 'py_gmi_get_execution_reports'):
            return []

        res = ExecRpts()
        res.ParseFromString(result)
        reports.extend([protobuf_to_dict(res_order, including_default_value_fields=True) for res_order in res.data])
    return reports
