from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher

from microservice import users


@dispatcher.add_method
def get_users(**kwargs):
    return users.get_all()


@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')
