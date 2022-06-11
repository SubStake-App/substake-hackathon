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

def get_round_info() -> int:
    result = substrate.query(
        module='ParachainStaking',
        storage_function='Round'
    )
    return result.value

def get_award_points(round:int, account:str) -> None:
    result = substrate.query(
        module='ParachainStaking',
        storage_function='AwardedPts',
        params=[round, account]
    )
    return result.value

## for test
def main():
    candidate_pool_list = get_candidate_pool()
    for c_pool in candidate_pool_list:
        owner = c_pool['owner']
        amount = c_pool['amount']
        logging.info(f'{owner} : {amount/10**18}')
    
    round = get_round_info()
    logging.info(f'{round}')
    
    awarded_pts = get_award_points(round['current'], '0xF1046A8D2451055BEA477799C19fd3fe815B05c5')
    logging.info(f'{awarded_pts}')
    
if __name__ == "__main__":
    main()