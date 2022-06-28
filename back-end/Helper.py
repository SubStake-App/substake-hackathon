from user_info import get_user_info
from subprocess import call
from hexbytes import HexBytes

from Key import Key_Handler
from Utils.helpful_function import str_to_bool

from dev_substrate_interface import get_recommended_collators

class Helper:

    @staticmethod
    def request_asset_status(user_address, asset_manager, chain_info):
        if chain_info == 'westend' :
            return asset_manager.get_user_balance_status(user_address=user_address)
        elif chain_info == 'moonbase' :
            return asset_manager.get_user_balance_status_moonbase(user_address=user_address)
    

    @staticmethod
    def request_staking_transaction(request, method, env, staking):

        if method == 'stake':

            user_address = request.get('userAddress')
            amount = request.get('amount')
            collator_address = request.get('collatorAddress') if env == 'evm' else None
            validators = request.get('validators') if env == 'substrate' else None
            payee = request.get('payee') if env == 'substrate' else None
            is_nominate = request.get('isNominate') if env == 'substrate' else None
            is_both = request.get('isBoth') if env == 'substrate' else None
            is_pool = request.get('isPool') if env == 'substrate' else None
            pool_id = request.get('poolId') if env == 'substrate' and is_pool else None

            result = staking.stake(
                        user_address=user_address,
                        collator_address=collator_address,
                        validators=validators,
                        amount=amount,
                        payee=payee,
                        is_nominate=is_nominate,
                        is_both=is_both,
                        is_pool=is_pool,
                        pool_id=pool_id,
                    )

            return result

        elif method == 'stakeMore':

            user_address = request.get('userAddress')
            amount = request.get('amount')
            collator_address = request.get('collatorAddress') if env == 'evm' else None
            is_pool = request.get('isPool') if env == 'substrate' else None
            result = staking.stake_more(
                        user_address=user_address,
                        collator_address=collator_address,
                        amount=amount,
                        is_pool=is_pool,
                    )
            return result

        elif method == 'stakeLess':

            user_address = request.get('userAddress')
            amount = request.get('amount') 
            collator_address = request.get('collatorAddress') if env == 'evm' else None
            result = staking.stake_less(
                        user_address=user_address,
                        collator_address=collator_address,
                        amount=amount,
                    )

            return result

        elif method == 'reStake':

            user_address = request.get('userAddress') 
            amount = request.get('amount') 
            result = staking.restake(
                        user_address=user_address,
                        amount=amount,
                    )

            return result 

        elif method == 'stopStake':
            
            user_address = request.get('userAddress')
            collator_address = request.get('collatorAddress') if env == 'evm' else None

            result = staking.stop_stake(
                        user_address=user_address,
                        collator_address=collator_address,
                    )

            return result

    @staticmethod
    def request_curation(which, request, curator=None):

        if which == 'validators':

            is_curate = str_to_bool(request.get('is_curate'))
            if is_curate:
                bond_amount = float(request.get('bond_amount'))
                return curator.recommend_validators(bond_amount=bond_amount)
            else:
                return curator.get_active_validators(is_request=True)
        # elif which == 'collators':
        #     return_str = json.dumps(dev.get_recommended_collators())
        elif which == 'nomination_pool':
            
            return curator.get_nomination_pools()
        
        elif which == 'moonbase':
            return get_recommended_collators(float(request.get('amount')))

    @staticmethod
    def send_extrinsic(api, generic_call, user_address):
        '''
        Internal Function
        Take extrinsic call as parameter and send extrinsic with user's key-pair

        Params
        - generic_call: extrinc call from Substrate Interface. 
        - public_key: To get private key. DB[public_key] -> private_key
        - user_address: User's public address 
        Returns
        - (True/False, message)
        - Message: Extrinsic Hash/ Error
        '''
        mnemonic = get_user_info(user_address).get('private_key')
        key_pair = Key_Handler.substrate_mnemonic_to_keypair(mnemonic=mnemonic) 
        signed = api.create_signed_extrinsic(
            call=generic_call,
            keypair=key_pair, 
        )
        try:
            print("Submit Extrinsic")
            receipt = api.submit_extrinsic(extrinsic=signed, wait_for_inclusion=True)  
            if receipt.is_success:
                print('✅ Success')
                return ("Success", receipt.extrinsic_hash)
            else:
                print('⚠️ Extrinsic Failed: ', receipt.error_message)
                return ("Fail", receipt.error_message)
        except Exception as e:
            return ("Fail", e)

    @staticmethod
    def get_generic_call(api, module, function, params=None):

        '''
        Params
        - module: Name of Pallet. First word must be Capital letter.
        - function: Dispatch call of Pallet
        - params: Parameters of dipatch call. Form should be dictionary.
        '''
        generic_call = api.compose_call(
            call_module=module,
            call_function=function,
            call_params=params
        )
        return generic_call

    @staticmethod
    def eth_sign_transaction(api, tx_dict, user_address):
        
        private_key = get_user_info(user_address).get('private_key')
        try:
            print("Signing transaction...!")
            signed_tx = api.eth.account.sign_transaction(tx_dict, private_key)
        except Exception as e:
            return ("Fail", e)
        try: 
            print("Sending transaction...!")
            api.eth.send_raw_transaction(signed_tx.rawTransaction)
            print('Done..!')
            return ("Success", HexBytes.hex(signed_tx.hash))
        except Exception as e:
            return ("Fail", e)

    @staticmethod
    def reorder_bag_for(api, user_address):
        
        '''
        Method
        - Dispath call of "Bag-list" Pallet.
        - user_address: User's Substrate address

        Params
        - lighter: address of whose point is lighter than user's
        '''

        (user_score, list_head) = Helper._get_list_head(api=api, user_address=user_address)
        curr_node = list_head
        score = Helper._get_score(api=api, node=curr_node)

        if user_score > score: 
            print("Put user node in front of {curr_node}".format(curr_node=curr_node))
            return curr_node
        
        while True :
            if user_score > score:
                print("Put user node in front of {curr_node}".format(curr_node=curr_node))
                return curr_node

            curr_node = Helper._get_next(api, curr_node)
            score = Helper._get_score(api, curr_node)

    @staticmethod
    def _get_list_head(api, user_address):
        
        '''
        Method
        - Internal method
        - Get head of the bag-list

        Params
        - user_address: User's substrate account

        Returns
        - Tuple
        - user_score: Score of user. Int 
        - list_head: address of head. String
        '''

        list_node = api.query('VoterList', 'ListNodes', params=[user_address]).value
        user_score = list_node['score']
        user_bag_upper = list_node['bag_upper']
        list_bags = api.query('VoterList', 'ListBags', params=[user_bag_upper]).value
        list_head = list_bags['head']
        
        return (user_score, list_head)
    
    staticmethod
    def _get_score(api, node):
        
        '''
        Method
        - Internal method

        Params
        - node: current node address
        
        Returns
        - Int
        - score of node
        '''

        return api.query('VoterList', 'ListNodes', params=[node]).value['score']
    
    staticmethod
    def _get_next(api, node):
        
        '''
        Method
        - Internal method

        Params
        - node: current node

        Returns
        - String
        - Next node
        '''

        return api.query('VoterList', 'ListNodes', params=[node]).value['next']


if __name__ == '__main__':

    from substrateinterface import SubstrateInterface
    api = SubstrateInterface(url='wss://ws-api.substake.app')
    print(function)
    # lighter_node = Helper.reorder_bag_for(api=api, user_address='5C5iC1ueEsEUTeXwwrzVDRkJqAHK1LbVaBMS59QdxhpZ9TD5')
    # assert lighter_node == '5CM2Uev6jfUE6JV1LoCuzNXZikPwjCjTX3gFQPTxSi4iTnwg', "Wrong answer"

    # get_user_info(public_key='5F4djM7QZGXF5zsSoRhUYFi99bdEGGVa9QJTxni7mPnzZR3q')