import type { Request, Response } from 'express';
import { CurriculoSchema } from '../schemas/curriculo.schema.js';
import * as CurriculoModel from '../models/curriculo.model.js';

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;');
}

export async function listCurriculos(_req: Request, res: Response): Promise<void> {
  const curriculos = await CurriculoModel.findAll();
  res.json(curriculos);
}

export async function getCurriculo(req: Request, res: Response): Promise<void> {
  const id = Number(req.params['id']);
  if (isNaN(id)) {
    res.status(400).json({ error: 'Invalid id' });
    return;
  }
  const curriculo = await CurriculoModel.findById(id);
  if (!curriculo) {
    res.status(404).json({ error: 'Not found' });
    return;
  }
  res.json(curriculo);
}

export async function createCurriculo(req: Request, res: Response): Promise<void> {
  const result = CurriculoSchema.safeParse(req.body);
  if (!result.success) {
    res.status(422).json({ errors: result.error.flatten().fieldErrors });
    return;
  }

  const raw = result.data;
  const data = {
    nome: escapeHtml(raw.nome),
    email: escapeHtml(raw.email),
    experiencia_profissional: escapeHtml(raw.experiencia_profissional),
    ...(raw.telefone !== undefined && { telefone: escapeHtml(raw.telefone) }),
    ...(raw.site_url !== undefined && { site_url: escapeHtml(raw.site_url) }),
  };

  const id = await CurriculoModel.create(data);
  res.status(201).json({ id });
}
