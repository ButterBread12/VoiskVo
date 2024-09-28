const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');
const { SerialPort } = require('serialport');
const bodyParser = require('body-parser');

const app = express();
const port = 8000;
app.use(bodyParser.json());
/*
const serialPort = 'COM12';  // 사용하는 시리얼 포트로 변경해 주세요.
const baudRate = 9600;  // 통신 속도를 필요에 맞게 변경해 주세요.
const port2 = new SerialPort({ path: serialPort, baudRate: baudRate });
*/
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'kiosk',
  password: 'goldenglow290$',
  port: 5432,
});

app.use(cors({
  origin: 'http://localhost:8080',
  methods: 'GET',
}));

app.get('/data/:division', async (req, res) => {
  try {
    const division = req.params.division;
    const client = await pool.connect();
    const result = await client.query(`SELECT * FROM product WHERE p_division = '${division}'`);
    const data = result.rows;
    client.release();

    res.json(data);
  } catch (error) {
    console.error('데이터베이스에서 데이터를 가져오는 중 오류 발생:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// 새로운 엔드포인트 설정
app.post('/order', async (req, res) => {
  try {
    const message = req.body.message;
    const client = await pool.connect();
    const date = new Date();
    client.query(`INSERT INTO order1(name, date) VALUES('${message}', '${date}')`);
    port2.write(message, (err) => {
      if (err) {
        return console.log('Error:', err.message);
      }
      console.log('Data sent successfully.');
    });
    //res.json({ message: '주문 정보가 아두이노에 전송되었습니다.' });
  } catch (error) {
    console.error('데이터베이스에서 데이터를 가져오는 중 오류 발생:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.get('/price/:name', async (req, res) => {
  try {
    const name = req.params.name;
    const client = await pool.connect();
    const result = await client.query(`SELECT p_price FROM product WHERE p_name='${name}'`);
    const data = result.rows[0].p_price
    res.json(data)
    console.log(data)
  } catch (error) {
    console.error('데이터베이스에서 데이터를 가져오는 중 오류 발생:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
})

app.listen(port, () => {
  console.log(`서버가 http://localhost:${port} 에서 실행 중입니다.`);
});