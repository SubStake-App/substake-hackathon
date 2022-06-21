
from curses.ascii import SUB
from base import Base
from Utils.chain_info import SUBSTRATE_DECIMALS

class Asset_Manager(Base):

    def __init__(self, env, provider):
        super().__init__(env=env, provider=provider)

    def get_user_balance_status(self, user_address):
        
        ledger = self.api.query(
                                    module='Staking',
                                    storage_function='Ledger',
                                    params=[user_address]
                                ).value
    
        print(ledger)
        total = float(ledger['total']) / 10**SUBSTRATE_DECIMALS
        active = float(ledger['active']) / 10**SUBSTRATE_DECIMALS
        if len(ledger['unlocking']) == 0:
            unlocking = ['']
        else:
            unlock = float(ledger['unlocking'][0].get('value')) / 10**SUBSTRATE_DECIMALS
            era = ledger['unlocking'][0].get('era')
        result = {
                    'total': total,
                    'active': active,
                    'unlock': {
                        'value': unlock,
                        'era': era
                    }
                }
        print(result)
        return result

if __name__ == '__main__': 

    asset_manager = Asset_Manager(
                                    env='substrate', 
                                    provider='wss://ws-api.substake.app'
                                 )
    asset_manager.get_user_balance_status(user_address='5GeGNPSck3uML62Xq8SSHSDgxS9WXMJ3ukNfajvrcYQ2HUe9')
