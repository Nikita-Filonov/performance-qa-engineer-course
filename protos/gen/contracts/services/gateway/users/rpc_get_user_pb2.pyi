"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import contracts.services.users.user_pb2
import google.protobuf.descriptor
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class GetUserRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    id: builtins.str
    def __init__(
        self,
        *,
        id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["id", b"id"]) -> None: ...

global___GetUserRequest = GetUserRequest

@typing.final
class GetUserResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    USER_FIELD_NUMBER: builtins.int
    @property
    def user(self) -> contracts.services.users.user_pb2.User: ...
    def __init__(
        self,
        *,
        user: contracts.services.users.user_pb2.User | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["user", b"user"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["user", b"user"]) -> None: ...

global___GetUserResponse = GetUserResponse
