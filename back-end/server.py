from operator import is_
from unicodedata import is_normalized
import requests
import json
import dev_substrate_interface as dev
from Helper import Helper
from Staking import Staking
from Utils.chain_info import NETWORK_PROVIDER
from validators import Validators as validator
import requests
import json
import dev_substrate_interface as dev

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

@app.route('/api/request/dev/validator', methods=['POST'])
def get_recommended_validator():
    if request.method == 'POST':
        
        return_str = json.dumps(validator.recommend_validators(bond_amount=3.5))
        
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
        env = _request.get('env')
        provider = NETWORK_PROVIDER[_request.get('provider')]
        method = _request.get('method')
        staking = Staking(env=env, provider=provider)
        print('Data Received: {request}'.format(request=_request))
        result = Helper.request_staking_transaction(
                    request=_request, 
                    method=method, 
                    env=env,
                    staking=staking
                )
        return_tx_status = json.dumps(result)
        response = make_response(return_tx_status, 200)

        return response
    else:
        return make_response('Not supported method', 400)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)