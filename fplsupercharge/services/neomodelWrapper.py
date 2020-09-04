from neomodel import config
from google.protobuf import message as pbMessage
from protos.apiServices_pb2 import Team, node, Node, relationship, Relationships, Player
import typing
import functools
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty, StructuredRel,
                      UniqueIdProperty, BooleanProperty, RelationshipFrom, RelationshipTo, db, config)
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

# # node_creator(Team);
# class Datastore(object):
#     def __init__(self):
#         config.ENCRYPTED_CONNECTION = False
#         db.set_connection('bolt://fpl:abcd@0.0.0.0:7687')
#         self.PLAYER = node_creator(Player)
#         self.TEAM = node_creator(Team)
#     @classmethod
#     def create_team(cls, team_info):
#         t1 = cls().TEAM()
#         t1.name = "olvier"
#         t1.save()

# Datastore.create_team("test")

# t1 =  TEAM()
# t1.name = "olivier"