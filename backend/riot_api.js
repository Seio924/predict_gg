const request = require("request");
const fs = require("fs");

const apiKey = "RGAPI-59ffd1a9-2677-40b0-be5d-24151cd90ec9";

function getSummonerInfo(matchId) {
  return new Promise((resolve, reject) => {
    const apiUrl = `https://asia.api.riotgames.com/lol/match/v5/matches/${matchId}?api_key=${apiKey}`;
    const apiUrl2 = `https://asia.api.riotgames.com/lol/match/v5/matches/${matchId}/timeline?api_key=${apiKey}`;

    request(apiUrl, (error, response, body) => {
      if (error) {
        reject(error);
      } else {
        try {
          const summonerInfo = JSON.parse(body);
          console.log("riot_api complete");

          // 파일에 기록
          fs.writeFileSync(
            "backend/api_match_info.json",
            JSON.stringify(summonerInfo, null, 2)
          );

          resolve(summonerInfo);
        } catch (parseError) {
          reject(parseError);
        }
      }
    });

    request(apiUrl2, (error, response, body) => {
      if (error) {
        reject(error);
      } else {
        try {
          const summonerInfo = JSON.parse(body);
          console.log("riot_api complete");

          // 파일에 기록
          fs.writeFileSync(
            "backend/api_timeline_info.json",
            JSON.stringify(summonerInfo, null, 2)
          );

          resolve(summonerInfo);
        } catch (parseError) {
          reject(parseError);
        }
      }
    });
  });
}

module.exports = {
  getSummonerInfo,
};
