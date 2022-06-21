import { Keyring } from '@polkadot/api';
import { BigNumber, Wallet } from 'ethers';
import { formatUnits } from 'ethers/lib/utils';

// TODO:  function that derive private key from seed phase
export const derivePrivateKey = (mnemonic) => {
  try {
    const keyring = new Keyring({ type: 'sr25519' });
    console.log(Wallet.fromMnemonic(mnemonic).address, Wallet.fromMnemonic(mnemonic).privateKey);

    return { sr25519: keyring.createFromUri(mnemonic), bip39: Wallet.fromMnemonic(mnemonic) };
  } catch {
    throw Error('Invalid Mnemonic');
  }
};

export const formatRawBalanceToString = (balance) => {
  return Number.parseFloat(formatUnits(BigNumber.from(balance.toHuman().replace(/,/g, '')), 12).toString()).toFixed(4);
};
