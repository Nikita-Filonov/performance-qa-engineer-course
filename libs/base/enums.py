from enum import Enum
from typing import Self, TypeVar

from libs.base.strings import to_upper_snake_case

T = TypeVar('T')


class ProtoEnum(Enum):
    @classmethod
    def to_proto_map(cls, proto: type[T]) -> dict[Self, T]:
        proto_name = proto.DESCRIPTOR.name

        return {
            key: getattr(proto, proto_key)
            for proto_key in proto.keys()
            for key in cls
            if proto_key == f'{to_upper_snake_case(proto_name)}_{key.name}'
        }

    @classmethod
    def from_proto_map(cls, proto: type[T]) -> dict[T, Self]:
        return {value: key for key, value in cls.to_proto_map(proto).items()}
