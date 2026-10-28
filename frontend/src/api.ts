import type { Project, ProjectPayload, Task, TaskPayload, TaskUpdatePayload } from "./types";

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "/api").replace(/\/+$/, "");

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

function describeError(detail: unknown, fallback: string): string {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    const messages = detail
      .map((item) => (item && typeof item === "object" && "msg" in item ? String(item.msg) : ""))
      .filter(Boolean);
    if (messages.length) return messages.join(" ");
  }
  return fallback;
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...init,
      headers: {
        ...(init.body ? { "Content-Type": "application/json" } : {}),
        ...init.headers,
      },
    });
  } catch {
    throw new ApiError("Não foi possível conectar à API. Confira o servidor e tente novamente.", 0);
  }

  if (response.status === 204) return undefined as T;

  const payload: unknown = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = payload && typeof payload === "object" && "detail" in payload
      ? payload.detail
      : undefined;
    const fallback = response.status >= 500
      ? "A API encontrou um problema. Tente novamente em instantes."
      : `A solicitação não foi concluída (HTTP ${response.status}).`;
    throw new ApiError(describeError(detail, fallback), response.status);
  }
  return payload as T;
}

export const taskflowApi = {
  listProjects: () => request<Project[]>("/projetos"),
  getProject: (id: number) => request<Project>(`/projetos/${id}`),
  createProject: (payload: ProjectPayload) => request<Project>("/projetos", {
    method: "POST",
    body: JSON.stringify(payload),
  }),
  updateProject: (id: number, payload: Partial<ProjectPayload>) => request<Project>(`/projetos/${id}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  }),
  deleteProject: (id: number) => request<void>(`/projetos/${id}`, { method: "DELETE" }),
  listTasks: (projectId: number) => request<Task[]>(`/tarefas?projeto_id=${projectId}`),
  createTask: (payload: TaskPayload) => request<Task>("/tarefas", {
    method: "POST",
    body: JSON.stringify(payload),
  }),
  updateTask: (id: number, payload: TaskUpdatePayload) => request<Task>(`/tarefas/${id}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  }),
  deleteTask: (id: number) => request<void>(`/tarefas/${id}`, { method: "DELETE" }),
};
