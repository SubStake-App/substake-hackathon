import { useEffect, useState } from 'react';
import { View, Image, Animated, Easing, Modal, StyleSheet } from 'react-native';
import loading_bag from '../../assets/loading_bag.png';
import loading_light from '../../assets/loading_light.png';
import { Nunito700, Nunito400 } from '../constant';

export default function LoadingModal() {
  const [isVisible, setIsVisible] = useState(false);
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
    <Modal transparent={true} animationType="fade">
      <View style={styles.modalOverlay}>
        <View style={styles.modalContent}>
          <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
            <Animated.Image
              source={loading_bag}
              style={{ position: 'absolute', transform: [{ translateY: animated }] }}
            />
            <Image source={loading_light} style={{ marginTop: 60 }} />
          </View>
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  modalOverlay: {
    width: '100%',
    height: '100%',
    backgroundColor: 'rgba(0,0,0,0.8)',
    padding: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  modalContent: {
    padding: 25,
  },
  modalTitle: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  modalTitleHeader: {
    fontSize: 18,
    fontFamily: Nunito700,
  },
  modalTitleMain: {
    fontSize: 10,
    fontFamily: Nunito400,
    color: '#7E7794',
  },
  modalDetailHeader: {
    fontSize: 10,
    fontFamily: Nunito700,
    color: '#7E7794',
  },
  modalDetailMain: {
    fontSize: 10,
    fontFamily: Nunito400,
    color: '#7E7794',
  },
  button: {
    alignSelf: 'stretch',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#CDE1FF80',
    marginTop: 10,
    paddingVertical: 5,
  },
  buttonText: {
    color: '#0029FF',
    fontSize: 18,
  },
});
