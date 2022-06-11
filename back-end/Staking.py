
from substrateinterface import SubstrateInterface, Keypair
from web3 import Web3
import json
from helper import Helper

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

    def __init__(self, provider):
        try:
            self.api = SubstrateInterface(url=provider)
        except Exception as e:
            print("Error connecting local node. Message: {error}".format(error=e))
            return 0
    
    def bond(self, user_account, amount, payee):

        '''
        Send bond extrinsic using user's key pair
        
        Params
        - user_account(controller): address of user
        - amount: bond amount
        - payee: Staked(auto-compound) / Stash(Reward goes to stash account)
        '''
        generic_call = Helper.get_generic_call(
            module="Staking",
            function="bond",
            params={
                'controller': user_account.ss58_address,
                'value': amount,
                'payee': payee
            }
        )
        Helper.send_extrinsic(
            api=self.api,
            generic_call=generic_call,
            user_account=user_account    
        )

    def nominate(self, user_account, validators):

        '''
        Send Nominate extrinsic using user's key pair

        Params
        - validators: [address of Validators]
        '''

        generic_call = Helper.get_generic_call(
            module="Staking",
            function="nominate",
            params={
                'targets': validators
            }
        )
        Helper.send_extrinsic(
            api=self.api,
            generic_call=generic_call,
            user_account=user_account    
        )

    def bond_extra(self, user_account, additional): 
        
        '''
        1. Send bond extra extrinsic using user's key pair
        2. Call "putInFrontof" extrinsic to adjust user's bag position
        
        Params
        - additional: bond extra amount. 'Int'
        '''
        generic_call = Helper.get_generic_call(
            module="Staking",
            function="bondExtra",
            params={
                'max_additional': additional
            }
        )
        Helper.send_extrinsic(
            api=self.api,
            generic_call=generic_call,
            user_account=user_account    
        )
        self.put_in_front_of(substrate_account="") # TO-DO 

    def unbond(self, user_account, amount):
        '''
        Send unbond extrinsic using user's key pair

        Params
        - amount: unbond amount. 'Int'
        '''
        generic_call = Helper.get_generic_call(
            module="Staking",
            function="unbond",
            params={
                'value': amount
            }
        )
        Helper.send_extrinsic(
            api=self.api,
            generic_call=generic_call,
            user_account=user_account    
        )

    def rebond(self, user_account, amount):
        '''
        Send rebond extrinsic using user's key pair

        Params
        - amount: unbond amount. 'Int'
        '''
        generic_call = Helper.get_generic_call(
            module="Staking",
            function="rebond",
            params={
                'value': amount
            }
        )
        Helper.send_extrinsic(
            api=self.api,
            generic_call=generic_call,
            user_account=user_account    
        )

    def put_in_front_of(self, user_account):
        
        '''
        Dispat call of "Bag-list" Pallet.

        Params
        - lighter: address of whose point is lighter than user's
        '''

        (user_score, list_head) = self._get_list_head(substrate_account=user_account)
        curr_node = list_head;
        score = self._get_score(node=curr_node);

        if user_score > score: 
            print("Put user node in front of {curr_node}".format(curr_node=curr_node))
            return curr_node
        
        while True :
            if user_score > score:
                print("Put user node in front of {curr_node}".format(curr_node=curr_node))
                break

            curr_node = self._get_next(curr_node)
            score = self._get_score(curr_node)

        generic_call = Helper.get_generic_call(
            module="VoterList",
            function="putInFrontOf",
            params={
                'lighter': curr_node
            }
        )
        Helper.send_extrinsic(
            api=self.api,
            generic_call=generic_call,
            user_account=user_account    
        )

    def _get_list_head(self, substrate_account):
        
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

    def _get_score(self, node):
        return self.api.query('VoterList', 'ListNodes', params=[node]).value['score']

    def _get_next(self, node):
        return self.api.query('VoterList', 'ListNodes', params=[node]).value['next']


if __name__ == "__main__":

    substrate = Substrate(provider="wss://ws-api.substake.app")
    # This account is only for test
    # No worry for hacking
    mnemonic = "seminar outside rack viable away limit tunnel marble category witness parrot eager"
    key_pair = Keypair.create_from_mnemonic(mnemonic=mnemonic)
    substrate.rebond(
        user_account=key_pair,
        amount=1000000000000,
    )
    


    
