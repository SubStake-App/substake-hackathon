from xmlrpc.client import Boolean
from Utils.AESCipher import AESCipher
from Utils.Config import get_connection, key


def set_user_info(public_key:str, private_key:str, env:str) -> Boolean:
    try:
        conn = get_connection()
        with conn.cursor() as cur: 
            private_key = AESCipher(bytes(key)).encrypt(private_key)
            query_str = f"INSERT INTO SUB_USER_KEY (public_key, private_key, env) " \
                    f"VALUES ({public_key}, {private_key}, {env})"
            cur.execute(query_str)
            return True;
    except Exception as e:
        conn.rollback()
        e.with_traceback()
        return False
        
    finally:
        conn.commit()
        conn.close()

def get_user_info(public_key:str) -> list:
    try:
        conn = get_connection()
        with conn.cursor() as cur: 
            private_key = AESCipher(bytes(key)).encrypt(private_key)
            query_str = f"SELECT public_key, private_key, env FROM SUB_USER_KEY " \
                    f"WHERE public_key = {public_key}"
            cur.execute(query_str)
            result_set = cur.fetchone()
            private_key = AESCipher(bytes(key)).decrypt(result_set[1])
            result_val = {
                                'public_key' : result_set[0],                #콜래터 지갑 주소 
                                'private_key' : private_key,       #콜래터 이름
                                'env' : result_set[2]
                                
                        }
            return result_val
    except Exception as e:
        e.with_traceback()
        
    finally:
        conn.close()