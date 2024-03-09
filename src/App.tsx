import React, { useState } from "react";
import styled from "styled-components";
import MainBox from "./components/MainBox";
import MainBackground from "./img/main_background.png";
import TitleBar from "./components/TitleBar";
import PredictBtnContainer from "./components/PredictBtnContainer";
import MainPage from "./pages/MainPage";
import { useRecoilState, useRecoilValue, useSetRecoilState } from "recoil";
import {
  setResultPageActiveState,
  showMainPageState,
  winningRateState,
} from "./atom";
import PredictResultPage from "./pages/PredictResultPage";
import Loading from "./components/Loading";
import { PREDICT_OVER } from "./constants";

const Container = styled.div`
  width: 100%;
  height: 100%;
  overflow: hidden;
  position: relative;
`;

const BoxContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 493px;
  width: 918px;
  background-color: rgba(30, 32, 35, 0.9);
  border-radius: 6px;
`;

const LoadingText = styled.p`
  color: #eeeeef;
  font-family: PretendardBold;
  font-size: 15px;
`;

const BackGroundContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-image: url(${MainBackground});
  background-size: cover;
  width: 100%;
  height: calc(100% - 56px);
`;

function App() {
  const [key, setKey] = useState(0); // 키 값을 변경하여 MainBox를 초기화
  const showMainPage = useRecoilValue(showMainPageState);
  const setWinningRate = useSetRecoilState(winningRateState);
  const [resultPageActive, setResultPageActive] = useRecoilState(
    setResultPageActiveState
  );
  const { ipcRenderer } = window.require("electron");

  ipcRenderer.on(PREDICT_OVER, (event, arg) => {
    setResultPageActive(true);
    setWinningRate(arg.predict_data);
  });

  const resetMainBox = () => {
    setKey((prevKey) => prevKey + 1); // 키 값을 변경하여 MainBox를 초기화
  };

  const handleUpload = () => {
    // 다른 파일 업로드 버튼 클릭 시 실행되는 함수
    // 필요한 로직을 구현
  };

  return (
    <>
      <Container>
        <TitleBar />
        <BackGroundContainer>
          {showMainPage ? (
            <MainPage
              resetMainBox={resetMainBox}
              handleUpload={handleUpload}
              key={key}
            />
          ) : resultPageActive ? (
            <PredictResultPage />
          ) : (
            <BoxContainer>
              <Loading />
              <LoadingText></LoadingText>
            </BoxContainer>
          )}
        </BackGroundContainer>
      </Container>
    </>
  );
}

export default App;
