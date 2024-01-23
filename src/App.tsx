import React from "react";
import ReactDOM from "react-dom/client";
import GlobalStyle from "./GlobalStyle";
import styled from "styled-components";
import MainBox from "./components/MainBox";
import MainBackground from "./img/main_background.png";
import TitleBar from "./components/TitleBar";

const MainPage = styled.div`
  width: 1072px;
  height: 659px;
`;

const Container = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 1072px;
  height: 603px;
  background-image: url(${MainBackground});
  background-size: cover;
`;

function App() {
  return (
    <>
      <GlobalStyle />
      <MainPage>
        <TitleBar />
        <Container>
          <MainBox />
        </Container>
      </MainPage>
    </>
  );
}

export default App;
