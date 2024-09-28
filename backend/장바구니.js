const express = require('express');
const { Pool } = require('pg');

const app = express();
const port = 3000;

const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'postgres',
  password: 'tlswo3850',
  port: 5432,
});

app.get('/api/data', async (req, res) => {
  try {
    const client = await pool.connect();
    const result = await client.query('SELECT * FROM menu'); // 테이블 이름을 실제 테이블 이름으로 변경
    const data = result.rows;
    client.release();

    res.json(data);
  } catch (error) {
    console.error('데이터베이스에서 데이터를 가져오는 중 오류 발생:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.listen(port, () => {
  console.log(`서버가 http://localhost:${port} 에서 실행 중입니다.`);
});



conn = psycopg2.connect(
  dbname="postgres",
  user="postgres",
  host="localhost",
  password="tlswo3850",
  port="5432"
)