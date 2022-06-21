import { ScrollView, Text, View, Pressable, Modal, StyleSheet, TextInput } from 'react-native';
import { useEffect, useRef, useState } from 'react';

export function NominationPoolModal({ setModalVisible, modalVisible, selectedValidator, setSelectedValidator }) {
  const [fetchedValidatorList, setFetchedValidatorList] = useState([]);

  // TODO: Change to nomination pool
  // useEffect(() => {
  //   const getValidatorList = async () => {
  //     const response = await fetch('https://rest-api.substake.app/api/request/dev/validator', {
  //       method: 'POST',
  //       headers: {
  //         'Content-type': 'application/json',
  //       },
  //     });
  //     const result = await response.json();
  //     console.log(result);
  //     setFetchedValidatorList(result);
  //   };

  //   getValidatorList();
  // }, []);

  const scrollViewRef = useRef();

  return (
    <Modal
      transparent={true}
      animationType="slide"
      visible={modalVisible}
      onRequestClose={() => setModalVisible(!modalVisible)}
    >
      <Pressable style={styles.modalOverlay} onPress={() => setModalVisible(false)}>
        <Pressable style={styles.modalContent}>
          <View style={{ justifyContent: 'space-between', flex: 1 }}>
            <View style={{ marginHorizontal: 25, marginBottom: 10 }}>
              <Text style={styles.modalTitle}>Select a Nomination Pool</Text>
              <Text style={styles.modalMain}>Do you have a specific pool you want to join?</Text>
              <TextInput
                autoCapitalize="none"
                style={styles.modalTextInput}
                placeholder="명칭, 주소, 혹은 계좌 인덱스로 필터링합니다."
              />
              <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
                <Text style={styles.tableHeader}>Open Pools</Text>
                <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
                  <Text style={{ ...styles.tableHeader, marginLeft: 15 }}>Points</Text>
                  <Text style={{ ...styles.tableHeader, marginLeft: 15 }}>Nominees</Text>
                </View>
              </View>
            </View>
            <ScrollView ref={scrollViewRef}>
              {fetchedValidatorList.map((el, i) => (
                <Pressable
                  key={i}
                  onPress={() => setSelectedValidator(el.display_name)}
                  onStartShouldSetResponder={() => true}
                  style={{
                    flexDirection: 'row',
                    justifyContent: 'space-between',
                    paddingHorizontal: 25,
                    backgroundColor: selectedValidator === el.display_name ? '#93A2F1' : 'white',
                  }}
                >
                  <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
                    <Text style={{ ...styles.tableMain, marginRight: 10 }}>{i + 1}</Text>
                    <Text style={styles.tableMain}>{el.display_name}</Text>
                  </View>
                  <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
                    <Text style={styles.tableMain}>{el.total.toFixed(3)}WND</Text>
                    <Text style={{ ...styles.tableMain }}>{el.own.toFixed(3)}</Text>
                  </View>
                </Pressable>
              ))}
            </ScrollView>
            <Pressable
              style={selectedValidator ? styles.confirmButton : styles.closeButton}
              onPress={() => setModalVisible(false)}
            >
              <Text style={{ color: selectedValidator ? '#ffffff' : 'black' }}>
                {selectedValidator ? 'Confirm' : 'Close'}
              </Text>
            </Pressable>
          </View>
        </Pressable>
      </Pressable>
    </Modal>
  );
}

const styles = StyleSheet.create({
  modalOverlay: {
    width: '100%',
    height: '100%',
    alignItems: 'center',
    justifyContent: 'flex-end',
    backgroundColor: 'rgba(0,0,0,0.7)',
  },
  modalContent: {
    backgroundColor: 'white',
    paddingVertical: 25,
    alignSelf: 'stretch',
    height: '65%',
  },
  modalTitle: {
    fontSize: 15,
  },
  modalMain: {
    marginTop: 15,
    fontSize: 10,
    color: '#7E7794',
  },
  modalTextInput: {
    marginTop: 5,
    marginBottom: 15,
    borderColor: '#AAAAAA',
    borderWidth: 1,
    borderStyle: 'solid',
    padding: 5,
    borderRadius: 5,
    fontSize: 10,
  },
  tableHeader: {
    fontSize: 10,
    color: '#7E7794',
  },
  tableMain: {
    fontSize: 10,
    marginRight: 20,
    marginVertical: 10,
  },
  closeButton: {
    alignSelf: 'stretch',
    justifyContent: 'center',
    alignItems: 'center',
    height: 30,
    backgroundColor: '#E7E7E7',
  },
  confirmButton: {
    alignSelf: 'stretch',
    justifyContent: 'center',
    alignItems: 'center',
    height: 30,
    backgroundColor: '#2745E2',
  },
});
