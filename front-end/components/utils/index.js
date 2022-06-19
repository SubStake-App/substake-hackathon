import { Keyring } from '@polkadot/api';
import { Wallet } from 'ethers';

// TODO:  function that derive private key from seed phase
export const derivePrivateKey = (mnemonic) => {
  try {
    const keyring = new Keyring({ type: 'sr25519' });
    return keyring.createFromUri(mnemonic);
  } catch {
    try {
      return Wallet.fromMnemonic(mnemonic);
    } catch {
      return undefined;
    }
  }
};
