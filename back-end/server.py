import requests
import json
import dev_substrate_interface as dev
from staking import Staking

from flask import Flask, request, make_response, jsonify
app = Flask (__name__)

@app.route('/api/request/dev/collator', methods=['POST'])
def get_recommended_collator():
    if request.method == 'POST':
        
        """ for Ito.
        data = request.get_json()
        print('Data Received: "{data}"'.format(data=data))
        action = data.get('action')
        user_addresss = data.get('address')
        chain_name = data.get('chain-name')
        """
        return_str = json.dumps(dev.get_recommended_collators())
        
        response = make_response(return_str, 200)
        #print(return_str)
        return response
    else:
        return make_response("Not supported method", 400)


@app.route('/api/request/dev/stake', methods=['POST'])
def request_stake():
    if request.method == 'POST':
        _request = request.get_json()
        print('Data Received: {request}'.format(request=_request))
        env = _request.get('env')
        provider = _request.get('provider')
        is_pool = _request.get('is_pool') # if needed 

    else:
        return make_response('Not supported method', 400)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)