from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher

from microservice import users, components


@dispatcher.add_method
def get_users(**kwargs):
    raven = components.get_raven()
    with components.get_riemann() as riemann:
        try:
            result = users.get_all()
        except Exception as e:
            raven.captureException(e)
            raise e

        riemann.event(service="microservice_users")
        return result


@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')
