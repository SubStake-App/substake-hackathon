import { Button, Divider } from '@rneui/base';
import { StyleSheet, Text, View, Image, Pressable } from 'react-native';
import AccountIcon from '../components/common/AccountIcon';
import { useAsyncStorageContext } from '../components/Context/AsyncStorage';
import Layout from '../components/Layout';
import TopBar from '../components/TopBar/TopBar';
import checked from '../assets/checked.png';

export default function Accounts({ navigation }) {
  const { accounts, currentIndex, setCurrentIndex } = useAsyncStorageContext();

  return (
    <Layout>
      <TopBar title="등록된 계정" navigation={navigation} path="Home" hideIcon={true} />
      <View style={styles.container}>
        <View>
          {accounts.map((el, i) => (
            <Pressable onPress={() => setCurrentIndex(i)}>
              <View key={i} style={styles.accountRow}>
                <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                  <AccountIcon publicKey={el.publicKey} />
                  <Text style={styles.nickname}>{el.nickname}</Text>
                </View>
                {currentIndex === i && <Image source={checked} />}
              </View>
              <Divider style={{ marginVertical: 15 }} />
            </Pressable>
          ))}
        </View>
        <Button title="계정 추가" onPress={() => navigation.navigate('ReRegister')} />
      </View>
    </Layout>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 10,
    paddingVertical: 20,
    justifyContent: 'space-between',
  },
  accountRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  nickname: {
    color: 'white',
    fontSize: 24,
    marginLeft: 15,
  },
});
