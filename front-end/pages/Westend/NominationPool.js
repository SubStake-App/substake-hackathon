import { Text, View } from 'react-native';
import Layout from '../../components/Layout';
import TopBar from '../../components/TopBar/TopBar';

export default function WestendNominationPool({ navigation }) {
  return (
    <Layout>
      <TopBar title="Nomination Pool" path="StakableAssets" navigation={navigation} />
      <View>
        <Text>WestendNominationPool</Text>
      </View>
    </Layout>
  );
}
