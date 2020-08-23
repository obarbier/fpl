from flask import Response, g , request
from fplsupercharge.protos.apiServices_pb2 import (
    ApiServices,
    ListTeams,
    ListOneTeam, rpc)
from fplsupercharge.utils.protosUtils import message_to_json
from querystring_parser import parser


def _listTeams():
    """Return a list of team"""
    listTeams = ListTeams()
    resp = listTeams.Response()
    resp.team.MergeFrom(g.db.get_teams())
    response = Response(mimetype="application/json")
    response.set_data(message_to_json(resp))
    return response


def _listOneTeam():
    # listOneTeam = ListOneTeam()
    query_string = request.query_string.decode("utf-8")
    request_dict = parser.parse(query_string, normalized=True)
    print(g.db.get_oneTeam(request_dict))
    return {}, 200


def _not_implemented():
    response = Response()
    response.status_code = 404
    return response


HANDLERS = {
    # Tracking Server APIs
    ListTeams: _listTeams,
    ListOneTeam: _listOneTeam

}


def _get_paths(base_path):
    return ['/api/2.0{}'.format(base_path)]


def get_handler(request_class):
    """
    :param request_class: The type of protobuf message
    :return:
    """
    return HANDLERS.get(request_class,
                        _not_implemented)


def get_endpoints():
    """
    :return: List of tuples (path, handler, methods)
    """

    def get_service_endpoints(service):
        ret = []
        for service_method in service.DESCRIPTOR.methods:
            endpoints = service_method.GetOptions(
            ).Extensions[rpc].endpoints
            for endpoint in endpoints:
                for http_path in _get_paths(endpoint.path):
                    handler = get_handler(
                        service().GetRequestClass(service_method))
                    ret.append((http_path, handler, [endpoint.method]))
        return ret

    return get_service_endpoints(ApiServices)
