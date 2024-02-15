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
  const [fileName, setFileName] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;

    if (files && files.length > 0) {
      const uploadedFileName = files[0].name;
      const fileExtension = uploadedFileName.split('.').pop(); // 파일의 확장자 추출
      if (fileExtension === 'rofl') { // 확장자가 .rofl인 경우에만 버튼 활성화
          setFileName(uploadedFileName);
          setActive(false); // 파일이 업로드되면 isActive를 false로 설정하여 스타일 변경 해제
      } else {
          alert('파일 확장자는 .rofl이어야 합니다.');
      }
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLLabelElement>) => {
    e.preventDefault();
    e.stopPropagation();

    const files = e.dataTransfer.files;

    if (files && files.length > 0) {
      const droppedFileName = files[0].name;
      setFileName(droppedFileName);
      setActive(false); // 파일이 업로드되면 isActive를 false로 설정하여 스타일 변경 해제
    }
  };

  const { ipcRenderer } = window.require("electron");

  const sendMail = () => {
    if (fileName) {
      ipcRenderer.send(SEND_MAIN_PING, { fileName });
    } else {
      alert('파일을 먼저 업로드해주세요.');
    }
  };

  return (
    <>
      <BoxContainer>
        <UploadArea 
          isActive={isActive}
          onDragOver={(e) => {
            e.preventDefault();
            e.stopPropagation();
          }}
          onDrop={handleDrop}
          onDragEnter={() => setActive(true)}
          onDragLeave={() => setActive(false)}
        >
          <FileUploadBtn
            type="file"
            onChange={handleFileChange}
          />
          <UploadIcon />
          <FileUploadText>{fileName ? fileName : "Upload HERE"}</FileUploadText>
        </UploadArea>
      </BoxContainer>
      <button onClick={sendMail}>파일 업로드</button>
    </>
  );
}

export default MainBox;
