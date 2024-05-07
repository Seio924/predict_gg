import React, { useState } from "react";
import styled from "styled-components";
import {
  SEND_WINDOW_MINIMIZE,
  SEND_WINDOW_MAXIMIZE,
  SEND_WINDOW_CLOSE,
} from "../constants";
import Modal from "react-modal";
import Button from "./Button";
import WindowCloseIcon from "../img/window_close_icon.png";
import WindowMinimizeIcon from "../img/window_minimize_icon.png";
import WindowMaximizeIcon from "../img/window_maximize_icon.png";
import LolTitleImg from "../img/lol_title.png";
import XIcon from "../img/x_icon.png";

const TitleBarContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  grid-template-rows: auto 1fr;
  background: #000000;
  padding: 0 0 0 20px;
`;

const Title = styled.p`
  font-size: 18px;
  font-family: PretendardBold;
  color: white;
`;

const LolTitle = styled.div`
  width: 70px;
  height: 30px;
  background-image: url(${LolTitleImg});
  background-size: cover;
`;

const Select = styled.div`
  display: flex;
  align-items: center;
`;

const TitleContainer = styled(Select)`
  -webkit-app-region: drag;
  flex: 1 0 auto;
`;

const WindowIconContainer = styled.div<WindowIconContainerProps>`
  width: 56px;
  height: 56px;
  display: flex;
  justify-content: center;
  align-items: center;

  &:hover {
    background: ${(props) => props.backgroundcolor};
  }
`;

const WindowIcon = styled.div<WindowIconProps>`
  width: 12px;
  height: 12px;
  margin: ${(props) => props.margin};
  background-image: url(${(props) => props.bgimg});
  background-size: cover;
`;

const ModalContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const BtnContainer = styled.div`
  display: flex;
  width: 300px;
  margin-top: 15px;
`;

const QText = styled.p`
  font-size: 18px;
  font-family: PretendardSemiBold, sans-serif;
  color: #eeeeef;
  margin-bottom: 15px;
`;

const customModalStyle = {
  content: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    width: "350px",
    height: "140px",
    borderRadius: "8px",
    margin: "auto",
    backgroundColor: "rgba(50, 53, 57, 0.96)",
    border: "none",
  },
  overlay: {
    backgroundColor: "rgba(0, 0, 0, 0.5)",
  },
};

interface WindowIconContainerProps {
  backgroundcolor?: string;
  onClick?: (handleType: string) => void;
}

interface WindowIconProps {
  bgimg?: string;
  margin?: string;
}

function TitleBar() {
  const [modalIsOpen, setModalIsOpen] = useState(false);

  const { ipcRenderer } = window.require("electron");

  const handleWindow = (handleType: string) => {
    console.log("1");
    if (handleType === "minimizeApp") {
      ipcRenderer.send(SEND_WINDOW_MINIMIZE, "send");
    } else if (handleType === "maximizeApp") {
      ipcRenderer.send(SEND_WINDOW_MAXIMIZE, "send");
    } else if (handleType === "closeApp") {
      openModal();
    }
  };

  const closeApp = () => {
    ipcRenderer.send(SEND_WINDOW_CLOSE, "send");
  };

  const openModal = () => {
    setModalIsOpen(true);
  };

  const closeModal = () => {
    setModalIsOpen(false);
  };

  return (
    <>
      <TitleBarContainer>
        <TitleContainer>
          <Title>PredictGG</Title>
          <WindowIcon bgimg={XIcon} margin={"0 10px 0 10px"} />
          <LolTitle />
        </TitleContainer>

        <Select>
          <WindowIconContainer
            backgroundcolor="gray"
            onClick={() => handleWindow("minimizeApp")}
          >
            <WindowIcon bgimg={WindowMinimizeIcon} />
          </WindowIconContainer>
          <WindowIconContainer
            backgroundcolor="gray"
            onClick={() => handleWindow("maximizeApp")}
          >
            <WindowIcon bgimg={WindowMaximizeIcon} />
          </WindowIconContainer>
          <WindowIconContainer
            backgroundcolor="red"
            onClick={() => handleWindow("closeApp")}
          >
            <WindowIcon bgimg={WindowCloseIcon} />
          </WindowIconContainer>
        </Select>
      </TitleBarContainer>
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        style={customModalStyle}
      >
        <ModalContainer>
          <QText>Predict.GG를 닫으시겠습니까?</QText>
          <BtnContainer>
            <Button
              height="35px"
              textSize="14px"
              textFont="PretendardMedium, sans-serif"
              onClick={closeModal}
              margin="15px 18px 0 0"
            >
              취소
            </Button>
            <Button
              height="35px"
              btnColor={true}
              onClick={closeApp}
              textSize="14px"
              textFont="PretendardMedium, sans-serif"
              margin="15px 0 0 0"
            >
              종료
            </Button>
          </BtnContainer>
        </ModalContainer>
      </Modal>
    </>
  );
}

export default TitleBar;
