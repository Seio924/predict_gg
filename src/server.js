const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 4000;

app.use(bodyParser.json());

app.post('/', (req, res) => {
    console.log('클라이언트에서 온 데이터:', req.body.data);
    res.send({ message: 'I am server data complete' });
});

app.listen(port, () => {
    console.log(`서버가 포트 ${port}에서 실행 중입니다.`);
});
