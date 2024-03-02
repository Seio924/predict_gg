import { useRecoilValue } from "recoil";
import styled from "styled-components";
import { winningRateState } from "../atom";
import { useEffect, useState } from "react";

const Container = styled.div`
  display: flex;
  flex-grow: 1;
  flex-direction: column;
  align-items: center;
`;

const Title = styled.p`
  color: #eeeeef;
  font-size: 20px;
  font-family: PretendardBold;
  margin-bottom: 10px;
`;

const TagContainer = styled.div`
  display: flex;
  flex-direction: column;
`;

const Tag = styled.div`
  display: flex;
`;

const TagText = styled.p<{ color?: string }>`
  margin-right: 10px;
  font-family: PretendardSemiBold;
  font-size: 17px;
  color: ${(props) => (props.color ? props.color : "white")};
`;

const GoBackBtn = styled.div``;

function PredictTagBox() {
  const winningRate = useRecoilValue(winningRateState);
  const [conditionWinningRate, setConditionWinningRate] = useState<number[][]>(
    []
  );

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

  useEffect(() => {
    let newConditionWinningRate = [];
    for (let i = 1; i < winningRate.length; i++) {
      const winningRateDiff = Math.abs(
        winningRate[i][1] - winningRate[i - 1][1]
      );
      if (winningRateDiff > 10) {
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
        <Title>10% 이상 승률이 변화하는 구간</Title>
        <TagContainer>
          {conditionWinningRate.map((index) => (
            <Tag key={`${index[0]}-${index[1]}`}>
              <TagText>
                {changeToTime(index[0]) + " ~ " + changeToTime(index[1])}
              </TagText>
              <TagText color="#5E82E1">
                {index[2].toString() + " > " + index[3].toString()}
              </TagText>
              <TagText color="#D64E5B">
                {index[4].toString() + " > " + index[5].toString()}
              </TagText>
            </Tag>
          ))}
        </TagContainer>
        <GoBackBtn></GoBackBtn>
      </Container>
    </>
  );
}

export default PredictTagBox;
