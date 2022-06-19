import { useState, useEffect, createContext, useContext } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const AsyncStorageContext = createContext();

export const useAsyncStorageContext = () => useContext(AsyncStorageContext);

export function AsyncStorageProvider({ children }) {
  const [accounts, setAccounts] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    const getAccounts = async () => {
      const accountArr = JSON.parse(await AsyncStorage.getItem('@substake_accounts'));
      setAccounts(accountArr);
      setIsLoaded(true);
    };

    getAccounts();
  }, []);

  useEffect(() => {
    AsyncStorage.setItem('@substake_accounts', JSON.stringify(accounts));
  }, [accounts]);

  const addAccount = (account) => {
    if (account?.publicKey && account?.nickname) setAccounts([...accounts, account]);
  };

  const removeAccount = (account) => {
    if (account?.publicKey && account?.nickname) {
      if (account.publicKey === accounts[accounts.length - 1].publicKey) setCurrentIndex(0);
      setAccounts(accounts.filter((el) => el.publicKey !== account.publicKey));
    }
  };

  return (
    <AsyncStorageContext.Provider
      value={{ isLoaded, accounts, currentIndex, setCurrentIndex, addAccount, removeAccount }}
    >
      {children}
    </AsyncStorageContext.Provider>
  );
}
