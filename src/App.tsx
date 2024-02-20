import React, { useState } from "react";
import styled from "styled-components";
import MainBox from "./components/MainBox";
import MainBackground from "./img/main_background.png";
import TitleBar from "./components/TitleBar";
import PredictBtn from "./components/PredictBtn";

const MainPage = styled.div`
  width: 100%;
  height: 100%;
  overflow: hidden;
  position: relative;
`;

const Container = styled.div`
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

  const resetMainBox = () => {
    setKey((prevKey) => prevKey + 1); // 키 값을 변경하여 MainBox를 초기화
  };

  const handleUpload = () => {
    // 다른 파일 업로드 버튼 클릭 시 실행되는 함수
    // 필요한 로직을 구현
  };

  return (
    <>
      <MainPage>
        <TitleBar />
        <Container>
          <MainBox key={key} resetMainBox={resetMainBox} />
          <PredictBtn resetMainBox={resetMainBox} handleUpload={handleUpload} />
        </Container>
      </MainPage>
    </>
  );
}

export default App;