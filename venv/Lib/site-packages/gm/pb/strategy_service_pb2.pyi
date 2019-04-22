from typing import Text, Dict
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.message import Message
from google.protobuf.internal.containers import RepeatedScalarFieldContainer, RepeatedCompositeFieldContainer
from gm.pb.common_pb2 import Filter


# noinspection PyAbstractClass
class SetAccountsReq(Message):
    strategy_id = ...  # type: Text
    stage = ...  # type: int
    account_ids = ...  # type: RepeatedScalarFieldContainer[Text]

    def __init__(self,
                 strategy_id: Text = None,
                 stage: int = None,
                 account_ids: RepeatedScalarFieldContainer[Text] = None,
                 ): ...


# noinspection PyAbstractClass
class GetAccountsReq(Message):
    strategy_id = ...  # type: Text
    stage = ...  # type: int

    def __init__(self,
                 strategy_id: Text = None,
                 stage: int = None,
                 ): ...


# noinspection PyAbstractClass
class GetAccountsRsp(Message):
    account_ids = ...  # type: RepeatedScalarFieldContainer[Text]

    def __init__(self, account_ids: RepeatedScalarFieldContainer[Text] = None): ...


# noinspection PyAbstractClass
class GetStrategiesToAccountReq(Message):
    account_id = ...  # type:Text

    def __init__(self, account_id: Text = None): ...


# noinspection PyAbstractClass
class GetStrategiesReq(Message):
    filter = ...  # type: Filter
    strategy_ids = ...  # type: RepeatedScalarFieldContainer[Text]

    def __init__(self, filter: Filter = None, strategy_ids: RepeatedScalarFieldContainer[Text] = None): ...


# noinspection PyAbstractClass
class GetStrategiesOfStageReq(Message):
    filter = ...  # type: Filter
    stages = ...  # type: RepeatedScalarFieldContainer[int]

    def __init__(self,
                 filter: Filter = None,
                 stages: RepeatedScalarFieldContainer[int] = None
                 ): ...


# noinspection PyAbstractClass
class DelStrategiesReq(Message):
    strategy_ids = ...  # type: RepeatedScalarFieldContainer[Text]

    def __init__(self, strategy_ids: RepeatedScalarFieldContainer[Text] = None): ...


# noinspection PyAbstractClass
class GetStartCommandsReq(Message):
    filter = ...  # type: Filter
    strategy_ids = ...  # type: RepeatedScalarFieldContainer[Text]

    def __init__(self,
                 filter: Filter = None,
                 strategy_ids: RepeatedScalarFieldContainer[Text] = None
                 ): ...


# noinspection PyAbstractClass
class GetStrategyStatusesReq(Message):
    filter = ...  # type: Filter
    strategy_ids = ...  # type: RepeatedScalarFieldContainer[Text]

    def __init__(self,
                 filter: Filter = None,
                 strategy_ids: RepeatedScalarFieldContainer[Text] = None
                 ): ...


# noinspection PyAbstractClass
class GetStrategyLogsReq(Message):
    filter = ...  # type: Filter
    strategy_id = ...  # type: Text

    def __init__(self,
                 filter: Filter = None,
                 strategy_id: Text = None,
                 ): ...
