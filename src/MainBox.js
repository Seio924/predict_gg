import React, { useState } from "react";
import styled from "styled-components";
import UploadingIcon from "./img/uploading_icon.png";

const BoxContainer = styled.div`
  height: 250px;
  width: 500px;
  background-color: lightgray;
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
