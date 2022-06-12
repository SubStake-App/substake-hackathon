import { useEffect } from 'react';
import { Text, View, Image, Animated, Easing } from 'react-native';
import Layout from '../components/Layout';
import loading_bag from '../assets/loading_bag.png';
import loading_light from '../assets/loading_light.png';

export default function Loading() {
  const animated = new Animated.Value(5);
  const duration = 500;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(animated, {
          toValue: 15,
          easing: Easing.bezier(0.5, 1, 0.89, 1),
          duration: duration,
          useNativeDriver: true,
        }),
        Animated.timing(animated, {
          toValue: 5,
          easing: Easing.bezier(0.11, 0, 0.5, 0),
          duration: duration,
          useNativeDriver: true,
        }),
        Animated.timing(animated, {
          toValue: -5,
          easing: Easing.bezier(0.5, 1, 0.89, 1),
          duration: duration,
          useNativeDriver: true,
        }),
        Animated.timing(animated, {
          toValue: 5,
          easing: Easing.bezier(0.11, 0, 0.5, 0),
          duration: duration,
          useNativeDriver: true,
        }),
      ])
    ).start();
  }, []);

  return (
    <Layout>
      <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        <Animated.Image source={loading_bag} style={{ position: 'absolute', transform: [{ translateY: animated }] }} />
        <Image source={loading_light} style={{ marginTop: 100 }} />
        <Text style={{ color: '#A8A8A8', fontSize: 18, marginTop: 20 }}>Rhee님의 자산내역을 업데이트 하는 중</Text>
      </View>
    </Layout>
  );
}
