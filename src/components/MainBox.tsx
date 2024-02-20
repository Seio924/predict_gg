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

function MainBox({ resetMainBox }: { resetMainBox: () => void }) {
  const [isActive, setActive] = useState(false);
  const [fileName, setFileName] = useState("");
  const [championName, setChampionName] = useState<string[]>([]);
  const [summonerName, setSummonerName] = useState<string[]>([]);
  const [teamId, setTeamId] = useState<number[]>([]);
  const [assists, setAssists] = useState<number[]>([]);
  const [deaths, setDeaths] = useState<number[]>([]);
  const [kills, setKills] = useState<number[]>([]);

  const { ipcRenderer } = window.require("electron");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;

    if (files && files.length > 0) {
      const uploadedFileName = files[0].name;
      const fileExtension = uploadedFileName.split(".").pop();
      if (fileExtension === "rofl") {
        setFileName(uploadedFileName);
        ipcRenderer.send(SEND_MAIN_PING, { fileName: uploadedFileName });
        setActive(false);
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
      const fileExtension = droppedFileName.split(".").pop();
      if (fileExtension === "rofl") {
        setFileName(droppedFileName);
        ipcRenderer.send(SEND_MAIN_PING, { fileName: droppedFileName });
        setActive(false);
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
        {championName.length === 0 ? (
          <UploadArea
            isActive={isActive}
            onDragOver={(e) => {
              e.preventDefault();
              e.stopPropagation();
            }}
            onDrop={(e) => handleDrop(e)}
            onDragEnter={() => setActive(true)}
            onDragLeave={() => setActive(false)}
          >
            <FileUploadBtn type="file" onChange={(e) => handleFileChange(e)} />
            <UploadIcon />
            <FileUploadText>{fileName ? fileName : "Upload HERE"}</FileUploadText>
          </UploadArea>
        ) : (
          <GameInfoBox
            championName={championName}
            summonerName={summonerName}
            teamId={teamId}
            assists={assists}
            deaths={deaths}
            kills={kills}
          />
        )}
      </BoxContainer>
    </>
  );
}

export default MainBox;