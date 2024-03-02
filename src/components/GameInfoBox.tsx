import styled from "styled-components";
import { useRecoilValue } from "recoil";
import {
  championNameState,
  summonerNameState,
  teamIdState,
  assistsState,
  deathsState,
  killsState,
} from "../atom";

const Container = styled.div<IProps>`
  display: flex;
  width: 100%;
  height: 250px;
  margin: ${(props) => props.margin || "0px"}; // margin props 추가
`;

const TeamContainer = styled.div<IProps>`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: ${(props) => props.alignDirection || "flex-start"};

  height: 100%;
`;

const VSContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex-grow: 1;
`;

const InfoContainer = styled.div`
  display: flex;
  align-items: center;
`;

const ChampionImg = styled.div<IProps>`
  width: 32px;
  height: 32px;
  background-image: url(${(props) => props.imageUrl});
  background-size: cover;
  margin: 0px 12px 0px 12px;
`;

const ChampionInfos = styled.div<IProps>`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: ${(props) => props.alignDirection || "flex-start"};
`;

const SummonerName = styled.p`
  font-size: 15px;
  font-family: PretendardSemiBold;
  color: white;
`;

const VS = styled.p<IProps>`
  font-size: ${(props) => props.vsSize};
  font-family: sans-serif;
  font-weight: ${(props) => props.vsWeight};
  color: white;
`;

const KDA = styled.p`
  font-size: 10px;
  font-weight: 900;
  color: white;
`;

interface IProps {
  imageUrl?: string;
  alignDirection?: string;
  vsSize?: string;
  vsWeight?: string;
  margin?: string;
}

function GameInfoBox({ vsSize, vsWeight, margin }: IProps) {
  const championName = useRecoilValue(championNameState);
  const summonerName = useRecoilValue(summonerNameState);
  const teamId = useRecoilValue(teamIdState);
  const assists = useRecoilValue(assistsState);
  const deaths = useRecoilValue(deathsState);
  const kills = useRecoilValue(killsState);
  const team1 = [0, 1, 2, 3, 4];
  const team2 = [5, 6, 7, 8, 9];

  console.log(championName);

  return (
    <>
      <Container margin={margin}>
        <TeamContainer>
          {team1.map((index) => (
            <InfoContainer>
              <ChampionImg
                imageUrl={`https://ddragon.leagueoflegends.com/cdn/14.3.1/img/champion/${
                  championName && championName[index]
                }.png`}
              />
              <ChampionInfos>
                <SummonerName>
                  {summonerName && summonerName[index]}
                </SummonerName>
                <KDA>
                  {kills && kills[index]} / {deaths && deaths[index]} /{" "}
                  {assists && assists[index]}
                </KDA>
              </ChampionInfos>
            </InfoContainer>
          ))}
        </TeamContainer>

        <VSContainer>
          <VS vsSize={vsSize} vsWeight={vsWeight}>
            VS
          </VS>
        </VSContainer>

        <TeamContainer alignDirection="flex-end">
          {team2.map((index) => (
            <InfoContainer>
              <ChampionInfos alignDirection="flex-end">
                <SummonerName>
                  {summonerName && summonerName[index]}
                </SummonerName>
                <KDA>
                  {kills && kills[index]} / {deaths && deaths[index]} /{" "}
                  {assists && assists[index]}
                </KDA>
              </ChampionInfos>

              <ChampionImg
                imageUrl={`https://ddragon.leagueoflegends.com/cdn/14.3.1/img/champion/${
                  championName && championName[index]
                }.png`}
              />
            </InfoContainer>
          ))}
        </TeamContainer>
      </Container>
    </>
  );
}

export default GameInfoBox;
