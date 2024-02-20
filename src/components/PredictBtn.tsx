import React, { useState, useEffect } from "react";
import styled, { css } from "styled-components";
import { SEND_MATCH_INFO, SEND_PREDICT_GAME } from "../constants";

const ButtonContainer = styled.div`
  display: flex;
  justify-content: flex-end;
  width: 580px;
`;

const Button = styled.div<{ isActive: boolean }>`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 45px;
  width: 280px;
  border-radius: 7px;
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
  &:first-child {
    margin-right: 18px;
  }
`;

const BtnText = styled.p`
  font-size: 20px;
  font-weight: 600;
  color: #eeeeef;
`;

interface PredictBtnProps {
  resetMainBox: () => void;
  // 다른 파일 업로드 시 MainBox를 초기화하는 함수
  handleUpload: () => void;
  // 다른 파일 업로드 버튼 클릭 시 실행되는 함수
}

const PredictBtn: React.FC<PredictBtnProps> = ({
  resetMainBox,
  handleUpload,
}) => {
  const [isActive, setActive] = useState(false);

  useEffect(() => {
    const ipcRenderer = window.require("electron").ipcRenderer;
    ipcRenderer.on(SEND_MATCH_INFO, (event, arg) => {
      setActive(true);
    });

    return () => {
      ipcRenderer.removeAllListeners(SEND_MATCH_INFO);
    };
  }, []);

  const onClick = () => {
    const ipcRenderer = window.require("electron").ipcRenderer;
    if (!isActive) {
      alert("리플레이 파일을 선택해주세요.");
    } else {
      alert("good");
      ipcRenderer.send(SEND_PREDICT_GAME);
    }
  };

  const onUploadClick = () => {
    resetMainBox(); // MainBox를 초기화하기 위해 전달된 함수 호출
    handleUpload(); // 다른 파일 업로드 버튼 클릭 시 실행되는 함수 호출
    setActive(false); // Predict Now 버튼을 초기화하기 위해 isActive를 false로 설정

    // 오버레이 프로세스 종료
    const ipcRenderer = window.require("electron").ipcRenderer;
    ipcRenderer.send("stopOverlayProcess");
  };

  return (
    <ButtonContainer>
      {/* 왼쪽에 추가할 버튼 */}
      <Button isActive={false} onClick={onUploadClick}>
        <BtnText>다른 파일 업로드</BtnText>
      </Button>
      <Button isActive={isActive} onClick={onClick}>
        <BtnText>Predict Now</BtnText>
      </Button>
    </ButtonContainer>
  );
};

export default PredictBtn;