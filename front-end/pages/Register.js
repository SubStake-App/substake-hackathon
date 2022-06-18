import { useState, useRef } from 'react';
import { View, Text, TextInput, Pressable, ScrollView } from 'react-native';
import { commonStyle } from '../components/common/ChatBox';
import Layout from '../components/Layout';
import { Divider } from '@rneui/base';
import LoadingModal from '../components/LoadingModal';

export default function Register({ navigation }) {
  const [pending, setPending] = useState(false);
  const [status, setStatus] = useState(0);
  const [seed, setSeed] = useState('');
  const [nickname, setNickname] = useState('');
  const [password, setPassword] = useState('');
  const [passwordReCheck, setPasswordReCheck] = useState('');

  const scrollViewRef = useRef();

  const loadAndNavigate = async () => {
    setPending(true);
    await new Promise((r) => setTimeout(r, 2000));
    setPending(false);
    navigation.navigate('Home');
  };

  return (
    <Layout>
      {pending && <LoadingModal />}
      <ScrollView
        showsVerticalScrollIndicator={false}
        ref={scrollViewRef}
        onContentSizeChange={() => scrollViewRef.current.scrollToEnd({ animated: true })}
      >
        <View style={commonStyle.serviceChatContainer}>
          <View style={commonStyle.serviceChatBox}>
            <Text style={commonStyle.serviceChatBoxTitle}>시드문구로 계정을 복구해주세요</Text>
            <Text style={commonStyle.serviceChatBoxDesc}>서비스 시작을 위해 처음 한 번만 복구하시면 됩니다.</Text>
            {status === 0 && (
              <>
                <Divider style={commonStyle.divider} color="rgba(65, 69, 151, 0.8)" />
                <View style={commonStyle.inputContainer}>
                  <TextInput
                    style={commonStyle.textInput}
                    placeholderTextColor="#A8A8A8"
                    placeholder="시드문구"
                    onChangeText={(text) => setSeed(text)}
                    editable={status === 0}
                    autoCorrect={false}
                  />
                  <Pressable onPress={() => setStatus(1)} disabled={status !== 0}>
                    <Text style={commonStyle.confirm}>확인</Text>
                  </Pressable>
                </View>
              </>
            )}
          </View>
        </View>
        {status > 0 && (
          <>
            <View style={commonStyle.userChatContainer}>
              <View style={commonStyle.userChatBox}>
                <Text style={commonStyle.userChatBoxText}>{seed}</Text>
              </View>
            </View>
            <View style={commonStyle.serviceChatContainer}>
              <View style={commonStyle.serviceChatBox}>
                <Text style={commonStyle.serviceChatBoxTitle}>계정 닉네임을 설정해주세요</Text>
                <Text style={commonStyle.serviceChatBoxDesc}>닉네임은 언제든 수정 가능합니다.</Text>
                {status === 1 && (
                  <>
                    <Divider style={commonStyle.divider} color="rgba(65, 69, 151, 0.8)" />
                    <View style={commonStyle.inputContainer}>
                      <TextInput
                        style={commonStyle.textInput}
                        placeholderTextColor="#A8A8A8"
                        placeholder="ex) David"
                        onChangeText={(text) => setNickname(text)}
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
          </>
        )}
        {status > 1 && (
          <>
            <View style={commonStyle.userChatContainer}>
              <View style={commonStyle.userChatBox}>
                <Text style={commonStyle.userChatBoxText}>{nickname}</Text>
              </View>
            </View>
            <View style={commonStyle.serviceChatContainer}>
              <View style={commonStyle.serviceChatBox}>
                <Text style={commonStyle.serviceChatBoxTitle}>비밀번호 재설정이 필요해요.</Text>
                <Text style={commonStyle.serviceChatBoxDesc}>비밀번호는 추후 시드문구로만 재설정할 수 있습니다.</Text>
                {status === 2 && (
                  <>
                    <Divider style={commonStyle.divider} color="rgba(65, 69, 151, 0.8)" />
                    <View style={commonStyle.inputContainer}>
                      <TextInput
                        style={commonStyle.textInput}
                        placeholderTextColor="#A8A8A8"
                        placeholder="Password"
                        secureTextEntry={true}
                        onChangeText={(text) => setPassword(text)}
                        editable={status === 2}
                      />
                      <Pressable onPress={() => setStatus(3)} disabled={status !== 2}>
                        <Text style={commonStyle.confirm}>확인</Text>
                      </Pressable>
                    </View>
                  </>
                )}
              </View>
            </View>
          </>
        )}
        {status > 2 && (
          <View style={commonStyle.serviceChatContainer}>
            <View style={commonStyle.serviceChatBox}>
              <Text style={commonStyle.serviceChatBoxTitle}>비밀번호 재확인이 필요해요</Text>
              <Text style={commonStyle.serviceChatBoxDesc}>방금 입력하신 비밀번호를 한 번 더 입력합니다.</Text>
              <Divider style={commonStyle.divider} color="rgba(65, 69, 151, 0.8)" />
              <View style={commonStyle.inputContainer}>
                <TextInput
                  style={commonStyle.textInput}
                  placeholderTextColor="#A8A8A8"
                  placeholder="Password"
                  secureTextEntry={true}
                  onChangeText={(text) => setPasswordReCheck(text)}
                  editable={status === 3}
                />
                <Pressable onPress={loadAndNavigate} disabled={status !== 3}>
                  <Text style={commonStyle.confirm}>확인</Text>
                </Pressable>
              </View>
            </View>
          </View>
        )}
      </ScrollView>
    </Layout>
  );
}
