
import string
from substrateinterface import SubstrateInterface 
from web3 import Web3
import json

KEY_PAIR = None
MOONBEAM_STAKING_CONTRACT = "0x0000000000000000000000000000000000000800"
MOONBEAM_STAKING_DECIMALS = 18
PRIVATE_KEY = ""

class MetaMask:

    def __init__(self, provider):
        try:
            self.web3 = Web3(Web3.HTTPProvider(provider))
        except Exception as e:
            print("Error connecting socket. Message: {error}".format(error=e))
            return 0

        file = open("Utils/moonbeam_abi.json")
        MOONBEAM_STAKING_ABI = json.load(file)
        self.contract = self.web3.eth.contract(
            address=MOONBEAM_STAKING_CONTRACT, 
            abi=MOONBEAM_STAKING_ABI
        )
        
    def delegate(
        self, 
        collator_address, 
        delegator_address,
        delegate_amount, 
    ):
        nonce = self.web3.eth.get_transaction_count(delegator_address)
        candidate_delgation_count = self.contract.functions.candidate_delegation_count(collator_address).call()
        delegator_delegation_count = self.contract.functions.delegator_delegation_count(delegator_address).call()
        tx_dict = self.contract.functions.delegate(
            collator_address,
            delegate_amount,
            candidate_delgation_count,
            delegator_delegation_count
        ).buildTransaction()
        tx_dict['nonce'] = nonce
        tx_dict['from'] = delegator_address
        signed_tx = self.web3.eth.account.sign_transaction(tx_dict, PRIVATE_KEY)
        self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)


class Substrate:

    def __init__(self, url):
        try:
            self.api = SubstrateInterface(url=url)
        except Exception as e:
            print("Error connecting local node. Message: {error}".format(error=e))
            return 0
            
    def get_generic_call(self, module, function, params=None):

        '''
        Params
        - module: Name of Pallet. First word must be Capital letter.
        - function: Dispatch call of Pallet
        - params: Parameters of dipatch call. Form should be dictionary.
        '''
        generic_call = self.api.compose_call(
            call_module=module,
            call_function=function,
            call_params=params
        )
        return generic_call

    def send_extrinsic(self, generic_call):

        '''
        Take extrinsic call as parameter and send extrinsic with user's key-pair

        Params
        - generic_call: extrinc call from Substrate Interface. 
        '''
        
        signed = self.api.create_signed_extrinsic(
            call=generic_call,
            keypair=KEY_PAIR, # ToDo
        )
        try:
            self.api.submit_extrinsic(
                extrinsic=signed,
            ) 
        except Exception as e:
            print("Error submitting extrinsic. Message: {error}".format(error=e))
    
    def bond(self, user_account, amount):

        '''
        Send bond extrinsic using user's key pair
        
        Params
        - user_account(controller): address of user
        - amount: bond amount
        '''
        generic_call = self.get_generic_call(
            module="Staking",
            call_function="bond",
            params={
                'controller': user_account,
                'value': amount
            }
        )
        self.send_extrinsic(generic_call=generic_call)

    def nominate(self, validators):

        '''
        Send Nominate extrinsic using user's key pair

        Params
        - validators: [address of Validators]
        '''

        generic_call = self.get_generic_call(
            module="Staking",
            call_function="nominate",
            params={
                'targets': validators
            }
        )
        self.send_extrinsic(generic_call=generic_call)

    def bond_extra(self, additional): 
        
        '''
        1. Send bond extra extrinsic using user's key pair
        2. Call "putInFrontof" extrinsic to adjust user's bag position
        
        Params
        - additional: bond extra amount. 'Int'
        '''
        generic_call = self.get_generic_call(
            module="Staking",
            call_function="bondExtra",
            params={
                'max_additional': additional
            }
        )
        self.send_extrinsic(generic_call=generic_call)
        self.put_in_front_of(substrate_account="") # TO-DO 

    def unbond(self, amount):
        '''
        Send unbond extrinsic using user's key pair

        Params
        - amount: unbond amount. 'Int'
        '''
        generic_call = self.get_generic_call(
            module="Staking",
            call_function="unbond",
            params={
                'value': amount
            }
        )
        self.send_extrinsic(generic_call=generic_call)

    def put_in_front_of(self, substrate_account):
        
        '''
        Dispat call of "Bag-list" Pallet.

        Params
        - lighter: address of whose point is lighter than user's
        '''

        (user_score, list_head) = self.get_list_head(substrate_account=substrate_account)
        curr_node = list_head;
        score = self.get_score(node=curr_node);

        if user_score > score: 
            print("Put user node in front of {curr_node}".format(curr_node=curr_node))
            return curr_node
        
        while True :
            if user_score > score:
                print("Put user node in front of {curr_node}".format(curr_node=curr_node))
                break

            curr_node = self.get_next(curr_node)
            score = self.get_score(curr_node)

        generic_call = self.get_generic_call(
            module="VoterList",
            call_function="putInFrontOf",
            params={
                'lighter': curr_node
            }
        )
        self.send_extrinsic(generic_call=generic_call)

    def get_list_head(self, substrate_account):
        
        '''
        Get head of the bag-list

        Params
        - substrate_account: User's substrate account
        '''
        
        list_node = self.api.query('VoterList', 'ListNodes', params=[substrate_account]).value
        user_score = list_node['score']
        user_bag_upper = list_node['bag_upper']
        list_bags = self.api.query('VoterList', 'ListBags', params=[user_bag_upper]).value
        list_head = list_bags['head']
        
        return (user_score, list_head)

    def get_score(self, node):
        return self.api.query('VoterList', 'ListNodes', params=[node]).value['score']

    def get_next(self, node):
        return self.api.query('VoterList', 'ListNodes', params=[node]).value['next']


if __name__ == "__main__":

    substrate = Substrate(url="wss://ws-api.substake.app")
    substrate.put_in_front_of(substrate_account="5C5iC1ueEsEUTeXwwrzVDRkJqAHK1LbVaBMS59QdxhpZ9TD5")
    


    
