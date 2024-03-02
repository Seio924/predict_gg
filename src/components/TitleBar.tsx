import React from "react";
import styled from "styled-components";
import {
  SEND_WINDOW_MINIMIZE,
  SEND_WINDOW_MAXIMIZE,
  SEND_WINDOW_CLOSE,
} from "../constants";
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

interface WindowIconContainerProps {
  backgroundcolor?: string;
  onClick?: (handleType: string) => void;
}

interface WindowIconProps {
  bgimg?: string;
  margin?: string;
}

function TitleBar() {
  const { ipcRenderer } = window.require("electron");

  const handleWindow = (handleType: string) => {
    console.log("1");
    if (handleType === "minimizeApp") {
      ipcRenderer.send(SEND_WINDOW_MINIMIZE, "send");
    } else if (handleType === "maximizeApp") {
      ipcRenderer.send(SEND_WINDOW_MAXIMIZE, "send");
    } else if (handleType === "closeApp") {
      ipcRenderer.send(SEND_WINDOW_CLOSE, "send");
    }
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
    </>
  );
}

export default TitleBar;
