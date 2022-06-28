import logging
import json
import Utils.Config as db_con
from Utils.Config import MOONBASE_AMOUNT_DUE
from substrateinterface import SubstrateInterface

substrate = SubstrateInterface(
    #url="wss://ws-api.moon.substake.app"
    url="ws://127.0.0.1:9944"
)   

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

def get_total_active_collator_count():
    result = substrate.query(
            module='ParachainStaking',
            storage_function='TotalSelected'
    )
    total_active_collator_count = result.value
    
    logging.info(f"==== {total_active_collator_count}")
    return total_active_collator_count

def get_recommended_collators(bond_amount:float, risk_level) -> list:
    try:
        conn = db_con.get_connection()
        collator_list = [] 
        with conn.cursor() as cur: 
            
            total_active_collator_count = get_total_active_collator_count() #change to get data from on-chain
            limit_collator_count = 1 #total_active_collator_count*(2/3)
            avg_bpr = total_active_collator_count / 600 #80(active collators)/600(blocks per round)
            
            query_string = f"SELECT * from dev_collator_list " \
                        f"WHERE active_status = True " \
                        f"AND minimun_bond < {bond_amount} " \
                        f"AND average_bpr_week > {avg_bpr} " \
                        f"ORDER BY average_bpr_week DESC, bonded_total DESC " \
                        f"LIMIT {limit_collator_count}" 
                        
            if risk_level == 'low' :
                query_string = f"SELECT * from dev_collator_list " \
                        f"WHERE active_status = True " \
                        f"AND minimun_bond < {bond_amount} " \
                        f"AND average_bpr_week > {avg_bpr} " \
                        f"ORDER BY bonded_total DESC, average_bpr_week DESC " \
                        f"LIMIT {limit_collator_count}" 
                        
            cur.execute(query_string)
            collator_set = cur.fetchall()
            
            for row in collator_set:
                account_address = row[0]
                account_displayname = row[1]
                average_bpr_week = '{:.3f}'.format(float(row[8]))
                bonded_total = row[5]
                estimated_apr = MOONBASE_AMOUNT_DUE * float(average_bpr_week) * 52 * 100
                estimated_apr = '{:.2f}'.format(estimated_apr)
                bonded_total = float(row[5])
                simulated_share = (bond_amount/bonded_total) * 100
                simulated_share = '{:.3f}'.format(float(simulated_share))
                
                collators = {
                                'address' : account_address,                #콜래터 지갑 주소 
                                'display_name' : account_displayname,       #콜래터 이름
                                'estimated_apr' : estimated_apr,            #average apr /week  
                                'simulated_share' : simulated_share
                                
                            }
                collator_list.append((collators))  
        return collator_list 
    except Exception as e:
        e.with_traceback()
    finally:
        conn.close()

## for test
def main():
    return_str = json.dumps(get_recommended_collators(10.0, 'high'))
    print(return_str)
    return_str = json.dumps(get_recommended_collators(10.0, 'low'))
    print(return_str)

    
if __name__ == "__main__":
    main()