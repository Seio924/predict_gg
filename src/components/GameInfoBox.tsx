import styled from "styled-components";

const WholeArea = styled.div`
  display: flex;
  height: 290px;
  width: 540px;
  background-color: #1e2023;
  border-radius: 5px;
`;

const Container = styled.div`
  display: flex;
  width: 100%;
  height: 250px;
  margin: 20px;
`;

const TeamContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
  height: 100%;
`;
const VSContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`;

const InfoContainer = styled.div`
  display: flex;
  align-items: center;
  margin-left: 20px;
`;

const ChampionImg = styled.div<{ imageUrl?: string }>`
  width: 32px;
  height: 32px;
  background-image: url(${(props) => props.imageUrl});
  background-size: cover;
  margin-right: 10px;
`;

const ChampionInfos = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
`;

const SummonerName = styled.p`
  font-size: 15px;
  font-weight: 900;
  color: white;
`;

const KDA = styled.p`
  font-size: 10px;
  font-weight: 900;
  color: white;
`;

interface IProps {
  championName?: string[];
  summonerName?: string[];
  teamId?: number[];
  assists?: number[];
  deaths?: number[];
  kills?: number[];
}

function GameInfoBox({
  championName,
  summonerName,
  teamId,
  assists,
  deaths,
  kills,
}: IProps) {
  const team1 = [0, 1, 2, 3, 4];
  const team2 = [5, 6, 7, 8, 9];

  console.log(championName);

  return (
    <>
      <WholeArea>
        <Container>
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
            <SummonerName>VS</SummonerName>
          </VSContainer>

          <TeamContainer>
            {team2.map((index) => (
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
        </Container>
      </WholeArea>
    </>
  );
}

export default GameInfoBox;