
from substrateinterface import SubstrateInterface
from web3 import Web3
from helper import Helper
import json

KEY_PAIR = None
MOONBEAM_STAKING_CONTRACT = "0x0000000000000000000000000000000000000800"
EVM_DECIMALS = 18
SUBSTRATE_DECIMALS = 12
PRIVATE_KEY = ""

class Staking:

    '''
    Class
    - Staking class contains EVM/Substrate class
    '''

    def __init__(self, env, provider, is_pool=False):
        
        if env == 'evm':
            self.evm = EVM(provider=provider)
            self.name = 'evm'
        elif env == 'substrate':
            self.substrate = Substrate(provider=provider, is_pool=is_pool)
            self.name = 'substrate'

    def stake(
        self, 
        user_address=None, 
        collator_address=None, 
        amount=None, 
        payee='Staked',
        is_nominate=False,
    ):

        '''
        Method
        - EVM: delegate
        - Substrate: bond
        '''
        
        if self.name == 'evm':
            self.evm.delegate(
                user_address=user_address, 
                collator_address=collator_address, 
                delegate_amount=amount
            )
        elif self.name == 'substrate':
            if is_nominate: # To-Do: Bond and Nominate
                pass
            else:
                self.substrate.bond(
                    user_address=user_address,
                    amount=amount,
                    payee=payee
                )
    
    def stake_more(self, user_address, more, collator_address=None):

        '''
        Method
        - Send stake-more-asset transaction
        
        Params
        - user_address: Whose asset
        - more: additional asset
        - collator_address: Only needed in EVM
        '''

        if self.name == 'evm':
            self.evm.bond_more(
                user_address=user_address,
                collator_address=collator_address,
                more=more
            )
        elif self.name == 'substrate':
            self.substrate.bond_extra(
                user_address=user_address,
                additional=more
            )

    def stake_less(self, user_address, less, collator_address=None):
        if self.name == 'evm':
            self.evm.bond_less(
                user_address=user_address,
                collator_address=collator_address,
                less=less
            )
        elif self.name == 'substrate':
            self.substrate.unbond(
                user_address=user_address,
                amount=less,
            )

    def stop_stake(self, user_address, collator_address=None):

        '''
        Method
        - Pull all staked asset

        Params 
        - user_address: Whose asset
        - collator_address: Only needed in EVM(Moonbeam)
        '''

        if self.name == 'evm':
            self.evm.revoke(
                user_address=user_address, 
                collator_address=collator_address
            )
        elif self.name == 'substrate':
            self.substrate.chill(user_address=user_address)


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
            address=MOONBEAM_STAKING_CONTRACT, 
            abi=MOONBEAM_STAKING_ABI
        )
        
    def delegate(
        self, 
        user_address,
        collator_address, 
        amount, 
    ):

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
        ).buildTransaction()
        tx_dict['nonce'] = nonce
        tx_dict['from'] = user_address

        Helper.eth_sign_transaction(
            web3=self.web3, 
            tx_dict=tx_dict, 
            user_address=user_address
        )

    def bond_more(self, user_address, collator_address, more):

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
            more,
        ).buildTransaction()
        tx_dict['nonce'] = nonce
        tx_dict['from'] = user_address

        Helper.eth_sign_transaction(
            web3=self.web3,
            tx_dict=tx_dict,
            user_address=user_address
        )

    def bond_less(self, user_address, collator_address, less):
        
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
            less,
        ).buildTransaction()
        tx_dict['nonce'] = nonce
        tx_dict['from'] = user_address

        Helper.eth_sign_transaction(
            web3=self.web3,
            tx_dict=tx_dict,
            user_address=user_address
        )

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
        ).buildTransaction()
        tx_dict['nonce'] = nonce
        tx_dict['from'] = user_address

        Helper.eth_sign_transaction(
            web3=self.web3,
            tx_dict=tx_dict,
            user_address=user_address
        )
        

