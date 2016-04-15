import requests
import logging
import json

logger = logging.getLogger('satnogsclient')

class Jsonhandler:

    def post_json(self,url,payload):
        url = 'https://localhost:5000/notify'
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
        
    def get_json_str(self,payload):
        return json.dumps(payload)
        