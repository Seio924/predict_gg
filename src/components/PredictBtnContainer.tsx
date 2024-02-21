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

const SelectNumberContainer = styled.div``;

const SelectBox = styled.select`
  width: 200px;
  height: 30px;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 5px;
  font-size: 16px;
  border: none;
  outline: none;
  color: #eeeeef;
  background-color: #1e2023;
`;

const customModalStyle = {
  content: {
    width: "300px",
    height: "100px",
    margin: "auto",
    backgroundColor: "#323539",
    border: "none",
  },
  overlay: {
    backgroundColor: "rgba(0, 0, 0, 0.5)",
  },
};

interface PredictBtnProps {
  resetMainBox?: () => void;
  handleUpload?: () => void;
}

function PredictBtnContainer({ resetMainBox, handleUpload }: PredictBtnProps) {
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
        <SelectNumberContainer>
          <h2>숫자를 입력하세요</h2>
          <SelectBox>
            <option value="option1">5초</option>
            <option value="option1">10초</option>
            <option value="option2">30초</option>
            <option value="option3">60초</option>
          </SelectBox>
          <button onClick={handleSubmit}>확인</button>
        </SelectNumberContainer>
      </Modal>
    </ButtonContainer>
  );
}

export default PredictBtnContainer;
