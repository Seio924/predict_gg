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
  padding: 13px 20px 13px 20px;
  -webkit-app-region: drag;
`;

const TitleContainer = styled.div`
  display: flex;
  align-items: center;
`;

const Title = styled.p`
  font-size: 18px;
  font-weight: 800;
  color: white;
`;

const LolTitle = styled.div`
  width: 70px;
  height: 30px;
  background-image: url(${LolTitleImg});
  background-size: cover;
`;

const Select = styled(TitleContainer)``;

const WindowIcon = styled.div<WindowIconProps>`
  width: 12px;
  height: 12px;
  margin: ${(props) => props.margin};
  background-image: url(${(props) => props.bgimg});
  background-size: cover;
`;

interface WindowIconProps {
  bgimg?: string;
  margin?: string;
  onClick?: (handleType: string) => void;
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
          <WindowIcon
            onClick={() => handleWindow("minimizeApp")}
            bgimg={WindowMinimizeIcon}
            margin={"0 0 0 20px"}
          />
          <WindowIcon
            onClick={() => handleWindow("maximizeApp")}
            bgimg={WindowMaximizeIcon}
            margin={"0 0 0 20px"}
          />
          <WindowIcon
            onClick={() => handleWindow("closeApp")}
            bgimg={WindowCloseIcon}
            margin={"0 0 0 20px"}
          />
        </Select>
      </TitleBarContainer>
    </>
  );
}

export default TitleBar;
