from neomodel import config
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty, StructuredRel,
                      UniqueIdProperty, BooleanProperty, RelationshipFrom, RelationshipTo, db, config)
import functools
import typing
from protos.apiServices_pb2 import Team, node, Node, relationship, Relationships, Player
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


PROTOTYPE2NEO_MAPPING = {
    5: IntegerProperty(default=0),  # int32,
    1: IntegerProperty(default=0),  # int32,
    9: StringProperty(default=""),  # string
    8: BooleanProperty(default=False),  # bool
    11: None,  # Custom

    # CPPTYPE_BOOL = 7

    # CPPTYPE_DOUBLE = 5

    # CPPTYPE_ENUM = 8

    # CPPTYPE_FLOAT = 6

    # CPPTYPE_INT32 = 1

    # CPPTYPE_INT64 = 2

    # CPPTYPE_MESSAGE = 10

    # CPPTYPE_STRING = 9

    # CPPTYPE_UINT32 = 3

    # CPPTYPE_UINT64 = 4

    # FIRST_RESERVED_FIELD_NUMBER = 19000
}


def get_pb_enum_name(msg, field_name, enum_int):
    """Return the value for the enum name of a field,
       or None if the field does not exist, is not an enum, or the
       enum does not have a value with the supplied name."""
    field = msg.DESCRIPTOR.fields_by_name.get(field_name, None)
    if field and field.enum_type:
        enum = field.enum_type.values_by_number.get(enum_int, None)
        return enum.name


get_node_enum = functools.partial(
    get_pb_enum_name, Node, 'identity')
get_relationship_enum = functools.partial(
    get_pb_enum_name, Relationships, 'identity')


def node_creator(message):
    superclasses = tuple([StructuredNode])
    classname = get_node_enum(
        message.DESCRIPTOR.GetOptions().Extensions[node].identity)
    DESCRIPTOR = message.DESCRIPTOR
    fields_by_name = message.DESCRIPTOR.fields_by_name
    attributedict = {}
    for idx, (field_name, field_descriptor) in enumerate(fields_by_name.items()):
        if field_descriptor.type == 11:  # case when field is message and should be a Relationships by design
            rel = fields_by_name[field_name].GetOptions(
            ).Extensions[relationship]
            node_label = get_node_enum(rel.start)
            rel_label = get_relationship_enum(rel.labels)
            attributedict[field_name] = RelationshipFrom(node_label, rel_label)
        else:
            attributedict[field_name] = PROTOTYPE2NEO_MAPPING[field_descriptor.type]
    return type(classname, superclasses, attributedict)
