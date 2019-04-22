from typing import Text, Dict
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.message import Message
from google.protobuf.internal.containers import RepeatedScalarFieldContainer, RepeatedCompositeFieldContainer


# noinspection PyAbstractClass
class RuntimeConfig(Message):
    owner_id = ...  # type: Text
    key = ...  # type: Text
    value = ...  # type: str
    name = ...  # type: Text
    intro = ...  # type: Text

    def __init__(self,
                 owner_id: Text = None,
                 key: Text = None,
                 value: str = None,
                 name: Text = None,
                 intro: Text = None,
                 ): ...


# noinspection PyAbstractClass
class Parameter(Message):
    key = ...  # type: Text
    value = ...  # type: float
    min = ...  # type: float
    max = ...  # type: float
    name = ...  # type: Text
    intro = ...  # type: Text
    group = ...  # type: Text
    readonly = ...  # type: bool

    def __init__(self,
                 key: Text = None,
                 value: float = None,
                 min: float = None,
                 max: float = None,
                 name: Text = None,
                 intro: Text = None,
                 group: Text = None,
                 readonly: bool = None
                 ): ...


# noinspection PyAbstractClass
class Parameters(Message):
    owner_id = ...  # type: Text
    parameters = ...  # type: RepeatedCompositeFieldContainer[Parameter]

    def __init__(self,
                 owner_id: Text = None,
                 parameters: RepeatedCompositeFieldContainer[Parameter] = None
                 ): ...


# noinspection PyAbstractClass
class Symbols(Message):
    owner_id = ...  # type: Text
    symbols = ...  # type: RepeatedScalarFieldContainer[Text]

    def __init__(self,
                 owner_id: Text = None,
                 symbols: RepeatedScalarFieldContainer[Text] = None
                 ): ...
