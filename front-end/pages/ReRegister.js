import { useState, useRef } from 'react';
import { View, Text, TextInput, Pressable, ScrollView } from 'react-native';
import { commonStyle, ConfirmButton, UserChatBox } from '../components/common/ChatBox';
import { Button, Divider } from '@rneui/base';
import { derivePrivateKey } from '../components/utils';
import { useAsyncStorageContext } from '../components/Context/AsyncStorage';
import Layout from '../components/Layout';
import LoadingModal from '../components/LoadingModal';
import TopBar from '../components/TopBar/TopBar';

export default function ReRegister({ navigation }) {
  const { addAccount, accounts } = useAsyncStorageContext();
  const [status, setStatus] = useState(0);
  const [mnemonic, setMnemonic] = useState('');
  const [nickname, setNickname] = useState('');
  const [publicKey, setPublicKey] = useState('');
  const [pending, setPending] = useState(false);
  const [clicked, setClicked] = useState(false);

  const scrollViewRef = useRef();

  const deriveAndPostPrivateKey = () => {
    setClicked(true);
    try {
      const result = derivePrivateKey(mnemonic);

      if (accounts.find((el) => el.publicKey === result.bip39.address)) throw new Error('Account already exist');

      setPublicKey(result);
      setStatus(1);
    } catch (e) {
      console.log(e);
    }
    setClicked(false);
  };

  const storeAccount = async () => {
    setClicked(true);
    setPending(true);
    try {
      await addAccount({ publicKey: publicKey.bip39.address, nickname });
      navigation.navigate('Accounts');
    } catch (e) {
      setPending(false);
    }
  };

  return (
    <Layout>
      <TopBar title="Add account" path="Accounts" navigation={navigation} />
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
                    autoCapitalize="none"
                    style={commonStyle.textInput}
                    placeholderTextColor="#A8A8A8"
                    placeholder="시드문구"
                    onChangeText={(text) => setMnemonic(text)}
                    editable={status === 0}
                    autoCorrect={false}
                  />
                  <ConfirmButton onPress={deriveAndPostPrivateKey} disabled={clicked || status !== 0} />
                </View>
              </>
            )}
          </View>
        </View>
        {status > 0 && (
          <>
            <UserChatBox text={`sr25519: ${publicKey.sr25519.address} bip39: ${publicKey.bip39.address}`} />
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
                      <ConfirmButton onPress={storeAccount} disabled={clicked || status !== 1} />
                    </View>
                  </>
                )}
              </View>
            </View>
          </>
        )}
        {status > 1 && <UserChatBox text={nickname} />}
      </ScrollView>
    </Layout>
  );
}
