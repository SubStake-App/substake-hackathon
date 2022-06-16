import { useRef, useState, useEffect } from 'react';
import { Image, ScrollView, Text, View, TextInput, Pressable } from 'react-native';
import { commonStyle } from '../../components/common/ChatBox';
import Layout from '../../components/Layout';
import TopBar from '../../components/TopBar/TopBar';
import img_1 from '../../assets/nominator_1.png';
import img_2 from '../../assets/nominator_2.png';
import img_3 from '../../assets/nominator_3.png';
import { Divider } from '@rneui/base';
import Slider from 'react-native-slide-to-unlock';
import success from '../../assets/success.png';
import { openBrowserAsync, WebBrowserPresentationStyle } from 'expo-web-browser';
import arrowRight from '../../assets/arrowRightBold.png';

export default function WestendNominator({ navigation }) {
  const [status, setStatus] = useState(0);
  const [bondAmount, setBondAmount] = useState(0);
  const [isDisabled, setIsDisabled] = useState(false);
  const [validatorFilter, setValidatorFilter] = useState([]);
  const [interestType, setInterestType] = useState('');
  const scrollViewRef = useRef();

  const cardContent = [
    {
      main: 'After showing your intent to bond your asset, your nomination takes 24 hours(1era) to come in to effect, and it takes 7 eras to completely unstake your fund.',
      sub: 'Note: Nominators should be only be able to see a SINGLE (our of the validators selected by you) active nomination per era.',
      img: img_1,
    },
    {
      main: 'Only the state of TOP 22,500 nominators out of nominator intentions (up to 50,000) is considered as the electing set to determine the active validators.',
      sub: 'Note: ONLY the state of TOP 256 nominatrors of each Active Validator is eligible for the staking reward.',
      img: img_2,
    },
    {
      main: 'Nominator’s account(or a “voter” will be automatically semi-sorted into a bag of 16 voter-list, based on the amount the voter nominates.',
      sub: 'SubStake App will automatically support you to adjust “moveUp” and “re-bag” extrinsics on behalf of you.',
      img: img_3,
    },
  ];

  useEffect(() => {
    setValidatorFilter([
      { filter: 'One validator per operator', isChecked: false },
      { filter: 'Commission rate under 10%', isChecked: false },
      { filter: 'Number of nominators under 256', isChecked: false },
      { filter: 'Rewards payout with regular basis', isChecked: false },
      { filter: 'Currently elected at least in 3 days', isChecked: false },
      { filter: 'With an onchain-identity', isChecked: false },
      { filter: 'No slashing historical record', isChecked: false },
      { filter: 'Average block rate above 4', isChecked: false },
    ]);
  }, []);

  return (
    <Layout>
      <TopBar title="Nominator" path="StakableAssets" navigation={navigation} />
      <ScrollView
        showsVerticalScrollIndicator={false}
        ref={scrollViewRef}
        onContentSizeChange={() => scrollViewRef.current.scrollToEnd({ animated: true })}
      >
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
            <Text style={commonStyle.serviceChatBoxTitle}>추가하실 스테이킹 수량을 입력해주세요.</Text>
            <Text style={commonStyle.serviceChatBoxDesc}>현재 전송가능 잔고: 253.2124 WND</Text>
            <Divider style={commonStyle.divider} color="rgba(65, 69, 151, 0.8)" />
            <View style={commonStyle.inputContainer}>
              <TextInput
                keyboardType="decimal-pad"
                style={commonStyle.textInput}
                placeholderTextColor="#A8A8A8"
                placeholder="숫자만 입력해주세요"
                onChangeText={(amount) => setBondAmount(amount)}
                editable={status === 0}
                autoCorrect={false}
              />
              <Pressable onPress={() => setStatus(1)} disabled={status !== 0}>
                <Text style={commonStyle.confirm}>확인</Text>
              </Pressable>
            </View>
          </View>
        </View>
        {status > 0 && (
          <>
            <View style={commonStyle.userChatContainer}>
              <View style={commonStyle.userChatBox}>
                <Text style={commonStyle.userChatBoxText}>{bondAmount}</Text>
              </View>
            </View>
            <View style={commonStyle.serviceChatContainer}>
              <View style={commonStyle.serviceChatBox}>
                <Text style={commonStyle.serviceChatBoxTitle}>벨리데이터 최소 기준을 필터링 해주세요</Text>
                <Text style={commonStyle.serviceChatBoxDesc}>
                  지나치게 엄격한 기준은 Validator 생태계에 건강하지 못하므로 최대 6가지 기준만 선택 가능하십니다.
                </Text>
                <Divider style={commonStyle.divider} color="rgba(65, 69, 151, 0.8)" />
                <View style={commonStyle.buttonWrapper}>
                  {validatorFilter.map((el, i) => (
                    <Pressable
                      key={i}
                      style={el.isChecked ? commonStyle.checkedButtonContainer : commonStyle.buttonContainer}
                      disabled={status !== 1}
                      onPress={() =>
                        setValidatorFilter(
                          validatorFilter.map((filter, j) =>
                            i === j ? { ...filter, isChecked: !filter.isChecked } : filter
                          )
                        )
                      }
                    >
                      <Text style={el.isChecked ? commonStyle.checkedButtonText : commonStyle.buttonText}>
                        {el.filter}
                      </Text>
                    </Pressable>
                  ))}
                </View>
                <Divider style={commonStyle.divider} />
                <Slider
                  onEndReached={() => {
                    setStatus(2);
                    setIsDisabled(true);
                  }}
                  containerStyle={isDisabled ? commonStyle.disabledSliderContainer : commonStyle.sliderContainer}
                  sliderElement={
                    <View style={commonStyle.sliderBox}>
                      <Image source={arrowRight} />
                    </View>
                  }
                  disableSliding={isDisabled}
                >
                  <Text style={commonStyle.sliderInnerText}>
                    {isDisabled ? 'confirmed' : 'Swipe to confirm the your filters'}
                  </Text>
                </Slider>
              </View>
            </View>
          </>
        )}
        {status > 1 && (
          <>
            <View style={commonStyle.userChatContainer}>
              <View style={commonStyle.userChatBox}>
                <Text style={commonStyle.userChatBoxText}>Confirmed</Text>
              </View>
            </View>
            <View style={commonStyle.serviceChatContainer}>
              <View style={commonStyle.serviceChatBox}>
                <Text style={commonStyle.serviceChatBoxTitle}>스테이킹 리워드 단리/복리 설정</Text>
                <Text style={commonStyle.serviceChatBoxDesc}>
                  단리: 리워드는 즉시 전송가능 상태로 표시됩니다. 복리: 리워드는 자동으로 재-스테이킹 됩니다.
                </Text>
                <Divider style={commonStyle.divider} color="rgba(65, 69, 151, 0.8)" />
                <View style={commonStyle.buttonWrapper}>
                  <Pressable
                    style={
                      interestType === 'Compound' ? commonStyle.checkedButtonContainer : commonStyle.buttonContainer
                    }
                    onPress={() => {
                      setStatus(3);
                      setInterestType('Compound');
                    }}
                    disabled={status !== 2}
                  >
                    <Text style={interestType === 'Compound' ? commonStyle.checkedButtonText : commonStyle.buttonText}>
                      Compound
                    </Text>
                  </Pressable>
                  <Pressable
                    style={interestType === 'Simple' ? commonStyle.checkedButtonContainer : commonStyle.buttonContainer}
                    onPress={() => {
                      setStatus(3);
                      setInterestType('Simple');
                    }}
                    disabled={status !== 2}
                  >
                    <Text style={interestType === 'Simple' ? commonStyle.checkedButtonText : commonStyle.buttonText}>
                      Simple
                    </Text>
                  </Pressable>
                </View>
              </View>
            </View>
          </>
        )}
        {status > 2 && (
          <View style={commonStyle.userChatContainer}>
            <View style={commonStyle.userChatBox}>
              <Text style={commonStyle.userChatBoxText}>{interestType}</Text>
            </View>
          </View>
        )}
      </ScrollView>
    </Layout>
  );
}
