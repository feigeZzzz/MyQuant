from typing import Text, Dict
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.message import Message
from google.protobuf.internal.containers import RepeatedScalarFieldContainer, RepeatedCompositeFieldContainer
from gm.pb.common_pb2 import Filter


# noinspection PyAbstractClass
class GetAccountConnectionsReq(Message):
    filter = ...  # type: Filter
    account_ids = ...  # type:RepeatedScalarFieldContainer[Text]

    def __init__(self,
                 filter: Filter = None,
                 account_ids: RepeatedScalarFieldContainer[Text] = None
                 ): ...


# noinspection PyAbstractClass
class DelAccountConnectionsReq(Message):
    account_ids = ...  # type:RepeatedScalarFieldContainer[Text]

    def __init__(self,
                 account_ids: RepeatedScalarFieldContainer[Text] = None
                 ): ...


# noinspection PyAbstractClass
class GetAccountStatusesReq(Message):
    filter = ...  # type: Filter
    account_ids = ...  # type:RepeatedScalarFieldContainer[Text]

    def __init__(self,
                 filter: Filter = None,
                 account_ids: RepeatedScalarFieldContainer[Text] = None
                 ): ...


# noinspection PyAbstractClass
class SetAccountCumInoutReq(Message):
    account_id = ...  # type: Text
    cum_inout = ...  # type: float

    def __init__(self,
                 account_id: Text = None,
                 cum_inout: float = None,
                 ): ...
