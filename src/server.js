const express = require("express");
const bodyParser = require("body-parser");
const { getSummonerInfo } = require("../backend/riot_api.js"); // 수정된 부분

const app = express();
const port = 4000;

app.use(bodyParser.json());

app.post("/", (req, res) => {
  let match_id = req.body.data;
  match_id = match_id.split(".")[0];
  match_id = match_id.substring(0, 2) + "_" + match_id.substring(3); // 문자열 일부를 변경
  console.log("클라이언트에서 매치아이디:", match_id);

  // getSummonerInfo 함수를 호출하고, 그 결과를 처리합니다.
  getSummonerInfo(match_id)
    .then((result) => {
      res.send({ message: "I am server data complete" });
    })
    .catch((error) => {
      console.error("getSummonerInfo 호출 중 에러 발생:", error);
      res.status(500).send({ error: "Internal Server Error" });
    });
});

app.listen(port, () => {
  console.log(`서버가 포트 ${port}에서 실행 중입니다.`);
});
