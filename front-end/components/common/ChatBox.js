import { StyleSheet } from 'react-native';

export const commonStyle = StyleSheet.create({
  serviceChatContainer: {
    alignSelf: 'stretch',
    alignItems: 'flex-start',
    marginBottom: 15,
    marginTop: 15,
  },
  userChatContainer: {
    alignSelf: 'stretch',
    alignItems: 'flex-end',
    marginBottom: 15,
  },
  serviceChatBox: {
    backgroundColor: 'rgba(52, 55, 129, 0.63)',
    borderRadius: 10,
    maxWidth: '70%',
    padding: 20,
  },
  serviceChatBoxTitle: {
    color: 'white',
    fontSize: 11,
  },
  serviceChatBoxDesc: {
    color: '#A8A8A8',
    fontSize: 10,
    marginTop: 8,
  },
  userChatBox: {
    backgroundColor: 'rgba(217, 218, 234, 0.76)',
    borderRadius: 10,
    maxWidth: '60%',
    padding: 13,
  },
  userChatBoxText: {
    color: 'black',
    fontSize: 12,
    lineHeight: 20,
  },
  textInput: {
    flex: 1,
    color: '#A8A8A8',
  },
  confirm: {
    margin: 2,
    color: '#6C84FF',
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    // marginTop: 20,
  },
  buttonWrapper: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  buttonContainer: {
    alignSelf: 'stretch',
    paddingVertical: 5,
    paddingHorizontal: 15,
    backgroundColor: 'rgba(108, 132, 255, 0.2)',
    justifyContent: 'center',
    alignItems: 'flex-start',
    marginTop: 5,
  },
  checkedButtonContainer: {
    alignSelf: 'stretch',
    paddingVertical: 5,
    paddingHorizontal: 15,
    backgroundColor: '#26F2A9',
    justifyContent: 'center',
    alignItems: 'flex-start',
    marginTop: 5,
  },
  buttonText: {
    color: 'white',
    fontSize: 11,
  },
  checkedButtonText: {
    color: 'black',
    fontSize: 11,
  },
  succesContainer: {
    flexDirection: 'row',
    flex: 1,
    backgroundColor: 'rgba(52, 55, 129, 0.63)',
    borderRadius: 10,
    width: '65%',
    paddingVertical: 20,
    alignItems: 'center',
    justifyContent: 'space-evenly',
  },
  successHeader: {
    color: '#26F2A9',
  },
  successMain: {
    color: 'white',
    fontSize: 10,
  },
  successLink: {
    fontSize: 10,
    color: '#3959FF',
  },
  divider: {
    marginVertical: 8,
  },
  sliderContainer: {
    justifyContent: 'center',
    backgroundColor: '#383537',
    borderRadius: 5,
    height: 24,
  },
  disabledSliderContainer: {
    justifyContent: 'center',
    backgroundColor: '#212351',
    borderRadius: 5,
    height: 24,
  },
  sliderBox: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 10,
    borderRadius: 5,
    height: 20,
    backgroundColor: 'rgba(217, 218, 234, 0.76)',
  },
  sliderInnerText: {
    color: '#FFFFFF',
    fontSize: 8,
  },
  cardContainer: {
    flexDirection: 'row',
  },
  cardBox: {
    height: 250,
    width: 250,
    backgroundColor: 'rgba(52, 55, 129, 0.63)',
    marginRight: 25,
  },
  cardTextWrapper: {
    padding: 10,
    flex: 1,
    justifyContent: 'space-between',
  },
  cardMainText: {
    color: 'white',
    fontSize: 11,
    // marginBottom: 15,
  },
  cardSubText: {
    color: '#A8A8A8',
    fontSize: 10,
  },
  cardImg: {
    width: 250,
  },
});
