import React, { useState } from "react";
import styled from "styled-components";
import UploadingIcon from "../img/uploading_icon.png";

const BoxContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 330px;
  width: 580px;
  background-color: rgba(30, 32, 35, 0.7);
  border-radius: 10px;
`;

const UploadArea = styled.label`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 290px;
  width: 540px;
  background-color: #1e2023;
  border-radius: 10px;
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
  return (
    <>
      <BoxContainer>
        <UploadArea>
          <FileUploadBtn type="file" />
          <UploadIcon />
          <FileUploadText>Upload HERE</FileUploadText>
        </UploadArea>
      </BoxContainer>
    </>
  );
}

export default MainBox;
