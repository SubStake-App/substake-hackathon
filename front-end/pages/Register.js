import { useState, useRef, useContext } from 'react';
import { View, Text, TextInput, Pressable, ScrollView } from 'react-native';
import { commonStyle } from '../components/common/ChatBox';
import { Divider } from '@rneui/base';
import { derivePrivateKey } from '../components/utils';
import { AsyncStorageContext } from '../components/Context/AsyncStorage';

export default function Register() {
  const { addAccount } = useContext(AsyncStorageContext);
  const [status, setStatus] = useState(0);
  const [mnemonic, setMnemonic] = useState('');
  const [nickname, setNickname] = useState('');
  const [publicKey, setPublicKey] = useState('');

  const scrollViewRef = useRef();

  const deriveAndPostPrivateKey = async () => {
    const result = derivePrivateKey(mnemonic);
    if (result.type === 'sr25519') setPublicKey(result.address);
    else setPublicKey(result.publicKey);
    setStatus(1);
  };

  const storeAccount = async () => {
    try {
      addAccount({ publicKey, nickname });
      console.log('hi');
    } catch {}
  };

  return (
    <>
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
                    autoCapitalize="none"
                    style={commonStyle.textInput}
                    placeholderTextColor="#A8A8A8"
                    placeholder="시드문구"
                    onChangeText={(text) => setMnemonic(text)}
                    editable={status === 0}
                    autoCorrect={false}
                  />
                  <Pressable onPress={deriveAndPostPrivateKey} disabled={status !== 0}>
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
                <Text style={commonStyle.userChatBoxText}>{publicKey}</Text>
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
                        autoCapitalize="none"
                        style={commonStyle.textInput}
                        placeholderTextColor="#A8A8A8"
                        placeholder="ex) David"
                        onChangeText={(text) => setNickname(text)}
                        editable={status === 1}
                        autoCorrect={false}
                      />
                      <Pressable onPress={storeAccount} disabled={status !== 1}>
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
          <View style={commonStyle.userChatContainer}>
            <View style={commonStyle.userChatBox}>
              <Text style={commonStyle.userChatBoxText}>{nickname}</Text>
            </View>
          </View>
        )}
      </ScrollView>
    </>
  );
}
