import React, { useState } from "react";
import styled from "styled-components";
import UploadingIcon from "../img/uploading_icon.png";
import { SEND_MAIN_PING } from "../constants";

const BoxContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 330px;
  width: 580px;
  background-color: rgba(30, 32, 35, 0.7);
  border-radius: 10px;
`;

const UploadArea = styled.label<{ isActive: boolean }>`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 290px;
  width: 540px;
  background-color: #1e2023;
  border-radius: 5px;
  border: 3px dashed #1e2023;
  cursor: pointer;

  &:hover {
    border-color: lightgray;
  }

  ${(props) =>
    props.isActive &&
    `
    background-color: #323539;
    border-color: lightgray;
  `}
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
  color: white;
`;

function MainBox() {
  const [isActive, setActive] = useState(false);
  const handleDragStart = () => setActive(true);
  const handleDragEnd = () => setActive(false);
  const handleDragOver = (e: React.DragEvent<HTMLLabelElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };
  const handleDrop = (e: React.DragEvent<HTMLLabelElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const { ipcRenderer } = window.require("electron");

  const sendMail = () => {
    ipcRenderer.send(SEND_MAIN_PING, "send");
  };

  return (
    <>
      <BoxContainer>
        <UploadArea
          isActive={isActive}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          onDragEnter={handleDragStart}
          onDragLeave={handleDragEnd}
        >
          <FileUploadBtn type="file" />
          <UploadIcon />
          <FileUploadText>Upload HERE</FileUploadText>
        </UploadArea>
      </BoxContainer>
      <button onClick={sendMail}>Send Mail</button>
    </>
  );
}

export default MainBox;
