const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 4000;

app.use(bodyParser.json());

app.post('/', (req, res) => {
    console.log('클라이언트에서 온 데이터:', req.body.data);

    // 여기서 적절한 응답을 보내줍니다.
    res.send({ message: 'I am server data complete' });
});

app.listen(port, () => {
    console.log(`서버가 포트 ${port}에서 실행 중입니다.`);
});
