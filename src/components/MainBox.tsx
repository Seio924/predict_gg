import React, { useState } from "react";
import styled from "styled-components";
import UploadingIcon from "../img/uploading_icon.png";
import { SEND_MAIN_PING, SEND_MATCH_INFO } from "../constants";
import { useRecoilState } from "recoil";
import {
  championNameState,
  summonerNameState,
  teamIdState,
  assistsState,
  deathsState,
  killsState,
} from "../atom";
import GameInfoBox from "./GameInfoBox";
import Loading from "./Loading";

const BoxContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 330px;
  width: 580px;
  background-color: rgba(30, 32, 35, 0.7);
  border-radius: 6px;
`;

const LoadingContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 290px;
  width: 540px;
  background-color: #1e2023;
  border-radius: 6px;
  border: 3px dashed #1e2023;
`;

const UploadArea = styled.label<{ isActive: boolean }>`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 290px;
  width: 540px;
  background-color: #1e2023;
  border-radius: 6px;
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
  width: 37px;
  height: 44.4px;
  margin-bottom: 20px;
  background-image: url(${UploadingIcon});
  background-size: cover;
`;

const FileUploadText = styled.p`
  font-size: 24px;
  font-family: PretendardBold;
  color: #eeeeef;
`;

const GameInfoContainer = styled.div`
  display: flex;
  height: 290px;
  width: 540px;
  background-color: #1e2023;
  border-radius: 6px;
  border: 3px dashed #1e2023;
`;

function MainBox() {
  const [isActive, setActive] = useState(false);
  const [loading, setLoading] = useState(false);
  const [uploadActive, setUploadActive] = useState(true);
  const [championName, setChampionName] = useRecoilState(championNameState);
  const [summonerName, setSummonerName] = useRecoilState(summonerNameState);
  const [teamId, setTeamId] = useRecoilState(teamIdState);
  const [assists, setAssists] = useRecoilState(assistsState);
  const [deaths, setDeaths] = useRecoilState(deathsState);
  const [kills, setKills] = useRecoilState(killsState);

  const { ipcRenderer } = window.require("electron");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;

    if (files && files.length > 0) {
      const uploadedFileName = files[0].name;
      const fileExtension = uploadedFileName.split(".").pop();
      if (fileExtension === "rofl") {
        ipcRenderer.send(SEND_MAIN_PING, { fileName: uploadedFileName });
        setLoading(true);
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
        ipcRenderer.send(SEND_MAIN_PING, { fileName: droppedFileName });
        setLoading(true);
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
    setLoading(false);
    setUploadActive(false);
  });

  return (
    <>
      <BoxContainer>
        {loading ? (
          <LoadingContainer>
            <Loading />
          </LoadingContainer>
        ) : uploadActive ? (
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
            <FileUploadText>Upload HERE</FileUploadText>
          </UploadArea>
        ) : (
          <GameInfoContainer>
            <GameInfoBox vsSize="20px" vsWeight="900" margin="20px" />
          </GameInfoContainer>
        )}
      </BoxContainer>
    </>
  );
}

export default MainBox;
