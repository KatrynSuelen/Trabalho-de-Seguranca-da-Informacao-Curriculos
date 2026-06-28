import { z } from 'zod';

export const CurriculoSchema = z.object({
  nome: z.string().min(2).max(255),
  telefone: z.string().max(15).regex(/^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$/).optional(),
  email: z.string().email().max(255),
  site_url: z.string().url().max(255).optional(),
  experiencia_profissional: z.string().min(10),
});

export type CurriculoInput = z.infer<typeof CurriculoSchema>;
