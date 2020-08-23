import logging
import inspect
from google.protobuf.json_format import Parse, ParseDict, MessageToJson
from google.protobuf import message as pbMessage
from google.protobuf.pyext import _message as pbPyMessage


def isProtoMessage(test):
    return inspect.isclass(test) and issubclass(test,
                                                pbMessage.Message)


def isProtoScalarMapContainer(test):
    return inspect.isclass(test) and isinstance(test,
                                                pbPyMessage.ScalarMapContainer)


def parse_dict(js_dict, message):
    ParseDict(js_dict=js_dict, message=message, ignore_unknown_fields=True)


def dict_to_map(dict, message):
    for k, v in dict.items():
        message[k] = v


def parse_list(values, message):
    '''parse list to protobuf message'''
    if isinstance(values[0], dict):  # value needs to be further parsed
        for v in values:
            cmd = message.add()
            parse_dict(v, cmd)
    else:  # value can be set
        message.extend(values)


def parse_dict(values, message):
    for k, v in values.items():
        if isinstance(message, pbMessage.Message):
            if isinstance(v, dict):  # value needs to be further parsed
                parse_dict(v, getattr(message, k))
            elif isinstance(v, list):
                parse_list(v, getattr(message, k))
            else:  # value can be set
                try:
                    setattr(message, k, v)
                except AttributeError:
                    print(
                        'try to access invalid attributes {}.{} = {}'.format(
                            message, k, v))
        elif isinstance(message, pbPyMessage.ScalarMapContainer):
            for key, val in values.items():
                message[key] = val
        elif isinstance(message, pbPyMessage.MessageMapContainer):
            for key, d in values.items():
                parse_dict(d, message[k])


def dict_to_protobuf(value, message):
    parse_dict(value, message)


def parseArray(text, message):
    Parse(text=text, message=message, ignore_unknown_fields=True)


def message_to_json(message):
    """Converts a message to JSON, using snake_case for field names."""
    return MessageToJson(message, preserving_proto_field_name=True)


def generateColumnDefsFromMessage(message, response):
    for field in message.DESCRIPTOR.fields:
        try:
            c = response.columnDefs.add()
            c.headerName = field.name
            c.field = field.name
        except Exception as ex:
            print(ex)
