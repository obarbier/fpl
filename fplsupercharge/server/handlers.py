from fplsupercharge.protos.apiServices_pb2 import (
    ApiServices,
    ListTeams, rpc)


def _listTeams(request):
    """Return a list of team"""
    return {}


def _not_implemented():
    # response = Response()
    # response.status_code = 404
    # return response
    pass


HANDLERS = {
    # Tracking Server APIs
    ListTeams: _listTeams
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
