import React, { useState } from "react";
import styled from "styled-components";
import UploadingIcon from "./img/uploading_icon.png";
import LolTitleImg from "./img/lol_title.png";
import { SEND_MAIN_PING } from './constants'; 

const BoxContainer = styled.div`
  position: relative;
  height: 250px;
  width: 500px;
  background-color: lightgray;
`;

const LolTitle = styled.div`
  position: absolute;
  width: 220px;
  height: 100px;
  top: 30px;
  background-image: url(${LolTitleImg});
  background-size: cover;
`;

const UploadArea = styled.label`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
`;

const FileUploadBtn = styled.input`
  display: none;
`;

const UploadIcon = styled.div`
  width: 50px;
  height: 60px;
  margin-bottom: 20px;
  background-image: url(${UploadingIcon});
  background-size: cover;
`;

const FileUploadText = styled.p`
  font-size: 25px;
  font-weight: 900;
`;

function MainBox() {
  const { ipcRenderer } = window.require("electron"); 
  const sendMail = () => { 
    ipcRenderer.send(SEND_MAIN_PING, 'send'); 
  } 
  return (
    <>
      <LolTitle />
      <BoxContainer>
        <UploadArea>
          <FileUploadBtn type="file" />
          <UploadIcon />
          <FileUploadText>Upload HERE</FileUploadText>
          <button onClick={ sendMail }>Send Mail</button> 
        </UploadArea>
      </BoxContainer>
    </>
  );
}

export default MainBox;
