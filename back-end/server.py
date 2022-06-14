from operator import is_
from unicodedata import is_normalized
import requests
import json
import dev_substrate_interface as dev
from helper import Helper

from flask import Flask, request, make_response, jsonify
app = Flask (__name__)

@app.route('/api/request/dev/collator', methods=['POST'])
def get_recommended_collator():
    if request.method == 'POST':

        return_str = json.dumps(dev.get_recommended_collators())
        
        response = make_response(return_str, 200)
        #print(return_str)
        return response
    else:
        return make_response("Not supported method", 400)


@app.route('/api/request/dev/stake', methods=['POST'])
def request_staking_transaction():

    if request.method == 'POST':
        
        '''
        request = {
            'env' : 'evm' / 'substrate'
            'provider': 'moonbase' / 'westend'
            'method': 'stake' / 'stakeMore' / 'stakeLess' / 'reStake' / 'stopStake'
        }
        '''

        _request = request.get_json()
        print('Data Received: {request}'.format(request=_request))
        result = Helper.request_staking_transaction(request=_request)
        return_tx_status = json.dumps(result)
        response = make_response(return_tx_status, 200)

        return response
    else:
        return make_response('Not supported method', 400)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)