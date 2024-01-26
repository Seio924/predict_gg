import React, { useState } from "react";
import ReactDOM from "react-dom/client";
import styled from "styled-components";
import MainBox from "./components/MainBox";
import MainBackground from "./img/main_background.png";
import TitleBar from "./components/TitleBar";

const MainPage = styled.div`
  width: 100%;
  height: 100%;
  overflow: hidden;
  position: relative;
`;

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  background-image: url(${MainBackground});
  background-size: cover;
  width: 100%;
  height: calc(100% - 56px);
`;

function App() {
  return (
    <>
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
