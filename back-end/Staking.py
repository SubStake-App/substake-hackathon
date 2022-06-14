

from substrateinterface import SubstrateInterface, Keypair
from web3 import Web3
from helper import Helper
import json

KEY_PAIR = None
EVM_CONTRACT = "0x0000000000000000000000000000000000000800"
EVM_DECIMALS = 18
SUBSTRATE_DECIMALS = 12
PRIVATE_KEY = ""

class Staking:

    '''
    Class
    - Staking class contains EVM/Substrate class
    '''

    def __init__(self, env=None, provider=None):
        
        assert env is not None, "SUBSTAKE-STAKING: Environment must be provided"
        assert provider is not None, "SUBSTAKE_STAKING: Provider must be provided"

        if env == 'evm':
            self.evm = EVM(provider=provider)
            self.name = 'evm'
        elif env == 'substrate':
            self.substrate = Substrate(provider=provider)
            self.name = 'substrate'

    def stake(
        self, 
        user_address=None, 
        collator_address=None, 
        validators=None,
        amount=None, 
        payee=None,
        is_nominate=None,
        is_pool=None,
        pool_id=None,
    ):

        '''
        Method
        - EVM: delegate
        - Substrate: bond

        Params
        - user_address: Public address of user. String
        - collator_address: For EVM, address of collator. String
        - validators: For Substrate, list of address of validators. [String]
        - amount: Staking amount. Int
        - payee: For Substrate, 'Staked' or 'Stash'
        - is_nominate: For Substrate, if already bonds 'True'. Default: 'False' 
        - is_pool: If user stakes to nomination pool, set to 'True'
        - pool_id: Pool id for nomination pool
        '''

        assert user_address is not None, "SUBSTAKE-STAKING(STAKE): User address must be provided"
        assert amount is not None, "SUBSTAKE-STAKING(STAKE): Amount must be provided"
        amount = int(amount)

        if self.name == 'evm':
            
            assert collator_address is not None, "SUBSTAKE-STAKING(STAKE): Collator address must be provided for EVM"
            amount = amount * 10**EVM_DECIMALS

            (is_success, message) = self.evm.delegate(
                                        user_address=user_address, 
                                        collator_address=collator_address, 
                                        amount=amount
                                    )
            return {'Transaction Status': is_success, 'Message': message}

        elif self.name == 'substrate':
            
            assert is_nominate is not None, "SUBSTAKE-STAKING(STAKE): Is_nominate must be provided"
            assert is_pool is not None, "SUBSTAKE-STAKING(STAKE): Is_pool must be provided"

            if is_nominate: 

                assert validators is not None, "SUBSTAKE-STAKING(STAKE): Validators must be provided for Substrate"

                (is_success, message) = self.substrate.nominate(
                                            user_address=user_address,
                                            validators=validators
                                        )
                return {'Transaction Status': is_success, 'Message': message}
            else:
                amount = amount * 10**SUBSTRATE_DECIMALS

                if is_pool:
                    assert pool_id is not None, "SUBSTAKE-STAKING(STAKE): Pool id must be provided for Substrate"
                    pool_id = int(pool_id)

                    (is_success, message) = self.substrate.bond(
                                                user_address=user_address,
                                                amount=amount,
                                                is_pool=is_pool,
                                                pool_id=pool_id
                                            )
                    return {'Transaction Status': is_success, 'Message': message}
                else:
                    assert payee is not None, "SUBSTAKE-STAKING(STAKE): Payee must be provided for Substrate"
                    (is_success, message) = self.substrate.bond(
                                                user_address=user_address,
                                                amount=amount,
                                                payee=payee
                                            )
                    return {'Transaction Status': is_success, 'Message': message}
    
    def stake_more(
        self, 
        user_address=None, 
        collator_address=None,
        amount=None, 
        is_pool=None
    ):

        '''
        Method
        - Send stake-more-asset transaction
        
        Params
        - user_address: Whose asset
        - more: additional asset
        - collator_address: Only needed in EVM
        '''

        assert user_address is not None, "SUBSTKAE-STAKING(STAKE MORE): User address must be provided"
        assert amount is not None, "SUBSTAKE-STAKING(STAKE MORE): More should be provided"
        amount = int(amount)

        if self.name == 'evm':
            assert collator_address is not None, "SUBSTAKE-STAKING(STAKE MORE): Collator address must be provided"
            more = more * 10**EVM_DECIMALS

            (is_success, message) = self.evm.bond_more(
                                        user_address=user_address,
                                        collator_address=collator_address,
                                        amount=amount
                                    )
            return {'Transaction Status': is_success, 'Message': message}

        elif self.name == 'substrate':
            
            assert is_pool is not None, "SUBSTAKE-STAKING(STAKE MORE): Is_pool must be provided"
            amount = amount * 10**SUBSTRATE_DECIMALS

            (is_success, message) = self.substrate.bond_extra(
                                        user_address=user_address,
                                        amount=amount,
                                        is_pool=is_pool
                                    )
            return {'Transaction Status': is_success, 'Message': message}

    def stake_less(
        self, 
        user_address=None, 
        collator_address=None,
        amount=None, 
    ):

        assert user_address is not None, "SUBSTAKE-STAKING(STAKE LESS): User address must be provided"
        assert amount is not None, "SUBSTAKE-STAKING(STAKE LESS): Less must be provided"
        amount = int(amount)

        if self.name == 'evm':
            assert collator_address is not None, "SUBSTAKE-STAKING(STAKE LESS): Collator address must be provided for EVM"
            less = less * 10**EVM_DECIMALS

            (is_success, message) = self.evm.bond_less(
                                        user_address=user_address,
                                        collator_address=collator_address,
                                        amount=amount
                                    )

            return {'Transaction Status': is_success, 'Message': message}

        elif self.name == 'substrate':
            less = less * 10**SUBSTRATE_DECIMALS
            (is_success, message) = self.substrate.unbond(
                                        user_address=user_address,
                                        amount=amount
                                    )

            return {'Transaction Status': is_success, 'Message': message}

    def restake(
        self, 
        user_address=None, 
        amount=None
    ):
        
        assert user_address is not None, "SUBSTAKE-STAKING(RESTAKE): User address should be provided"
        assert amount is not None, "SUBSTAKE-STAKING(RESTAKE): Amount shoud be provided"
        amount = int(amount)

        if self.name == 'evm':
            pass
        elif self.name == 'substrate':
            amount = amount * 10**SUBSTRATE_DECIMALS
            (is_success, message) = self.substrate.rebond(
                                        user_address=user_address, 
                                        amount=amount
                                    )
            return {'Transaction Status': is_success, 'Message': message}

    def stop_stake(
        self, 
        user_address=None, 
        collator_address=None
    ):

        '''
        Method
        - Pull all staked asset

        Params 
        - user_address: Whose asset
        - collator_address: Only needed in EVM(Moonbeam)
        '''
        assert user_address is not None, "SUBSTAKE-STAKING(STOP STAKE): User address must be provided"

        if self.name == 'evm':
            assert collator_address is not None, "SUBSTAKE-STAKING(STOP STAKE): Collator address must be provided"
            (is_success, message) = self.evm.revoke(
                                        user_address=user_address, 
                                        collator_address=collator_address
                                    )
            return {'Transaction Status': is_success, 'Message': message}

        elif self.name == 'substrate':
            (is_success, message) = self.substrate.chill(user_address=user_address)
            return {'Transaction Status': is_success, 'Message': message}

