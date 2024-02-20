import styled, { css } from "styled-components";
import React, { useState } from "react";
import { SEND_MATCH_INFO, SEND_PREDICT_GAME } from "../constants";

const Button = styled.div<{ isActive: boolean }>`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 45px;
  width: 580px;
  border-radius: 7px;
  margin-top: 15px;
  cursor: pointer;
  ${(props) =>
    props.isActive
      ? css`
          background-image: linear-gradient(
            265deg,
            rgba(24, 200, 255, 0.7),
            rgba(147, 63, 254, 0.7)
          );
        `
      : css`
          background-image: linear-gradient(
            265deg,
            rgba(198, 197, 197, 0.7),
            rgba(91, 90, 90, 0.7)
          );
        `};
`;

const BtnText = styled.p`
  font-size: 20px;
  font-weight: 600;
  color: #eeeeef;
`;

function PredictBtn() {
  const [isActive, setActive] = useState(false);

  const { ipcRenderer } = window.require("electron");

  ipcRenderer.on(SEND_MATCH_INFO, (event, arg) => {
    // SET isActive based on your logic
    setActive(true);
  });

  const onClick = () => {
    if (isActive == false) {
      alert("리플레이 파일을 선택해주세요.");
    } else {
      alert("good");
      const { ipcRenderer } = window.require("electron");
      ipcRenderer.send(SEND_PREDICT_GAME, {send_text:"predict_game!"});
    }
  };

  return (
    <>
      <Button isActive={isActive} onClick={onClick}>
        <BtnText>Predict Now</BtnText>
      </Button>
    </>
  );
}

export default PredictBtn;
