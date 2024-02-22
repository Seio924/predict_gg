import React, { useState } from "react";
import styled from "styled-components";
import Lottie from "react-lottie";
import LoadingIcon from "../img/loading_icon.json";

const LoadingContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 290px;
  width: 540px;
  background-color: #1e2023;
  border-radius: 6px;
  border: 3px dashed #1e2023;
`;

function Loading() {
  const defaultOptions = {
    loop: true,
    autoplay: true,
    animationData: LoadingIcon,
    rendererSettings: {
      preserveAspectRatio: "xMidYMid slice",
    },
  };
  return (
    <>
      <LoadingContainer>
        <Lottie
          options={defaultOptions}
          height={130}
          width={130}
          isClickToPauseDisabled={true}
        />
      </LoadingContainer>
    </>
  );
}

export default Loading;
