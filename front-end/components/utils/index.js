import { Keyring } from '@polkadot/api';
import { Wallet } from 'ethers';

// TODO:  function that derive private key from seed phase
export const derivePrivateKey = (mnemonic) => {
  try {
    const keyring = new Keyring({ type: 'sr25519' });
    return { sr25519: keyring.createFromUri(mnemonic), bip39: Wallet.fromMnemonic(mnemonic) };
  } catch {
    throw Error('Invalid Mnemonic');
  }
};
