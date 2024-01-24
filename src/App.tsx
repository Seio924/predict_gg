import React, { useState } from "react";
import ReactDOM from "react-dom/client";
import GlobalStyle from "./GlobalStyle";
import styled from "styled-components";
import MainBox from "./components/MainBox";
import MainBackground from "./img/main_background.png";
import TitleBar from "./components/TitleBar";
import { DEFAULT_WINDOW, MAX_WINDOW } from "./constants";

const MainPage = styled.div<Size>`
  width: ${(props) => props.widthsize};
  height: ${(props) => props.heightsize};
`;

const Container = styled.div<Size>`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: ${(props) => props.widthsize};
  height: ${(props) => props.heightsize};
  background-image: url(${MainBackground});
  background-size: cover;
`;

interface Size {
  widthsize?: string;
  heightsize?: string;
}

function App() {
  const [mainPageWidth, setMainPageWidth] = useState("1072px");
  const [mainPageHeight, setMainPageHeight] = useState("659px");
  const [containerWidth, setContainerWidth] = useState("1072px");
  const [containerHeight, setContainerHeight] = useState("603px");
  const { ipcRenderer } = window.require("electron");

  ipcRenderer.on(DEFAULT_WINDOW, (event, arg) => {
    console.log("1111");
    setMainPageWidth("1072px");
    setMainPageHeight("659px");
    setContainerWidth("1072px");
    setContainerHeight("603px");
  });

  ipcRenderer.on(MAX_WINDOW, (event, arg) => {
    console.log("2222");
    setMainPageWidth("100vh");
    setMainPageHeight("100vh");
    setContainerWidth("100%");
    setContainerHeight("100%");
  });

  return (
    <>
      <GlobalStyle />
      <MainPage widthsize={mainPageWidth} heightsize={mainPageHeight}>
        <TitleBar />
        <Container widthsize={containerWidth} heightsize={containerHeight}>
          <MainBox />
        </Container>
      </MainPage>
    </>
  );
}

export default App;
