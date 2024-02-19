import React, { useState } from "react";
import styled from "styled-components";
import UploadingIcon from "../img/uploading_icon.png";
import { SEND_MAIN_PING } from "../constants";
import { SEND_MATCH_INFO } from "../constants";
import GameInfoBox from "./GameInfoBox";
const BoxContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 330px;
  width: 580px;
  background-color: rgba(30, 32, 35, 0.7);
  border-radius: 7px;
`;

const UploadArea = styled.label<{ isActive: boolean }>`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 290px;
  width: 540px;
  background-color: #1e2023;
  border-radius: 7px;
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
  font-size: 23px;
  font-weight: 900;
  color: #eeeeef;
`;

function MainBox() {
  const [isActive, setActive] = useState(false);
  const [fileName, setFileName] = useState("");
  const [championName, setChampionName] = useState([]);
  const [summonerName, setSummonerName] = useState([]);
  const [teamId, setTeamId] = useState([]);
  const [assists, setAssists] = useState([]);
  const [deaths, setDeaths] = useState([]);
  const [kills, setKills] = useState([]);

  const { ipcRenderer } = window.require("electron");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;

    if (files && files.length > 0) {
      const uploadedFileName = files[0].name;
      const fileExtension = uploadedFileName.split(".").pop(); // 파일의 확장자 추출
      if (fileExtension === "rofl") {
        // 확장자가 .rofl인 경우에만 버튼 활성화
        setFileName(uploadedFileName);
        ipcRenderer.send(SEND_MAIN_PING, { fileName: uploadedFileName });
        setActive(false); // 파일이 업로드되면 isActive를 false로 설정하여 스타일 변경 해제
      } else {
        alert("파일 확장자는 .rofl이어야 합니다.");
      }
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLLabelElement>) => {
    e.preventDefault();
    e.stopPropagation();

    const files = e.dataTransfer.files;

    if (files && files.length > 0) {
      const droppedFileName = files[0].name;
      const fileExtension = droppedFileName.split(".").pop(); // 파일의 확장자 추출
      if (fileExtension === "rofl") {
        // 확장자가 .rofl인 경우에만 버튼 활성화
        setFileName(droppedFileName);
        ipcRenderer.send(SEND_MAIN_PING, { fileName: droppedFileName });
        setActive(false); // 파일이 업로드되면 isActive를 false로 설정하여 스타일 변경 해제
      } else {
        alert("파일 확장자는 .rofl이어야 합니다.");
      }
    }
  };

  ipcRenderer.on(SEND_MATCH_INFO, (event, arg) => {
    console.log(arg);
    setChampionName(arg.championNameList);
    setSummonerName(arg.summonerNameList);
    setTeamId(arg.teamIdList);
    setAssists(arg.assistsList);
    setDeaths(arg.deathsList);
    setKills(arg.killsList);
  });

  return (
    <>
      <BoxContainer>
        {championName.length == 0 ? (
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
            <FileUploadBtn type="file" onChange={handleFileChange} />
            <UploadIcon />
            <FileUploadText>
              {fileName ? fileName : "Upload HERE"}
            </FileUploadText>
          </UploadArea>
        ) : (
          <GameInfoBox
            championName={championName}
            summonerName={summonerName}
            teamId={teamId}
            assists={assists}
            deaths={deaths}
            kills={kills}
          ></GameInfoBox>
        )}
      </BoxContainer>
    </>
  );
}

export default MainBox;
