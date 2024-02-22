const request = require("request");
const fs = require("fs");

const apiKey = "RGAPI-3ec05947-04f7-4650-a49a-0c4b0e5d1b1f";

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

          request(apiUrl2, (error2, response2, body2) => {
            if (error2) {
              reject(error2);
            } else {
              try {
                const timelineInfo = JSON.parse(body2);
                console.log("riot_timeline_api complete");

                // 파일에 기록
                fs.writeFileSync(
                  "../backend/api_match_info.json",
                  JSON.stringify(summonerInfo, null, 2)
                );

                // 파일에 기록
                fs.writeFileSync(
                  "../backend/api_timeline_info.json",
                  JSON.stringify(timelineInfo, null, 2)
                );

                // 두 요청 모두 완료되면 resolve 호출
                resolve({ matchInfo: summonerInfo, timelineInfo });
              } catch (parseError2) {
                reject(parseError2);
              }
            }
          });
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
