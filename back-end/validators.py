
from substrateinterface import SubstrateInterface

class Validators:
    
    def __init__(self, env, provider):
        self.env = env
        self.provider = provider

class Substrate:
    
    def __init__(self, provider):
        
        try:
            self.api = SubstrateInterface(url=provider)
        except Exception as e:
            print("Error connecting local node. Message: {error}".format(error=e))
            return 0
        
    