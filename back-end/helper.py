
class Helper:

    @staticmethod
    def send_extrinsic(api, generic_call, user_account):
        '''
        Internal Function
        Take extrinsic call as parameter and send extrinsic with user's key-pair

        Params
        - generic_call: extrinc call from Substrate Interface. 
        - public_key: To get private key. DB[public_key] -> private_key
        '''
        key_pair = user_account
        signed = api.create_signed_extrinsic(
            call=generic_call,
            keypair=key_pair, # ToDo
        )
        try:
            print("Submit Extrinsic")
            api.submit_extrinsic(
                extrinsic=signed,
            ) 
            print("Done!")
        except Exception as e:
            print("Error submitting extrinsic. Message: {error}".format(error=e))

    @staticmethod
    def get_generic_call(self, module, function, params=None):

        '''
        Params
        - module: Name of Pallet. First word must be Capital letter.
        - function: Dispatch call of Pallet
        - params: Parameters of dipatch call. Form should be dictionary.
        '''
        generic_call = self.api.compose_call(
            call_module=module,
            call_function=function,
            call_params=params
        )
        return generic_call