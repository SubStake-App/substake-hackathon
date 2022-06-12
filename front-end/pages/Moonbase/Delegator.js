import { Text, View } from 'react-native';
import Layout from '../../components/Layout';
import TopBar from '../../components/TopBar/TopBar';

export default function MoonbaseDelegator({ navigation }) {
  return (
    <Layout>
      <TopBar title="Delegator" path="StakableAssets" navigation={navigation} />
      <View>
        <Text>MoonbaseDelegator</Text>
      </View>
    </Layout>
  );
}
