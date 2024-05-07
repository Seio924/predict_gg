import React, { useState } from "react";
import styled from "styled-components";
import GameInfoBox from "../components/GameInfoBox";
import Chart from "../components/Chart";
import PredictTagBox from "../components/PredictTagBox";
import AkaliImg from "../img/akali.png";

const BoxContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 493px;
  width: 918px;
  background-color: rgba(30, 32, 35, 0.9);
  border-radius: 6px;
`;

const SubContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
`;

const TagContainer = styled.div`
  width: 100%;
  display: flex;
  justify-content: space-around;
`;

const TCContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-left: 20px;
`;

const CharacterImg = styled.div`
  width: 200px;
  height: 200px;
  background-image: url(${AkaliImg});
  background-size: cover;
`;

const Title = styled.p`
  color: #eeeeef;
  font-size: 20px;
  margin-bottom: 20px;
  font-family: PretendardBold;
`;

function PredictResultPage() {
  return (
    <>
      <BoxContainer>
        <SubContainer>
          <Chart />
        </SubContainer>
        <TagContainer>
          <TCContainer>
            <Title>5% 이상 승률이 변화하는 구간</Title>
            <CharacterImg />
          </TCContainer>
          <PredictTagBox />
        </TagContainer>
      </BoxContainer>
    </>
  );
}

export default PredictResultPage;
