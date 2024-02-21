import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { SEND_MATCH_INFO, SEND_PREDICT_GAME } from "../constants";
import Modal from "react-modal";
import Button from "./Button";

const ButtonContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 580px;
`;

const customModalStyle = {
  content: {
    width: "300px",
    height: "100px",
    margin: "auto",
  },
};

interface PredictBtnProps {
  resetMainBox?: () => void;
  handleUpload?: () => void;
}

function PredictBtn({ resetMainBox, handleUpload }: PredictBtnProps) {
  const [isActive, setActive] = useState(false);
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [userInput, setUserInput] = useState("");

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
    if (!isActive) {
      alert("리플레이 파일을 선택해주세요.");
    } else {
      openModal();
    }
  };

  const onUploadClick = () => {
    resetMainBox && resetMainBox();
    handleUpload && handleUpload();
    setActive(false);

    const ipcRenderer = window.require("electron").ipcRenderer;
    ipcRenderer.send("stopOverlayProcess");
  };

  const openModal = () => {
    setModalIsOpen(true);
  };

  const closeModal = () => {
    setModalIsOpen(false);
  };

  const handleSubmit = () => {
    const ipcRenderer = window.require("electron").ipcRenderer;
    const fs = window.require("fs");
    if (!isNaN(Number(userInput))) {
      alert("입력한 숫자: " + userInput);
      fs.writeFileSync("backend/userInput.txt", userInput);
      ipcRenderer.send(SEND_PREDICT_GAME);
      setActive(false);
    } else {
      alert("숫자를 입력하세요.");
    }
    setUserInput("");
    closeModal();
  };

  return (
    <ButtonContainer>
      <Button btnColor={false} onClick={onUploadClick}>
        다른 파일 업로드
      </Button>
      <Button btnColor={isActive} onClick={onClick}>
        Predict Now
      </Button>
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        style={customModalStyle}
      >
        <div>
          <h2>숫자를 입력하세요</h2>
          <input
            type="number"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
          />
          <button onClick={handleSubmit}>확인</button>
        </div>
      </Modal>
    </ButtonContainer>
  );
}

export default PredictBtn;
