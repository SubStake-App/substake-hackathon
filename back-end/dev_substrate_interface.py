import logging
from substrateinterface import SubstrateInterface

substrate = SubstrateInterface(
    url="wss://moonbeam-alpha.api.onfinality.io/public-ws"
)   

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

def get_candidate_pool() -> list:
    
    result = substrate.query(
        module='ParachainStaking',
        storage_function='CandidatePool'
    )
    return result.value

def main():
    candidate_pool_list = get_candidate_pool()
    for c_pool in candidate_pool_list:
        owner = c_pool['owner']
        amount = c_pool['amount']
        logging.info(f'{owner} : {amount/10**18}')
    
if __name__ == "__main__":
    main()