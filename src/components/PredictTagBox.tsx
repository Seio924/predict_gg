import { useRecoilState, useSetRecoilState } from "recoil";
import styled from "styled-components";
import {
  setResultPageActiveState,
  showMainPageState,
  winningRateState,
} from "../atom";
import { useEffect, useState } from "react";
import Button from "./Button";

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const ScrollContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 200px;
  margin-bottom: 11.4px;
`;

const TagContainer = styled.div`
  display: flex;
  flex-grow: 1;
  overflow: auto;
`;

const Tag = styled.div`
  display: flex;
  margin-bottom: 15px;
`;

const TagText = styled.p<{ color?: string }>`
  margin-right: 10px;
  font-family: PretendardMedium;
  font-size: 17px;
  color: ${(props) => (props.color ? props.color : "#eeeeef")};
`;

const TagSubContainer = styled.div`
  display: flex;
  flex-direction: column;
  margin: 0 5px 0 5px;
`;

const GoBackBtn = styled.div`
  display: flex;
  width: 100%;
`;

function PredictTagBox() {
  const [winningRate, setWinningRate] = useRecoilState(winningRateState);
  const setShowMainPage = useSetRecoilState(showMainPageState);
  const [conditionWinningRate, setConditionWinningRate] = useState<number[][]>(
    []
  );
  const setResultPageActive = useSetRecoilState(setResultPageActiveState);

  const changeToTime = (num: number) => {
    let minute = 0;
    let second = 0;
    if (num != 0) {
      minute = parseInt(`${num / 60}`);
      second = num % 60;
    }
    const time =
      String(minute).padStart(2, "0") + ":" + String(second).padStart(2, "0");
    return time;
  };

  const onClickBtn = () => {
    setShowMainPage(true);
    setWinningRate([]);
    setResultPageActive(false);

    const ipcRenderer = window.require("electron").ipcRenderer;
    ipcRenderer.send("stopOverlayProcess");
  };

  useEffect(() => {
    let newConditionWinningRate = [];
    for (let i = 1; i < winningRate.length; i++) {
      const winningRateDiff = Math.abs(
        winningRate[i][1] - winningRate[i - 1][1]
      );
      if (winningRateDiff > 5) {
        newConditionWinningRate.push([
          winningRate[i - 1][0],
          winningRate[i][0],
          winningRate[i - 1][1],
          winningRate[i][1],
          winningRate[i - 1][2],
          winningRate[i][2],
        ]);
      }
    }
    setConditionWinningRate(newConditionWinningRate);
  }, [winningRate]);

  return (
    <>
      <Container>
        <ScrollContainer>
          <TagContainer>
            <TagSubContainer>
              {conditionWinningRate.map((index) => (
                <Tag key={`${index[0]}-${index[1]}`}>
                  <TagText>
                    {changeToTime(index[0]) + " ~ " + changeToTime(index[1])}
                  </TagText>
                </Tag>
              ))}
            </TagSubContainer>
            <TagSubContainer>
              {conditionWinningRate.map((index) => (
                <Tag key={`${index[0]}-${index[1]}`}>
                  <TagText color="#5E82E1">
                    {index[2].toString() + "% > " + index[3].toString() + "%"}
                  </TagText>
                </Tag>
              ))}
            </TagSubContainer>
            <TagSubContainer>
              {conditionWinningRate.map((index) => (
                <Tag key={`${index[0]}-${index[1]}`}>
                  <TagText color="#D64E5B">
                    {index[4].toString() + "% > " + index[5].toString() + "%"}
                  </TagText>
                </Tag>
              ))}
            </TagSubContainer>
          </TagContainer>
        </ScrollContainer>

        <GoBackBtn>
          <Button
            height="35px"
            textSize="14px"
            textFont="PretendardMedium, sans-serif"
            onClick={onClickBtn}
          >
            뒤로가기
          </Button>
        </GoBackBtn>
      </Container>
    </>
  );
}

export default PredictTagBox;
