from typing import Any

from google.protobuf.json_format import MessageToDict, MessageToJson
from google.protobuf.message import Message


def protobuf_to_dict(message: Message) -> dict[str, Any]:
    return MessageToDict(message, preserving_proto_field_name=True)


def protobuf_to_json(message: Message) -> str:
    return MessageToJson(message, preserving_proto_field_name=True)
