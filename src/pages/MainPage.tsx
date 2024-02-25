import React, { useState } from "react";
import styled from "styled-components";
import MainBox from "../components/MainBox";
import PredictBtnContainer from "../components/PredictBtnContainer";

interface IProps {
  resetMainBox: () => void;
  handleUpload: () => void;
}

function MainPage({ resetMainBox, handleUpload }: IProps) {
  return (
    <>
      <MainBox resetMainBox={resetMainBox} />
      <PredictBtnContainer
        resetMainBox={resetMainBox}
        handleUpload={handleUpload}
      />
    </>
  );
}

export default MainPage;
