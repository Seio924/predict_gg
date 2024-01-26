const request = require('request');
const fs = require('fs');

const apiKey = 'RGAPI-a54a9866-026e-4264-9543-d74029f333d0';

function getSummonerInfo(matchId) {
  return new Promise((resolve, reject) => {
    const apiUrl = `https://asia.api.riotgames.com/lol/match/v5/matches/${matchId}/timeline?api_key=${apiKey}`;

    request(apiUrl, (error, response, body) => {
      if (error) {
        reject(error);
      } else {
        try {
          const summonerInfo = JSON.parse(body);
          console.log("riot_api complete");

          // 파일에 기록
          fs.writeFileSync('backend/api_info.json', JSON.stringify(summonerInfo, null, 2));

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
