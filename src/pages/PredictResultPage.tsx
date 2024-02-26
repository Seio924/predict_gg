import React, { useState } from "react";
import styled from "styled-components";
import GameInfoBox from "../components/GameInfoBox";
import Chart from "../components/Chart";

const BoxContainer = styled.div`
  display: flex;
  height: 493px;
  width: 918px;
  background-color: rgba(30, 32, 35, 0.9);
  border-radius: 6px;
`;

const SubContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 20px;
`;

function PredictResultPage() {
  return (
    <>
      <BoxContainer>
        <SubContainer>
          <GameInfoBox />
          <Chart />
        </SubContainer>
      </BoxContainer>
    </>
  );
}

export default PredictResultPage;