class EVM:

    def __init__(self, provider):

        try:
            self.web3 = Web3(Web3.HTTPProvider(provider))
        except Exception as e:
            print("Error connecting socket. Message: {error}".format(error=e))
            return 0

        file = open("Utils/moonbeam_abi.json")
        MOONBEAM_STAKING_ABI = json.load(file)
        self.contract = self.web3.eth.contract(
            address=EVM_CONTRACT, 
            abi=MOONBEAM_STAKING_ABI
        )
        
    def delegate(self, user_address, collator_address, amount):

        '''
        Method
        - Send delegate tranasction

        Params 
        - collator_address: Whom to delegate
        - user_address: Who is delegating
        - delegate_amount: amount of delegate
        '''
        
        nonce = self.web3.eth.get_transaction_count(user_address)
        candidate_delgation_count = self.contract.functions.candidate_delegation_count(collator_address).call()
        delegator_delegation_count = self.contract.functions.delegator_delegation_count(user_address).call()
        tx_dict = self.contract.functions.delegate(
            collator_address,
            amount,
            candidate_delgation_count,
            delegator_delegation_count
        ).buildTransaction({'gas': 210000})
        tx_dict['nonce'] = nonce
        tx_dict['from'] = user_address

        (is_success, message) = Helper.eth_sign_transaction(
                        web3=self.web3, 
                        tx_dict=tx_dict, 
                        user_address=user_address
                    )

        return (is_success, message)

    def bond_more(self, user_address, collator_address, amount):

        '''
        Method
        - Send delegator-bond-more transaction.

        Params 
        - collator_address: Whom to delegate
        - user_address: Who is delegating
        - more: amount of more staking 
        '''
        
        nonce = self.web3.eth.get_transaction_count(user_address)
        tx_dict = self.contract.functions.delegator_bond_more(
            collator_address,
            amount,
        ).buildTransaction({'gas': 210000})
        tx_dict['nonce'] = nonce
        tx_dict['from'] = user_address

        (is_success, message) = Helper.eth_sign_transaction(
                        web3=self.web3, 
                        tx_dict=tx_dict, 
                        user_address=user_address
                    )

        return (is_success, message)

    def bond_less(self, user_address, collator_address, amount):
        
        '''
        Method
        - Send schedule-bond-less transaction

        Params 
        - user_address: user's public address
        - collator_address: Whom to bond less
        - less: amount of bond less
        '''

        nonce = self.web3.eth.get_transaction_count(user_address)
        tx_dict = self.contract.functions.schedule_delegator_bond_less(
            collator_address,
            amount,
        ).buildTransaction({'gas': 210000})
        tx_dict['nonce'] = nonce
        tx_dict['from'] = user_address
        (is_success, message) = Helper.eth_sign_transaction(
                        web3=self.web3, 
                        tx_dict=tx_dict, 
                        user_address=user_address
                    )

        return (is_success, message)

    def revoke(self, user_address, collator_address):
        
        '''
        Method
        - Send scheduled-revoke-delegation transaction

        Params
        - user_address: User's public address
        - collator_address: Whom to revoke
        '''

        nonce = self.web3.eth.get_transaction_count(user_address)
        tx_dict = self.contract.functions.schedule_revoke_delegation(
            collator_address,
        ).buildTransaction({'gas': 210000})
        tx_dict['nonce'] = nonce
        tx_dict['from'] = user_address

        (is_success, message) = Helper.eth_sign_transaction(
                        web3=self.web3, 
                        tx_dict=tx_dict, 
                        user_address=user_address
                    )

        return (is_success, message)
        

