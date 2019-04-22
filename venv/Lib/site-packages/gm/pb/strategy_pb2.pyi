from typing import Text, Dict
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.message import Message
from google.protobuf.internal.containers import RepeatedScalarFieldContainer, RepeatedCompositeFieldContainer
from gm.pb.common_pb2 import Property, ConnectionStatus


# noinspection PyAbstractClass
class Strategy(Message):
    Stage_Unknown = 0
    Stage_Backtest = 1
    Stage_Simulation = 2
    Stage_Live = 3

    Type_Default = 0
    Type_Scanner = 1
    Type_External = 2

    strategy_id = ...  # type: Text
    name = ...  # type: Text
    intro = ...  # type: Text
    language = ...  # type: Text
    stage = ...  # type: int
    strategy_type = ...  # type: int
    properties = ...  # type: Dict[Text, RepeatedCompositeFieldContainer[Property]]
    created_at = ...  # type: Timestamp
    updated_at = ...  # type: Timestamp

    def __init__(self,
                 strategy_id: Text = None,
                 name: Text = None,
                 intro: Text = None,
                 language: Text = None,
                 stage: int = None,
                 strategy_type: int = None,
                 properties: Dict[Text, RepeatedCompositeFieldContainer[Property]] = None,
                 created_at: Timestamp = None,
                 updated_at: Timestamp = None,
                 ): ...


# noinspection PyAbstractClass
class Strategies(Message):
    data = ...  # type: RepeatedCompositeFieldContainer[Strategy]

    def __init__(self, data: RepeatedCompositeFieldContainer[Strategy] = None): ...


# noinspection PyAbstractClass
class StrategyStatus(Message):
    strategy_id = ...  # type: Text
    status = ...  # type: ConnectionStatus

    def __init__(self, strategy_id: Text = None, status: ConnectionStatus = None): ...


# noinspection PyAbstractClass
class StrategyStatuses(Message):
    data = ...  # type: RepeatedCompositeFieldContainer[StrategyStatus]

    def __init__(self, data=RepeatedCompositeFieldContainer[StrategyStatus]): ...


# noinspection PyAbstractClass
class StopCommand(Message):
    strategy_id = ...  # type: Text
    reason = ...  # type: int
    reason_detail = ...  # type: Text

    def __init__(self,
                 strategy_id: Text = None,
                 reason: int = None,
                 reason_detail: Text = None,
                 ): ...


# noinspection PyAbstractClass
class StartCommand(Message):
    strategy_id = ...  # type: Text
    command = ...  # type: Text
    directory = ...  # type: Text
    path = ...  # type: Text
    interpreter_path = ...  # type: Text
    interpreter_venv_path = ...  # type: Text

    def __init__(self,
                 strategy_id: Text = None,
                 command: Text = None,
                 directory: Text = None,
                 path: Text = None,
                 interpreter_path: Text = None,
                 interpreter_venv_path: Text = None,
                 ): ...


# noinspection PyAbstractClass
class StartCommands(Message):
    data = ...  # type: RepeatedCompositeFieldContainer[StartCommand]

    def __init__(self, data: RepeatedCompositeFieldContainer[StartCommand] = None): ...
