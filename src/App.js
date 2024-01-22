import React from "react";
import ReactDOM from "react-dom/client";
import GlobalStyle from "./GlobalStyle";
import styled from "styled-components";
import MainBox from "./MainBox";
import MainBackground from "./img/main_background.png";

const Container = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-image: url(${MainBackground});
  background-size: cover;
`;

function App() {
  return (
    <>
      <GlobalStyle />
      <Container>
        <MainBox></MainBox>
      </Container>
    </>
  );
}

export default App;