class Substrate:

    def __init__(self, provider, is_pool=False):
        try:
            self.api = SubstrateInterface(url=provider)
        except Exception as e:
            print("Error connecting local node. Message: {error}".format(error=e))
            return 0
        self.is_pool = is_pool

    def bond(self, user_address=None, amount=None, payee=None, pool_id=None):

        '''
        Method
        - Send bond extrinsic 
        
        Params
        - user_account(controller): user's public address 
        - amount: bond amount. Int
        - payee: Staked(auto-compound) / Stash(Reward goes to stash account)
        - pool_id: Pool id when user stakes to nomination pool. Int
        '''
        
        assert user_address is not None, "SUBSTAKE-SUBSTRATE(BOND): User adress should be provided"
        assert amount is not None, "SUBSTAKE-SUBSTRATE(BOND): Amount should be provided"
        assert type(amount) is int, "SUBSTAKE-SUBSTRATE(BOND): Amount should be Int" 
        
        if self.is_pool:
            assert pool_id is not None, "Pool ID must be provided when bond to nomination pool"

        if not self.is_pool:
            assert payee is not None, "Payee must be provided when bond to validators"

        amount = amount * 10**SUBSTRATE_DECIMALS    
        pallet = "NominationPools" if self.is_pool else "Staking"
        dispatch_call = "join" if self.is_pool else "bond"
        params = {'amount': amount, 'pool_id': pool_id} if self.is_pool \
                 else {'controller': user_address, 'value': amount, 'payee': payee}
        
        generic_call = Helper.get_generic_call(
            api=self.api,
            module=pallet,
            function=dispatch_call,
            params=params
        )
            
        Helper.send_extrinsic(
            api=self.api,
            generic_call=generic_call,
            user_address=user_address    
        )

    def nominate(self, user_address=None, validators=None):

        '''
        Method
        - Send Nominate extrinsic 

        Params
        - user_account: User's public address
        - validators: [address of Validators]
        '''

        assert user_address is not None, "SUBSTAKE-SUBSTRATE(NOMINATE): User address should be provided"
        assert validators is not None, "SUBSTAKE-SUBSTRATE(NOMINATE): Validators should be provided when nominate"
        assert self.is_pool is False, "SUBSTAKE_SUBSTRATE(NOMINATE): Current nomination pool not supports nominate"

        generic_call = Helper.get_generic_call(
            api=self.api,
            module="Staking",
            function="nominate",
            params={
                'targets': validators
            }
        )
        Helper.send_extrinsic(
            api=self.api,
            generic_call=generic_call,
            user_address=user_address    
        )

    def bond_extra(self, user_address=None, additional=None): 
        
        '''
        Method
        - Send bond extra extrinsic using user's key pair
        - Depends on whether user stakes to nomination pools or not
        - Call "putInFrontof" extrinsic to adjust user's bag position
        
        Params
        - additional: bond extra amount. 'Int'
        '''

        assert user_address is not None, "SUBSTAKE-SUBSTRATE(BOND_EXTRA): User adress should be provided"
        assert additional is not None, "SUBSTAKE-SUBSTRATE(BOND_EXTRA): Additional amount should be provided"
        assert type(additional) is int, "SUBSTAKE-SUBSTRATE(BOND_EXTRA): Additional type should be Int"
        
        additional = additional * 10**SUBSTRATE_DECIMALS
        pallet = "NominationPools" if self.is_pool else "Staking"
        dispatch_call = "bondExtra"
        params = {'extra': additional} if self.is_pool else {'max_additional': additional}
    
        generic_call = Helper.get_generic_call(
            api=self.api,
            module=pallet,
            function=dispatch_call,
            params=params
        )
        Helper.send_extrinsic(
            api=self.api,
            generic_call=generic_call,
            user_address=user_address    
        )

        lighter_node = Helper.reorder_bag_for(api=self.api, user_address=user_address) # TO-DO 
        generic_call = Helper.get_generic_call(
            api=self.api,
            module="VoterList",
            function="putInFrontOf",
            params={
                'lighter': lighter_node
            }
        )
        Helper.send_extrinsic(
            api=self.api,
            generic_call=generic_call,
            user_address=user_address    
        )

    def unbond(self, user_address=None, amount=None):
        
        '''
        Method
        - Send unbond extrinsic using user's key pair

        Params
        - amount: unbond amount. 'Int'
        '''

        assert user_address is not None, "SUBSTAKE-SUBSTRATE(UNBOND): User adress should be provided"
        assert amount is not None, "SUBSTAKE-SUBSTRATE(UNBOND): Amount should be provided"
        assert type(amount) is int, "SUBSTAKE-SUBSTRATE(UNBOND): Amount should be Int"
        assert self.is_pool is False, "SUBSTAKE_SUBSTRATE(UNBOND): Current nomination pool not support unbond"

        amount = amount * 10**SUBSTRATE_DECIMALS
        generic_call = Helper.get_generic_call(
            api=self.api,
            module="Staking",
            function="unbond",
            params={
                'value': amount
            }
        )
        Helper.send_extrinsic(
            api=self.api,
            generic_call=generic_call,
            user_address=user_address    
        )

    def rebond(self, user_address=None, amount=None):
        
        '''
        Method
        - Send rebond extrinsic using user's key pair

        Params
        - amount: unbond amount. 'Int'
        '''

        assert user_address is not None, "SUBSTAKE-SUBSTRATE(REBOND): User adress should be provided"
        assert amount is not None, "SUBSTAKE-SUBSTRATE(REBOND): Amount should be provided"
        assert type(amount) is int, "SUBSTAKE-SUBSTRATE(REBOND): Amount should be Int"
        assert self.is_pool is False, "SUBSTAKE_SUBSTRATE(REBOND): Current nomination pool not supports rebond"

        amount = amount * 10**SUBSTRATE_DECIMALS
        generic_call = Helper.get_generic_call(
            api=self.api,
            module="Staking",
            function="rebond",
            params={
                'value': amount
            }
        )
        Helper.send_extrinsic(
            api=self.api,
            generic_call=generic_call,
            user_address=user_address    
        )

    def chill(self, user_address=None):

        '''
        Method
        - Send chill extrinsic 
        - Stop being as nominator/validator

        Params
        - user_addrss: User's public addrss
        '''

        assert user_address is not None, "SUBSTAKE-SUBSTRATE(CHILL): User address must be provided"
        assert self.is_pool is False, "SUBSTAKE_SUBSTRATE(CHILL): Current nomination pool not supports chill"
        
        generic_call = Helper.get_generic_call(
            api=self.api,
            module="Staking",
            function="chill",
            params={}
        )
        Helper.send_extrinsic(
            api=self.api,
            generic_call=generic_call,
            user_address=user_address    
        )


if __name__ == "__main__":

    substrate = Substrate(provider="wss://ws-api.substake.app", is_pool=True)
    substrate.nominate(user_address="a", validators="b")
    # This account is only for test
    # No worry for hacking
    # mnemonic = "seminar outside rack viable away limit tunnel marble category witness parrot eager"
    # key_pair = Keypair.create_from_mnemonic(mnemonic=mnemonic)
    # substrate.rebond(
    #     user_address=key_pair,
    #     amount=1000000000000,
    # )

    # staking1 = Staking(env='evm', provider='https://rpc.api.moonbase.moonbeam.network')
    # staking2 = Staking(env='substrate', provider='wss://ws-api.substake.app')

    # print(staking1.name)
    # print(staking2.name)


    