class Substrate:

    def __init__(self, provider):
        
        try:
            self.api = SubstrateInterface(url=provider)
        except Exception as e:
            print("Error connecting local node. Message: {error}".format(error=e))
            return 0

    def bond(self, user_address, amount, payee, is_pool, pool_id):

        '''
        Method
        - Send bond extrinsic 
        
        Params
        - user_account(controller): user's public address 
        - amount: bond amount. Int
        - payee: Staked(auto-compound) / Stash(Reward goes to stash account)
        - pool_id: Pool id when user stakes to nomination pool. Int

        Returns
        - (is_success, message)
        - True, if succeed. False, if failed
        - message: Tx Hash / Error
        '''
 
        pallet = "NominationPools" if is_pool else "Staking"
        dispatch_call = "join" if is_pool else "bond"
        params = {'amount': amount, 'pool_id': pool_id} if is_pool \
                 else {'controller': user_address, 'value': amount, 'payee': payee}
        
        generic_call = Helper.get_generic_call(
            api=self.api,
            module=pallet,
            function=dispatch_call,
            params=params
        )
            
        (is_success, message) = Helper.send_extrinsic(
                                    api=self.api,
                                    generic_call=generic_call,
                                    user_address=user_address    
                                )
        return (is_success, message)

    def nominate(self, user_address, validators):

        '''
        Method
        - Send Nominate extrinsic 

        Params
        - user_account: User's public address
        - validators: [address of Validators]

        Returns
        - is_success: True, if succeed. False, if failed
        '''

        generic_call = Helper.get_generic_call(
            api=self.api,
            module="Staking",
            function="nominate",
            params={
                'targets': validators
            }
        )
        (is_success, message) = Helper.send_extrinsic(
                                    api=self.api,
                                    generic_call=generic_call,
                                    user_address=user_address    
                                )
        return (is_success, message)

    def bond_extra(self, user_address, amount, is_pool): 
        
        '''
        Method
        - Send bond extra extrinsic using user's key pair
        - Depends on whether user stakes to nomination pools or not
        - Call "putInFrontof" extrinsic to adjust user's bag position
        
        Params
        - additional: bond extra amount. 'Int'

        Returns
        - is_success: True, if succeed. False, if failed
        '''

        pallet = "NominationPools" if is_pool else "Staking"
        dispatch_call = "bondExtra"
        params = {'extra': amount} if is_pool else {'max_additional': amount}
    
        generic_call = Helper.get_generic_call(
            api=self.api,
            module=pallet,
            function=dispatch_call,
            params=params
        )

        (is_success, message) = Helper.send_extrinsic(
                                    api=self.api,
                                    generic_call=generic_call,
                                    user_address=user_address    
                                )

        if is_success == "Success": 

            lighter_node = Helper.reorder_bag_for(api=self.api, user_address=user_address) # TO-DO 
            generic_call = Helper.get_generic_call(
                api=self.api,
                module="VoterList",
                function="putInFrontOf",
                params={
                    'lighter': lighter_node
                }
            )
            (is_success, message) = Helper.send_extrinsic(
                                    api=self.api,
                                    generic_call=generic_call,
                                    user_address=user_address    
                                )
            return (is_success, message)
        else:
            return (is_success, message)

    def unbond(self, user_address, amount):
        
        '''
        Method
        - Send unbond extrinsic using user's key pair

        Params
        - amount: unbond amount. 'Int'

        Returns
        - is_success: True, if succeed. False, if failed
        '''

        generic_call = Helper.get_generic_call(
            api=self.api,
            module="Staking",
            function="unbond",
            params={
                'value': amount
            }
        )
        (is_success, message) = Helper.send_extrinsic(
                                    api=self.api,
                                    generic_call=generic_call,
                                    user_address=user_address    
                                )
        return (is_success, message)

    def rebond(self, user_address=None, amount=None):
        
        '''
        Method
        - Send rebond extrinsic using user's key pair

        Params
        - amount: unbond amount. 'Int'

        Returns
        - is_success: True, if succeed. False, if failed
        '''

        generic_call = Helper.get_generic_call(
            api=self.api,
            module="Staking",
            function="rebond",
            params={
                'value': amount
            }
        )
        (is_success, message) = Helper.send_extrinsic(
                                    api=self.api,
                                    generic_call=generic_call,
                                    user_address=user_address    
                                )
        return (is_success, message)

    def chill(self, user_address=None):

        '''
        Method
        - Send chill extrinsic 
        - Stop being as nominator/validator

        Params
        - user_addrss: User's public addrss

        Returns
        - is_success: True, if succeed. False, if failed
        '''
        
        generic_call = Helper.get_generic_call(
            api=self.api,
            module="Staking",
            function="chill",
            params={}
        )
        (is_success, message) = Helper.send_extrinsic(
                                    api=self.api,
                                    generic_call=generic_call,
                                    user_address=user_address    
                                )
        return (is_success, message)

if __name__ == "__main__":

    staking_substrate = Staking(env='substrate', provider='wss://ws-api.substake.app')
    mnemonic = "seminar outside rack viable away limit tunnel marble category witness parrot eager"
    key_pair = Keypair.create_from_mnemonic(mnemonic=mnemonic)
    staking_substrate.stake_less(
        user_address=key_pair,
        less="1"
    )
     
    staking_evm = Staking(env='evm', provider='https://rpc.api.moonbase.moonbeam.network')
    staking_evm.stake_less(
        user_address="0x24E54d40c79dd99Ec626692C0AB58862A126A67b",
        collator_address="0x3937B5F83f8e3DB413bD202bAf4da5A64879690F",
        less="1",
    )
    
