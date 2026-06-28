import { Router } from 'express';
import {
  listCurriculos,
  getCurriculo,
  createCurriculo,
} from '../controllers/curriculo.controller.js';

const router = Router();

router.get('/curriculos', listCurriculos);
router.get('/curriculos/:id', getCurriculo);
router.post('/curriculos', createCurriculo);

export default router;
