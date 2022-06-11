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
        generic_call = self.api.compose_call(
            call_module=module,
            call_function=function,
            call_params=params
        )
        return generic_call
        
    def nominate(self, validators):

        '''
        Send Nominate extrinsic using users' key pair
        '''

        generic_call = self.get_generic_call(
            module="Staking",
            call_function="nominate",
            params={
                'targets': validators
            }
        )

        signed_extrinc = self.api.create_signed_extrinsic(
            call=generic_call,
            keypair= KEY_PAIR, # ToDo
        )

        try:
            self.api.submit_extrinsic(
                extrinsic=signed_extrinc,
            ) 
        except Exception as e:
            print("Error submitting extrinsic. Message: {error}".format(error=e))

if __name__ == "__main__":

    substrate = Substrate(url="wss://ws-api.substake.app").api
    metamask = MetaMask(provider="https://rpc.api.moonbase.moonbeam.network")
    metamask.delegate(
        collator_address="0x3937B5F83f8e3DB413bD202bAf4da5A64879690F",
        delegator_address="0x24E54d40c79dd99Ec626692C0AB58862A126A67b",
        delegate_amount=5,
    )


    
