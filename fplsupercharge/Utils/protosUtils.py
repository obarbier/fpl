from google.protobuf.json_format import Parse, ParseDict, MessageToJson


def parse_dict(js_dict, message):
    ParseDict(js_dict=js_dict, message=message, ignore_unknown_fields=True)


def parseArray(text, message):
    Parse(text=text, message=message, ignore_unknown_fields=True)


def message_to_json(message):
    """Converts a message to JSON, using snake_case for field names."""
    return MessageToJson(message, preserving_proto_field_name=True)
