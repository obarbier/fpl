from google.protobuf.json_format import Parse, ParseDict, MessageToJson
from google.protobuf import message as _message

def parse_dict(js_dict, message):
    ParseDict(js_dict=js_dict, message=message, ignore_unknown_fields=True)


def parseArray(text, message):
    Parse(text=text, message=message, ignore_unknown_fields=True)


def message_to_json(message):
    """Converts a message to JSON, using snake_case for field names."""
    return MessageToJson(message, preserving_proto_field_name=True)

def generateColumnDefsFromMessage(message: _message, response):
    for field in message.DESCRIPTOR.fields:
        try:
            c = response.columnDefs.add()
            c.headerName = field.name
            c.field = field.name
        except Exception as ex:
            print(ex)