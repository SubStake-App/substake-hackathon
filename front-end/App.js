import { useEffect, useState, useContext } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { StatusBar } from 'expo-status-bar';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import {
  Nunito_400Regular,
  Nunito_500Medium,
  Nunito_600SemiBold,
  Nunito_700Bold,
  useFonts,
} from '@expo-google-fonts/nunito';

import Home from './pages/Home';
import StakableAssets from './pages/StakableAssets';
import WestendNominator from './pages/Westend/Nominator';
import WestendNominationPool from './pages/Westend/NominationPool';
import WestendValidator from './pages/Westend/Validator';
import MoonbaseCollator from './pages/Moonbase/Collator';
import MoonbaseDelegator from './pages/Moonbase/Delegator';
import Register from './pages/Register';
import Welcome from './pages/Welcome';
import { AsyncStorageProvider, AsyncStorageContext } from './components/Context/AsyncStorage';
import LoadingModal from './components/LoadingModal';
import AppLoading from './components/AppLoading';

const Stack = createNativeStackNavigator();

export function Root() {
  const { isLoaded, accounts } = useContext(AsyncStorageContext);
  const isRegistered = accounts && accounts.length > 0;

  return (
    <NavigationContainer>
      <StatusBar style="light" />
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {isLoaded ? (
          isRegistered ? (
            <>
              <Stack.Screen name="Home" component={Home} />
              <Stack.Screen name="StakableAssets" component={StakableAssets} />
              <Stack.Screen name="WestendNominator" component={WestendNominator} />
              <Stack.Screen name="WestendNominationPool" component={WestendNominationPool} />
              <Stack.Screen name="WestendValidator" component={WestendValidator} />
              <Stack.Screen name="MoonbaseCollator" component={MoonbaseCollator} />
              <Stack.Screen name="MoonbaseDelegator" component={MoonbaseDelegator} />
            </>
          ) : (
            <>
              <Stack.Screen name="Welcome" component={Welcome} />
              <Stack.Screen name="Register" component={Register} />
            </>
          )
        ) : (
          <Stack.Screen name="Loading" component={AppLoading} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default function App() {
  useFonts({ Nunito_400Regular, Nunito_500Medium, Nunito_600SemiBold, Nunito_700Bold });

  return (
    <AsyncStorageProvider>
      <Root />
    </AsyncStorageProvider>
  );
}
