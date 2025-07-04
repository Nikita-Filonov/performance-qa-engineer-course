"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _PaymentStatus:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _PaymentStatusEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_PaymentStatus.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    PAYMENT_STATUS_UNSPECIFIED: _PaymentStatus.ValueType  # 0
    PAYMENT_STATUS_AUTHORIZED: _PaymentStatus.ValueType  # 1
    PAYMENT_STATUS_CAPTURED: _PaymentStatus.ValueType  # 2
    PAYMENT_STATUS_REFUNDED: _PaymentStatus.ValueType  # 3
    PAYMENT_STATUS_DECLINED: _PaymentStatus.ValueType  # 4
    PAYMENT_STATUS_FAILED: _PaymentStatus.ValueType  # 5

class PaymentStatus(_PaymentStatus, metaclass=_PaymentStatusEnumTypeWrapper): ...

PAYMENT_STATUS_UNSPECIFIED: PaymentStatus.ValueType  # 0
PAYMENT_STATUS_AUTHORIZED: PaymentStatus.ValueType  # 1
PAYMENT_STATUS_CAPTURED: PaymentStatus.ValueType  # 2
PAYMENT_STATUS_REFUNDED: PaymentStatus.ValueType  # 3
PAYMENT_STATUS_DECLINED: PaymentStatus.ValueType  # 4
PAYMENT_STATUS_FAILED: PaymentStatus.ValueType  # 5
global___PaymentStatus = PaymentStatus

class _PaymentSystem:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _PaymentSystemEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_PaymentSystem.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    PAYMENT_SYSTEM_UNSPECIFIED: _PaymentSystem.ValueType  # 0
    PAYMENT_SYSTEM_MASTERCARD: _PaymentSystem.ValueType  # 1
    PAYMENT_SYSTEM_VISA: _PaymentSystem.ValueType  # 2

class PaymentSystem(_PaymentSystem, metaclass=_PaymentSystemEnumTypeWrapper): ...

PAYMENT_SYSTEM_UNSPECIFIED: PaymentSystem.ValueType  # 0
PAYMENT_SYSTEM_MASTERCARD: PaymentSystem.ValueType  # 1
PAYMENT_SYSTEM_VISA: PaymentSystem.ValueType  # 2
global___PaymentSystem = PaymentSystem

@typing.final
class Payment(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    SYSTEM_FIELD_NUMBER: builtins.int
    MESSAGE_FIELD_NUMBER: builtins.int
    id: builtins.str
    status: global___PaymentStatus.ValueType
    system: global___PaymentSystem.ValueType
    message: builtins.str
    def __init__(
        self,
        *,
        id: builtins.str = ...,
        status: global___PaymentStatus.ValueType = ...,
        system: global___PaymentSystem.ValueType = ...,
        message: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["id", b"id", "message", b"message", "status", b"status", "system", b"system"]) -> None: ...

global___Payment = Payment
