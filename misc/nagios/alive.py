#!/usr/bin/python3
import http.client
import json
import sys

connection = http.client.HTTPConnection('localhost', 8000)
headers = {'Content-type': 'application/json'}
json_rpc = {"jsonrpc": "2.0", "id": 1, "method": "get_users", "params": []}
json_request = json.dumps(json_rpc)

try:
    connection.request('POST', '/', json_request, headers)
    response = connection.getresponse()
except (http.client.HTTPException, ConnectionError):
    print('CRITICAL - cannot reach the server.')
    sys.exit(2)

try:
    json_response = json.loads(response.read().decode())
    if not len(json_response['result']):
        raise RuntimeError
except (ValueError, KeyError, RuntimeError):
    print('WARNING - cannot reach the server.')
    sys.exit(1)

print('OK - seems to be OK.')
sys.exit(0)
