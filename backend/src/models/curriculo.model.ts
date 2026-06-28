import type { RowDataPacket, ResultSetHeader } from 'mysql2';
import { pool } from '../db.js';
import type { CurriculoInput } from '../schemas/curriculo.schema.js';

export interface Curriculo extends RowDataPacket {
  id: number;
  nome: string;
  telefone: string | null;
  email: string;
  site_url: string | null;
  experiencia_profissional: string;
}

export async function findAll(): Promise<Curriculo[]> {
  const [rows] = await pool.execute<Curriculo[]>(
    'SELECT id, nome, email FROM curriculo ORDER BY nome ASC',
  );
  return rows;
}

export async function findById(id: number): Promise<Curriculo | null> {
  const [rows] = await pool.execute<Curriculo[]>(
    'SELECT * FROM curriculo WHERE id = ?',
    [id],
  );
  return rows[0] ?? null;
}

export async function create(data: CurriculoInput): Promise<number> {
  const [result] = await pool.execute<ResultSetHeader>(
    'INSERT INTO curriculo (nome, telefone, email, site_url, experiencia_profissional) VALUES (?, ?, ?, ?, ?)',
    [
      data.nome,
      data.telefone ?? null,
      data.email,
      data.site_url ?? null,
      data.experiencia_profissional,
    ],
  );
  return result.insertId;
}
