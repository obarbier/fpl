# # Static imports
# import functools
# import inspect
# # Third party imports
# from google.protobuf import message
# from uplink import converters, returns, json
# # local imports
# from fplsupercharge.converter import json_options, helpers
# from fplsupercharge.protos.apiServices_pb2 import Teams
# from fplsupercharge.Utils import protosUtils


# class ProtobuffConverter(converters.Factory):
#     __DECODING_STRATEGIES = {
#         returns.json: json_options.parse_json
#     }

#     __ENCODING_STRATEGIES = {
#         json: json_options.convert_message_to_dict
#     }

#     @staticmethod
#     def _get_content_by_type(cls, response):
#         """
#         :return: return content by type
#         """
#         msg = cls()
#         if inspect.isclass(cls) and issubclass(cls, Teams):
#             response = response.json()
#             for k, v in response.items():
#                 if k == "teams":
#                     for t in v:
#                         team = msg.team.add()
#                         protosUtils.parse_dict(t, team)
#                     return msg
#         else:
#             msg.ParseFromString(response)
#             return msg

#     @staticmethod
#     def is_protocol_buffer_class(cls):
#         """
#         Returns whether or not the given `cls` is a protobuf message
#         subclass.
#         """
#         return inspect.isclass(cls) and issubclass(cls, message.Message)

#     @staticmethod
#     def _get_strategy(cls, request_definition, strategies):
#         if not ProtobuffConverter.is_protocol_buffer_class(cls):
#             # Returning None tells Uplink's converter layer that we
#             # can't handle this type, so it can move on to the next
#             # factory.
#             return None

#         strategy_keys = tuple(strategies.keys())
#         method_annotations = request_definition.method_annotations

#         try:
#             key = helpers.get_first_of_type(method_annotations, strategy_keys)
#         except StopIteration:
#             raise KeyError
#         else:
#             target_strategy = strategies[type(key)]
#             return functools.partial(target_strategy, cls, request_definition)

#     # === END Helpers === #
#     def create_response_body_converter(self, cls, request_definition):
#         try:
#             return self._get_strategy(
#                 cls, request_definition, self.__DECODING_STRATEGIES
#             )
#         except KeyError:
#             # Return default callable that can decode Protobuf message
#             # from response content.
#             def converter(response):
#                 msg = self._get_content_by_type(cls, response)
#                 return msg

#             return converter

#     def create_request_body_converter(self, cls, request_definition):
#         try:
#             return self._get_strategy(
#                 cls, request_definition, self.__ENCODING_STRATEGIES
#             )
#         except KeyError:
#             # Return callable that can serialize Protobuf message.
#             def converter(msg):
#                 return msg.SerializeToString()

from fplsupercharge.services.neo4jServices import Datastore
import  logging
db = Datastore(uri="bolt://0.0.0.0:7687",username="fpl", password="abcd", logger=logging.getLogger())
print(db.get_oneTeamById(id=1))