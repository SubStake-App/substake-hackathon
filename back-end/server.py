from operator import is_
from unicodedata import is_normalized
import requests
import json
import dev_substrate_interface as dev
from staking import Staking
from Utils.chain_info import NETWORK_PROVIDER

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
def request_stake():

    if request.method == 'POST':
        
        '''
        - env: 'EVM' or 'SUBSTRATE'
        - provider: 'NETWORK'
        '''

        _request = request.get_json()
        print('Data Received: {request}'.format(request=_request))

        env = _request.get('env')
        provider = NETWORK_PROVIDER[_request.get('provider')]
        staking = Staking(env=env, provider=provider)

        user_address = _request.get('userAddress')
        collator_address = _request.get('collatorAddress')
        validators = _request.get('validators')
        amount = _request.get('amount')
        payee = _request.get('payee')
        is_nominate = _request.get('isNominate') 
        is_pool = _request.get('isPool')
        pool_id = _request.get('poolId')

        return_tx_status = json.dumps(staking.stake(
            user_address=user_address,
            collator_address=collator_address,
            validators=validators,
            amount=amount,
            payee=payee,
            is_nominate=is_nominate,
            is_pool=is_pool,
            pool_id=pool_id,
        ))

        response = make_response(return_tx_status, 200)
        return response
    else:
        return make_response('Not supported method', 400)

@app.route('/api/request/dev/stake/more', methods=['POST'])
def request_stake_more():

    if request.method == 'POST':
        
        '''
        - env: 'EVM' or 'SUBSTRATE'
        - provider: 'NETWORK'
        '''

        _request = request.get_json()
        print('Data Received: {request}'.format(request=_request))

        env = _request.get('env')
        provider = NETWORK_PROVIDER[_request.get('provider')]
        staking = Staking(env=env, provider=provider)

        user_address = _request.get('userAddress')
        collator_address = _request.get('collatorAddress')
        more = _request.get('amount')
        is_pool = _request.get('isPool')

        return_tx_status = json.dumps(staking.stake_more(
            user_address=user_address,
            collator_address=collator_address,
            more=more,
            is_pool=is_pool,
        ))

        response = make_response(return_tx_status, 200)
        return response
    else:
        return make_response('Not supported method', 400)

@app.route('/api/request/dev/stake/less', methods=['POST'])
def request_stake_less():

    if request.method == 'POST':
        
        '''
        - env: 'EVM' or 'SUBSTRATE'
        - provider: 'NETWORK'
        '''

        _request = request.get_json()
        print('Data Received: {request}'.format(request=_request))

        env = _request.get('env')
        provider = NETWORK_PROVIDER[_request.get('provider')]
        staking = Staking(env=env, provider=provider)

        user_address = _request.get('userAddress')
        collator_address = _request.get('collatorAddress')
        less = _request.get('amount')

        return_tx_status = json.dumps(staking.stake_less(
            user_address=user_address,
            collator_address=collator_address,
            less=less,
        ))

        response = make_response(return_tx_status, 200)
        return response
    else:
        return make_response('Not supported method', 400)

@app.route('/api/request/dev/stake/again', methods=['POST'])
def request_stake_less():

    if request.method == 'POST':
        
        '''
        - env: 'EVM' or 'SUBSTRATE'
        - provider: 'NETWORK'
        '''

        _request = request.get_json()
        print('Data Received: {request}'.format(request=_request))

        env = _request.get('env')
        provider = NETWORK_PROVIDER[_request.get('provider')]
        staking = Staking(env=env, provider=provider)

        user_address = _request.get('userAddress')
        less = _request.get('amount')

        return_tx_status = json.dumps(staking.restake(
            user_address=user_address,
            less=less,
        ))

        response = make_response(return_tx_status, 200)
        return response
    else:
        return make_response('Not supported method', 400)

@app.route('/api/request/dev/stake/stop', methods=['POST'])
def request_stake_less():

    if request.method == 'POST':
        
        '''
        - env: 'EVM' or 'SUBSTRATE'
        - provider: 'NETWORK'
        '''

        _request = request.get_json()
        print('Data Received: {request}'.format(request=_request))

        env = _request.get('env')
        provider = NETWORK_PROVIDER[_request.get('provider')]
        staking = Staking(env=env, provider=provider)

        user_address = _request.get('userAddress')
        collator_address = _request.get('collatorAddress')

        return_tx_status = json.dumps(staking.stop_stake(
            user_address=user_address,
            collator_address=collator_address,
        ))

        response = make_response(return_tx_status, 200)
        return response
    else:
        return make_response('Not supported method', 400)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)