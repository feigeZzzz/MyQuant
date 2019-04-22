from typing import Text, Dict
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.message import Message
from google.protobuf.internal.containers import RepeatedScalarFieldContainer, RepeatedCompositeFieldContainer
from gm.pb.common_pb2 import Filter


# noinspection PyAbstractClass
class GetParametersReq(Message):
    filter = ...  # type: Filter
    owner_id = ...  # type: Text

    def __init__(self,
                 filter: Filter = None,
                 owner_id: Text = None,
                 ): ...


# noinspection PyAbstractClass
class DelParametersReq(Message):
    owner_id = ...  # type: Text
    keys = ...  # type: RepeatedScalarFieldContainer[Text]

    def __init__(self,
                 owner_id: Text,
                 keys: RepeatedScalarFieldContainer[Text],
                 ): ...


# noinspection PyAbstractClass
class GetSymbolsReq(Message):
    filter = ...  # type: Filter
    owner_id = ...  # type: Text

    def __init__(self,
                 filter: Filter = None,
                 owner_id: Text = None,
                 ): ...
