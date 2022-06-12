import { Text, View } from 'react-native';
import Layout from '../../components/Layout';
import TopBar from '../../components/TopBar/TopBar';

export default function MoonbaseCollator({ navigation }) {
  return (
    <Layout>
      <TopBar title="Collator" path="StakableAssets" navigation={navigation} />
      <View>
        <Text>MoonbaseCollator</Text>
      </View>
    </Layout>
  );
}
