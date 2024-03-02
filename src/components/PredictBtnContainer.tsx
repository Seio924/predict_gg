import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { SEND_MATCH_INFO, SEND_PREDICT_GAME } from "../constants";
import Modal from "react-modal";
import Button from "./Button";
import { useSetRecoilState, useRecoilState } from "recoil";
import {
  showMainPageState,
  championNameState,
  summonerNameState,
  teamIdState,
  assistsState,
  deathsState,
  killsState,
} from "../atom";

const ButtonContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 580px;
`;

const SelectNumberContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const SelectBox = styled.select`
  width: 300px;
  height: 30px;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 5px;
  border: none;
  outline: none;
  color: #eeeeef;
  background-color: #1e2023;

  option {
    font-size: 15px;
    font-family: PretendardLight, sans-serif;
    border: none;
    color: #eeeeef;
    background-color: #1e2023;
  }
`;

const SelectBtnContainer = styled.div`
  display: flex;
  width: 300px;
  margin-top: 10px;
`;

const SelectNumberText = styled.p`
  font-size: 18px;
  font-family: PretendardSemiBold, sans-serif;
  color: #eeeeef;
  margin-bottom: 23px;
`;

const customModalStyle = {
  content: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    width: "370px",
    height: "160px",
    borderRadius: "8px",
    margin: "auto",
    backgroundColor: "rgba(50, 53, 57, 0.96)",
    border: "none",
  },
  overlay: {
    backgroundColor: "rgba(0, 0, 0, 0.5)",
  },
};

interface PredictBtnProps {
  resetMainBox?: () => void;
  handleUpload?: () => void;
}

function PredictBtnContainer({ resetMainBox, handleUpload }: PredictBtnProps) {
  const [isActive, setActive] = useState(false);
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [userInput, setUserInput] = useState("");
  const setShowMainPage = useSetRecoilState(showMainPageState);
  const [championName, setChampionName] = useRecoilState(championNameState);
  const [summonerName, setSummonerName] = useRecoilState(summonerNameState);
  const [teamId, setTeamId] = useRecoilState(teamIdState);
  const [assists, setAssists] = useRecoilState(assistsState);
  const [deaths, setDeaths] = useRecoilState(deathsState);
  const [kills, setKills] = useRecoilState(killsState);

  const options = [
    { value: "5", label: "5초" },
    { value: "10", label: "10초" },
    { value: "30", label: "30초" },
    { value: "60", label: "60초" },
  ];

  useEffect(() => {
    const ipcRenderer = window.require("electron").ipcRenderer;
    ipcRenderer.on(SEND_MATCH_INFO, (event, arg) => {
      setActive(true);
    });

    return () => {
      ipcRenderer.removeAllListeners(SEND_MATCH_INFO);
    };
  }, []);

  const onClick = () => {
    if (!isActive) {
      alert("리플레이 파일을 선택해주세요.");
    } else {
      openModal();
    }
  };

  const onUploadClick = () => {
    resetMainBox && resetMainBox();
    handleUpload && handleUpload();
    setActive(false);
    setChampionName([]);
    setSummonerName([]);
    setTeamId([]);
    setAssists([]);
    setDeaths([]);
    setKills([]);

    const ipcRenderer = window.require("electron").ipcRenderer;
    ipcRenderer.send("stopOverlayProcess");
  };

  const openModal = () => {
    setModalIsOpen(true);
  };

  const closeModal = () => {
    setModalIsOpen(false);
  };

  const handleSubmit = () => {
    const ipcRenderer = window.require("electron").ipcRenderer;
    const fs = window.require("fs");

    if (userInput.trim() === "") {
      alert("입력한 숫자: " + "10");
      setShowMainPage(false);
      fs.writeFileSync("backend/userInput.txt", "10");
      ipcRenderer.send(SEND_PREDICT_GAME);
      setActive(false);
    } else {
      if (!isNaN(Number(userInput))) {
        alert("입력한 숫자: " + userInput);
        setShowMainPage(false);
        fs.writeFileSync("backend/userInput.txt", userInput);
        ipcRenderer.send(SEND_PREDICT_GAME);
        setActive(false);
      } else {
        alert("숫자를 입력하세요.");
      }
    }

    setUserInput("");
    closeModal();
  };

  const handleSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setUserInput(e.target.value);
  };

  return (
    <ButtonContainer>
      <Button
        btnColor={false}
        onClick={onUploadClick}
        textSize="20px"
        textFont="PretendardBold, sans-serif"
      >
        다른 파일 업로드
      </Button>
      <Button
        btnColor={isActive}
        onClick={onClick}
        textSize="20px"
        textFont="PretendardBold, sans-serif"
      >
        Predict Now
      </Button>
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        style={customModalStyle}
      >
        <SelectNumberContainer>
          <SelectNumberText>숫자를 입력하세요</SelectNumberText>
          <SelectBox onChange={handleSelectChange} defaultValue="10">
            {options.map((option) => (
              <option key={option.value} value={option.value} defaultValue="10">
                {option.label}
              </option>
            ))}
          </SelectBox>
          <SelectBtnContainer>
            <Button
              height="35px"
              textSize="14px"
              textFont="PretendardMedium, sans-serif"
              onClick={closeModal}
            >
              Cancel
            </Button>
            <Button
              height="35px"
              btnColor={true}
              onClick={handleSubmit}
              textSize="14px"
              textFont="PretendardMedium, sans-serif"
            >
              Submit
            </Button>
          </SelectBtnContainer>
        </SelectNumberContainer>
      </Modal>
    </ButtonContainer>
  );
}

export default PredictBtnContainer;
