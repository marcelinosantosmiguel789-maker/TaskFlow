export interface Project {
  id: number;
  nome: string;
  descricao: string | null;
}

export interface Task {
  id: number;
  titulo: string;
  descricao: string | null;
  concluida: boolean;
  projeto_id: number;
}

export interface ProjectPayload {
  nome: string;
  descricao: string | null;
}

export interface TaskPayload {
  titulo: string;
  descricao: string | null;
  projeto_id: number;
}

export interface TaskUpdatePayload {
  titulo?: string;
  descricao?: string | null;
  concluida?: boolean;
}
