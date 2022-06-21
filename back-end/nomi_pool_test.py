from substrateinterface import SubstrateInterface

substrate = SubstrateInterface(
    url="wss://ws-api.substake.app"
)   

result = substrate.query( 
    module='NominationPools',
    storage_function='LastPoolId'
)

last_pool_id = result.value
index = 1
while index <= last_pool_id :
    result = substrate.query(
        module='NominationPools',
        storage_function='Metadata',
        params=[index]
    )
    index += 1
    print(result.value)
