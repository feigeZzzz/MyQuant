from typing import Text, Dict
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.message import Message
from google.protobuf.internal.containers import RepeatedScalarFieldContainer, RepeatedCompositeFieldContainer
from gm.pb.account_pb2 import AccountStatus
from gm.pb.common_pb2 import Filter


# noinspection PyAbstractClass
class LoginReq(Message):
    account_id = ...  # type: Text
    account_name = ...  # type: Text
    password = ...  # type: Text
    captcha = ...  # type: Text
    properties = ...  # type: Dict[Text,Text]

    def __init__(self,
                 account_id: Text = None,
                 account_name: Text = None,
                 password: Text = None,
                 captcha: Text = None,
                 properties: Dict[Text, Text] = None,
                 ): ...


# noinspection PyAbstractClass
class LoginRsp(Message):
    account_id = ...  # type:Text
    token = ...  # type:Text
    status = ...  # type: AccountStatus

    def __init__(self,
                 account_id: Text = None,
                 token: Text = None,
                 status: AccountStatus = None,
                 ): ...


# noinspection PyAbstractClass
class LogoutReq(Message):
    account_id = ...  # type:Text
    properties = ...  # type: Dict[Text,Text]

    def __init__(self,
                 account_id: Text = None,
                 properties: Dict[Text, Text] = None,
                 ): ...


# noinspection PyAbstractClass
class LogoutRsp(Message):
    account_id = ...  # type: Text
    status = ...  # type: AccountStatus

    def __init__(self,
                 account_id: Text = None,
                 status: AccountStatus = None,
                 ): ...


# noinspection PyAbstractClass
class GetOrdersReq(Message):
    filter = ...  # type: Filter
    account_id = ...  # type: Text
    symbols = ...  # type: RepeatedScalarFieldContainer[Text]
    cl_ord_ids = ...  # type: RepeatedScalarFieldContainer[Text]
    properties = ...  # type: Dict[Text,Text]

    def __init__(self,
                 filter: Filter = None,
                 account_id: Text = None,
                 symbols: RepeatedScalarFieldContainer[Text] = None,
                 cl_ord_ids: RepeatedScalarFieldContainer[Text] = None,
                 properties: Dict[Text, Text] = None,
                 ): ...


# noinspection PyAbstractClass
class GetUnfinishedOrdersReq(Message):
    filter = ...  # type: Filter
    account_id = ...  # type: Text
    properties = ...  # type: Dict[Text,Text]

    def __init__(self,
                 filter: Filter = None,
                 account_id: Text = None,
                 properties: Dict[Text, Text] = None,
                 ): ...


# noinspection PyAbstractClass
class GetIntradayOrdersReq(Message):
    filter = ...  # type: Filter
    account_id = ...  # type: Text
    cl_ord_ids = ...  # type: RepeatedScalarFieldContainer[Text]
    properties = ...  # type: Dict[Text,Text]

    def __init__(self,
                 filter: Filter = None,
                 account_id: Text = None,
                 cl_ord_ids: RepeatedScalarFieldContainer[Text] = None,
                 properties: Dict[Text, Text] = None,
                 ): ...


# noinspection PyAbstractClass
class GetExecrptsReq(Message):
    filter = ...  # type: Filter
    account_id = ...  # type: Text
    cl_ord_id = ...  # type: Text
    exec_type = ...  # type: int
    properties = ...  # type: Dict[Text,Text]

    def __init__(self,
                 filter: Filter = None,
                 account_id: Text = None,
                 cl_ord_id: Text = None,
                 exec_type: int = None,
                 properties: Dict[Text, Text] = None,
                 ): ...


# noinspection PyAbstractClass
class GetIntradayExecrptsReq(Message):
    filter = ...  # type: Filter
    account_id = ...  # type: Text
    exec_type = ...  # type: int
    properties = ...  # type: Dict[Text,Text]

    def __init__(self,
                 filter: Filter = None,
                 account_id: Text = None,
                 exec_type: int = None,
                 properties: Dict[Text, Text] = None,
                 ): ...


# noinspection PyAbstractClass
class GetCashReq(Message):
    filter = ...  # type: Filter
    account_id = ...  # type: Text
    properties = ...  # type: Dict[Text,Text]

    def __init__(self,
                 filter: Filter = None,
                 account_id: Text = None,
                 properties: Dict[Text, Text] = None,
                 ): ...


# noinspection PyAbstractClass
class GetPositionsReq(Message):
    filter = ...  # type: Filter
    account_id = ...  # type: Text
    symbol = ...  # type: Text
    side = ...  # type: Text
    properties = ...  # type: Dict[Text,Text]

    def __init__(self,
                 filter: Filter = None,
                 account_id: Text = None,
                 symbol: Text = None,
                 side: Text = None,
                 properties: Dict[Text, Text] = None,
                 ): ...


# noinspection PyAbstractClass
class CancelAllOrdersReq(Message):
    account_ids = ...  # type: RepeatedScalarFieldContainer[Text]
    properties = ...  # type: Dict[Text,Text]

    def __init__(self,
                 account_ids: RepeatedScalarFieldContainer[Text] = None,
                 properties: Dict[Text, Text] = None,
                 ): ...


# noinspection PyAbstractClass
class CloseAllPositionsReq(Message):
    account_ids = ...  # type: RepeatedScalarFieldContainer[Text]
    properties = ...  # type: Dict[Text,Text]

    def __init__(self,
                 account_ids: RepeatedScalarFieldContainer[Text] = None,
                 properties: Dict[Text, Text] = None,
                 ): ...


# noinspection PyAbstractClass
class GetAccountStatusReq(Message):
    account_id = ...  # type:Text
