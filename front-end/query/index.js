import { ethers } from 'ethers';
import { useQuery } from 'react-query';
import { useAsyncStorage } from '../components/Context/AsyncStorage';
import { useMoonbeam } from '../components/Context/MoonbeamContext';
import { useWestend } from '../components/Context/WestendContext';

export const balanceQuery = async (api, provider, accounts, currentIndex) => {
  if (accounts.length === 0) return { moonbeamBalance: 0, westendBalance: 0 };

  const publicKey = { sr25519: accounts[currentIndex].sr25519, bip39: accounts[currentIndex].bip39 };

  const { data: westendRawBalance } = await api.query.system.account(publicKey.sr25519);
  const westendBalance = westendRawBalance;

  // const moonbeamRawBalance = await provider.getBalance(publicKey.bip39);
  // const moonbeamBalance = ethers.utils.formatEther(moonbeamRawBalance);

  return { moonbeamBalance: 0, westendBalance };
};

export const useUserBalance = () => {
  const { accounts, currentIndex } = useAsyncStorage();
  const { provider } = useMoonbeam();
  const { api } = useWestend();

  return useQuery(['userBalance', currentIndex], () => balanceQuery(api, provider, accounts, currentIndex), {
    enabled: !!api && !!provider && !!accounts,
  });
};
