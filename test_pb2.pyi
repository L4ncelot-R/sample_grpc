from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class message(_message.Message):
    __slots__ = ["topic", "message"]
    class MessageEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: answers
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[answers, _Mapping]] = ...) -> None: ...
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    topic: str
    message: _containers.MessageMap[str, answers]
    def __init__(self, topic: _Optional[str] = ..., message: _Optional[_Mapping[str, answers]] = ...) -> None: ...

class subscription(_message.Message):
    __slots__ = ["ip", "port", "topic"]
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    ip: str
    port: str
    topic: str
    def __init__(self, ip: _Optional[str] = ..., port: _Optional[str] = ..., topic: _Optional[str] = ...) -> None: ...

class answers(_message.Message):
    __slots__ = ["answer"]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    answer: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, answer: _Optional[_Iterable[str]] = ...) -> None: ...

class Received_t(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
