import 'dotenv/config';
import express from 'express';
import curriculoRoutes from './routes/curriculo.routes.js';

const app = express();
const port = process.env['PORT'] ?? 3000;

app.use(express.json());
app.use(curriculoRoutes);

app.listen(port, () => {
  console.log(`Backend running on http://localhost:${port}`);
});
