

from substrateinterface import SubstrateInterface
from base import Base
import json

OVER_SUBSCRIBED = 256
COMMISSION_THRESHOLD = 10

class Validators(Base):
    
    def __init__(self, env, provider):
       super().__init__(env=env, provider=provider)

    def ready(self):
        self.active_validators = self.api.query('Session', 'Validators').value
        self.era = self.api.query('Staking', 'ActiveEra').value['index'] - 1
        print(self.active_validators)
    
    def recommend_validators(self, bond_amount: float):

        self.ready()
        stakers = dict()
        # eras_reward_points = self.api.query(
        #                     'Staking',
        #                     'ErasRewardPoints',
        #                     params=[self.era]
        #                 ).value
        # total_points = float(eras_reward_points['total'])
        # individual_points = float(eras_reward_points['individual'])
        # eras_reward_dict = {}
        # for (validator, reward) in individual_points:
        #     eras_reward_dict[validator] = int(reward)

        # with open('reward.json', 'w') as f:
        #     json.dump(eras_reward_dict, f, indent=2)

        eras_validators_reward = float(
                                        self.api.query(
                                            'Staking',
                                            'ErasValidatorReward',
                                            params=[self.era]
                                        ).value
                                ) / 10**12
        eras_reward_per_validators = eras_validators_reward / len(self.active_validators)
        
        for i in range(len(self.active_validators)):

            '''
            validator_info = {
                'commission':
                'blocked':
            }

            temp = {
                'total':
                'owned':
                'others':
            }
            '''
            
            validator_info = self.api.query(
                                                'Staking', 
                                                'Validators', 
                                                params=[self.active_validators[i]]
                                            ).value
            commission = float(validator_info['commission']) / 10**7
            blocked = validator_info['blocked']
            
            if blocked: 
                continue

            if commission > COMMISSION_THRESHOLD:
                continue

            commission = 0 if commission < 1 else commission
            eras_reward_per_validators = (1 - commission / 10**2) * eras_reward_per_validators
            
            temp = self.api.query(
                        'Staking', 
                        'ErasStakers', 
                        params=[self.era, self.active_validators[i]]
                      ).value 
    
            total = float(temp['total']) / 10**12 
            own = float(temp['own']) / 10**12
            nominators = temp['others']

            if len(nominators) > OVER_SUBSCRIBED:
                continue

            share_ratio = bond_amount / (total + bond_amount)
            print('share_ratio: {share}'.format(share=share_ratio))
            user_reward = eras_reward_per_validators * share_ratio
            print('user_reward: {reward}'.format(reward=user_reward))
            user_return = user_reward / bond_amount * 100        

            stakers[self.active_validators[i]] = { 
                                                    'total': total, 
                                                    'own': own, 
                                                    'user_return': user_return, 
                                                    'nominators': nominators 
                                                }
            
            return stakers
        with open('output.json', 'w') as f:
            json.dump(stakers, f, indent=2)




if __name__ == '__main__':
    
    validators = Validators(env='substrate', provider='wss://ws-api.substake.app')
    validators.recommend_validators(bond_amount=3.05)

        
    