import { useRef, useState, useEffect } from 'react';
import { Image, ScrollView, Text, View, TextInput, Pressable, Modal } from 'react-native';
import { commonStyle } from '../../components/common/ChatBox';
import Layout from '../../components/Layout';
import TopBar from '../../components/TopBar/TopBar';
import img_1 from '../../assets/nomination_pool_1.png';
import img_2 from '../../assets/nomination_pool_2.png';
import img_3 from '../../assets/nomination_pool_3.png';
import { Divider } from '@rneui/base';
import Slider from 'react-native-slide-to-unlock';
import success from '../../assets/success.png';
import { openBrowserAsync, WebBrowserPresentationStyle } from 'expo-web-browser';
import arrowRight from '../../assets/arrowRightBold.png';
import { NominationPoolModal } from '../../components/Westend/NominationPool/Modal';

const cardContent = [
  {
    main: 'A member delegates funds to a pool by transferring some amount to the pool’s bonded account with the “join” extrinsic.',
    sub: 'Note: A member is afforded the ability to bond additional funds, or re-stake rewards as long as they are already actively bonded. Remeber, a member may only belong to one pool at a time.',
    img: img_1,
  },
  {
    main: 'The member can claim their portion of any rewards that have accumulated since the previous time they claimed (or in the case that they have never claimed, any rewards that have accumulated since the era after they joined). Rewards are split pro rata among the actively bonded members.',
    sub: '',
    img: img_2,
  },
  {
    main: "At any point in time after joining the pool, a member can start the process of exiting by unbonding. unbond will unbond part or all of the member's funds.",
    sub: 'The unbonding duration has passed (e.g. 28 days on Polkadot), a member may withdraw their funds with withdraw unbonded',
    img: img_3,
  },
];

