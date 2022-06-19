import { View, StyleSheet, Text, Image, Pressable } from 'react-native';
import arrow from '../../assets/arrowLeft.png';
import AccountIcon from '../common/AccountIcon';
import { useAsyncStorageContext } from '../Context/AsyncStorage';

export default function TopBar({ path, navigation, title, hideIcon }) {
  const { accounts, currentIndex } = useAsyncStorageContext();

  return (
    <View style={styles.container}>
      {path && (
        <Pressable onPress={() => navigation.navigate(path)}>
          <Image source={arrow} on />
        </Pressable>
      )}
      {title && <Text style={{ color: 'white', fontSize: 20 }}>{title}</Text>}
      {hideIcon ? (
        <View />
      ) : (
        <Pressable onPress={() => navigation.navigate('Accounts')}>
          <AccountIcon publicKey={accounts[currentIndex].publicKey} />
        </Pressable>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    height: 50,
  },
});
