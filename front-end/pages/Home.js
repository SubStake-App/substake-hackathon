import { StyleSheet, Text, View } from 'react-native';
import { Button } from '@rneui/base';
import TopBar from '../components/TopBar/TopBar';
import Layout from '../components/Layout';
import { useAsyncStorage } from '../components/Context/AsyncStorage';

export default function Home({ navigation }) {
  const { accounts, currentIndex } = useAsyncStorage();

  return (
    <Layout>
      <TopBar title={accounts[currentIndex].nickname} navigation={navigation} />
      <View style={styles.container}>
        <View style={styles.container}>
          <Text style={styles.text}>최초의 섭스레이트 자산 스테이킹 플랫폼</Text>
          <Text style={styles.text}>SubStake에 오신 것을 환영합니다.</Text>
          <Button
            title="+ STAKE NOW"
            titleStyle={{ color: '#243AFF', fontSize: 13 }}
            buttonStyle={{ backgroundColor: 'white', borderRadius: 30, marginTop: 30 }}
            onPress={() => navigation.navigate('StakableAssets')}
          />
        </View>
        <View style={styles.serviceDetail}>
          <Text style={{ color: 'white' }}>서비스 상세정보</Text>
        </View>
      </View>
    </Layout>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    color: 'white',
    fontSize: 20,
    marginBottom: 3,
  },
  serviceDetail: {
    paddingVertical: 10,
    paddingHorizontal: 20,
    backgroundColor: '#343781A1',
    borderRadius: 10,
    marginTop: 30,
  },
});