export default function WestendNominationPool({ navigation }) {
  const [status, setStatus] = useState(0);
  const [action, setAction] = useState('');
  const [bondAmount, setBondAmount] = useState(0);
  const [selectedValidator, setSelectedValidator] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);
  const scrollViewRef = useRef();

  return (
    <Layout>
      <TopBar title="Nomination Pool" path="StakableAssets" navigation={navigation} />
      <ScrollView
        showsVerticalScrollIndicator={false}
        ref={scrollViewRef}
        onContentSizeChange={() => scrollViewRef.current.scrollToEnd({ animated: true })}
      >
        <NominationPoolModal
          modalVisible={modalVisible}
          setModalVisible={setModalVisible}
          selectedValidator={selectedValidator}
          setSelectedValidator={setSelectedValidator}
        />
        <ScrollView horizontal={true}>
          <View style={commonStyle.cardContainer}>
            {cardContent.map((el, i) => (
              <View style={commonStyle.cardBox} key={i}>
                <Image source={el.img} style={commonStyle.cardImg} />
                <View style={commonStyle.cardTextWrapper}>
                  <Text style={commonStyle.cardMainText}>{el.main}</Text>
                  <Text style={commonStyle.cardSubText}>{el.sub}</Text>
                </View>
              </View>
            ))}
          </View>
        </ScrollView>
        <View style={commonStyle.serviceChatContainer}>
          <View style={commonStyle.serviceChatBox}>
            <Text style={commonStyle.serviceChatBoxTitle}>Do you want to join SubStake Pool?</Text>
            <Text style={commonStyle.serviceChatBoxDesc}>If no, you can manually select a pool.</Text>
            {status === 0 && (
              <>
                <Divider style={commonStyle.divider} color="rgba(65, 69, 151, 0.8)" />
                <View style={commonStyle.buttonWrapper}>
                  <Pressable
                    style={commonStyle.buttonContainer}
                    onPress={() => {
                      setStatus(1);
                      setAction(() => 'substake');
                    }}
                    disabled={status !== 0}
                  >
                    <Text style={commonStyle.buttonText}>Yes, please</Text>
                  </Pressable>
                  <Pressable
                    style={commonStyle.buttonContainer}
                    onPress={() => {
                      setStatus(1);
                      setAction(() => 'manual');
                    }}
                    disabled={status !== 0}
                  >
                    <Text style={commonStyle.buttonText}>No, I want to select manually</Text>
                  </Pressable>
                </View>
              </>
            )}
          </View>
        </View>
        {action === 'substake' && status > 0 && (
          <>
            <View style={commonStyle.userChatContainer}>
              <View style={commonStyle.userChatBox}>
                <Text style={commonStyle.userChatBoxText}>Yes, please</Text>
              </View>
            </View>
            <View style={commonStyle.serviceChatContainer}>
              <View style={commonStyle.serviceChatBox}>
                <Text style={commonStyle.serviceChatBoxTitle}>추가하실 스테이킹 수량을 입력해주세요.</Text>
                <Text style={commonStyle.serviceChatBoxDesc}>현재 전송가능 잔고: 253.2124 WND</Text>
                {status === 1 && (
                  <>
                    <Divider style={commonStyle.divider} color="rgba(65, 69, 151, 0.8)" />
                    <View style={commonStyle.inputContainer}>
                      <TextInput
                        keyboardType="decimal-pad"
                        style={commonStyle.textInput}
                        placeholderTextColor="#A8A8A8"
                        placeholder="숫자만 입력해주세요"
                        onChangeText={(amount) => setBondAmount(amount)}
                        editable={status === 1}
                        autoCorrect={false}
                      />
                      <Pressable onPress={() => setStatus(2)} disabled={status !== 1}>
                        <Text style={commonStyle.confirm}>확인</Text>
                      </Pressable>
                    </View>
                  </>
                )}
              </View>
            </View>
            {status > 1 && (
              <>
                <View style={commonStyle.userChatContainer}>
                  <View style={commonStyle.userChatBox}>
                    <Text style={commonStyle.userChatBoxText}>{bondAmount}</Text>
                  </View>
                </View>
                <View style={commonStyle.serviceChatContainer}>
                  <View style={commonStyle.succesContainer}>
                    <Image source={success} />
                    <View>
                      <Text style={commonStyle.successHeader}>Success</Text>
                      <View style={{ flexDirection: 'row' }}>
                        <Text style={commonStyle.successMain}>Your Extrinsic tx-id:</Text>
                        <Pressable
                          onPress={() =>
                            openBrowserAsync('https://moonbase.subscan.io/extrinsic/2298472-4', {
                              presentationStyle: WebBrowserPresentationStyle.POPOVER,
                            })
                          }
                        >
                          <Text style={commonStyle.successLink}> #2275958-3</Text>
                        </Pressable>
                      </View>
                    </View>
                  </View>
                </View>
              </>
            )}
          </>
        )}
        {action === 'manual' && status > 0 && (
          <>
            <View style={commonStyle.userChatContainer}>
              <View style={commonStyle.userChatBox}>
                <Text style={commonStyle.userChatBoxText}>No, I want to select manually</Text>
              </View>
            </View>
            <View style={commonStyle.serviceChatContainer}>
              <View style={commonStyle.serviceChatBox}>
                <Text style={commonStyle.serviceChatBoxTitle}>Which pool are you looking for?</Text>
                {!selectedValidator && (
                  <>
                    <Divider style={commonStyle.divider} color="rgba(65, 69, 151, 0.8)" />
                    <View style={commonStyle.buttonWrapper}>
                      <Pressable
                        style={commonStyle.buttonContainer}
                        onPress={() => setModalVisible(true)}
                        disabled={status !== 1}
                      >
                        <Text style={commonStyle.buttonText}>Select a Nomination Pool</Text>
                      </Pressable>
                    </View>
                  </>
                )}
              </View>
            </View>
            {selectedValidator && (
              <>
                <View style={commonStyle.userChatContainer}>
                  <View style={commonStyle.userChatBox}>
                    <Text style={commonStyle.userChatBoxText}>{selectedValidator}</Text>
                  </View>
                </View>
                <View style={commonStyle.serviceChatContainer}>
                  <View style={commonStyle.serviceChatBox}>
                    <Text style={commonStyle.serviceChatBoxTitle}>차감하실 스테이킹 수량을 입력해주세요</Text>
                    <Text style={commonStyle.serviceChatBoxDesc}>현재 스테이킹 수량: 25253.2124 WND</Text>
                    {status === 1 && (
                      <>
                        <Divider style={commonStyle.divider} color="rgba(65, 69, 151, 0.8)" />
                        <View style={commonStyle.inputContainer}>
                          <TextInput
                            keyboardType="decimal-pad"
                            style={commonStyle.textInput}
                            placeholderTextColor="#A8A8A8"
                            placeholder="숫자만 입력해주세요"
                            onChangeText={(amount) => setBondAmount(amount)}
                            editable={status === 1}
                            autoCorrect={false}
                          />
                          <Pressable onPress={() => setStatus(2)} disabled={status !== 1}>
                            <Text style={commonStyle.confirm}>확인</Text>
                          </Pressable>
                        </View>
                      </>
                    )}
                  </View>
                </View>
                {status > 1 && (
                  <>
                    <View style={commonStyle.userChatContainer}>
                      <View style={commonStyle.userChatBox}>
                        <Text style={commonStyle.userChatBoxText}>{bondAmount}</Text>
                      </View>
                    </View>
                    <View style={commonStyle.serviceChatContainer}>
                      <View style={commonStyle.succesContainer}>
                        <Image source={success} />
                        <View>
                          <Text style={commonStyle.successHeader}>Success</Text>
                          <View style={{ flexDirection: 'row' }}>
                            <Text style={commonStyle.successMain}>Your Extrinsic tx-id:</Text>
                            <Pressable
                              onPress={() =>
                                openBrowserAsync('https://moonbase.subscan.io/extrinsic/2298472-4', {
                                  presentationStyle: WebBrowserPresentationStyle.POPOVER,
                                })
                              }
                            >
                              <Text style={commonStyle.successLink}> #2275958-3</Text>
                            </Pressable>
                          </View>
                        </View>
                      </View>
                    </View>
                  </>
                )}
              </>
            )}
          </>
        )}
      </ScrollView>
    </Layout>
  );
}
