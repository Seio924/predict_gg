import React, { useState } from "react";
import styled from "styled-components";
import Lottie from "react-lottie";
import LoadingIcon from "../img/loading_icon.json";

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
      <Lottie
        options={defaultOptions}
        height={200}
        width={200}
        isClickToPauseDisabled={true}
      />
    </>
  );
}

export default Loading;
