from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class message(_message.Message):
    __slots__ = ["from_ip", "from_port", "to_ip", "to_port", "message", "hash", "timestamp"]
    FROM_IP_FIELD_NUMBER: _ClassVar[int]
    FROM_PORT_FIELD_NUMBER: _ClassVar[int]
    TO_IP_FIELD_NUMBER: _ClassVar[int]
    TO_PORT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    from_ip: str
    from_port: str
    to_ip: str
    to_port: str
    message: str
    hash: bytes
    timestamp: int
    def __init__(self, from_ip: _Optional[str] = ..., from_port: _Optional[str] = ..., to_ip: _Optional[str] = ..., to_port: _Optional[str] = ..., message: _Optional[str] = ..., hash: _Optional[bytes] = ..., timestamp: _Optional[int] = ...) -> None: ...

class Received_t(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
