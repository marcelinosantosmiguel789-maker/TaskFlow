import { useCallback, useEffect, useState } from "react";
import { ApiError, taskflowApi } from "../api";
import type { Project, ProjectPayload, Task, TaskPayload, TaskUpdatePayload } from "../types";

function messageFor(error: unknown): string {
  if (error instanceof ApiError) return error.message;
  if (error instanceof Error) return error.message;
  return "Algo não saiu como esperado. Tente novamente.";
}

export function useTaskflow() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [tasksByProject, setTasksByProject] = useState<Record<number, Task[]>>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [loadingProjectId, setLoadingProjectId] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const runMutation = useCallback(async <T,>(action: () => Promise<T>): Promise<T> => {
    setSaving(true);
    setError(null);
    try {
      return await action();
    } catch (cause) {
      setError(messageFor(cause));
      throw cause;
    } finally {
      setSaving(false);
    }
  }, []);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const nextProjects = await taskflowApi.listProjects();
      const taskLists = await Promise.all(nextProjects.map(async (project) => [
        project.id,
        await taskflowApi.listTasks(project.id),
      ] as const));
      setProjects(nextProjects);
      setTasksByProject(Object.fromEntries(taskLists));
      return true;
    } catch (cause) {
      setError(messageFor(cause));
      return false;
    } finally {
      setLoading(false);
    }
  }, []);

  const readProject = useCallback(async (id: number) => {
    setLoadingProjectId(id);
    setError(null);
    try {
      const project = await taskflowApi.getProject(id);
      setProjects((current) => current.map((item) => item.id === id ? project : item));
      return project;
    } catch (cause) {
      setError(messageFor(cause));
      throw cause;
    } finally {
      setLoadingProjectId(null);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const createProject = useCallback((payload: ProjectPayload) => runMutation(async () => {
    const project = await taskflowApi.createProject(payload);
    setProjects((current) => [...current, project]);
    setTasksByProject((current) => ({ ...current, [project.id]: [] }));
    return project;
  }), [runMutation]);

  const updateProject = useCallback((id: number, payload: Partial<ProjectPayload>) => runMutation(async () => {
    const project = await taskflowApi.updateProject(id, payload);
    setProjects((current) => current.map((item) => item.id === id ? project : item));
    return project;
  }), [runMutation]);

  const deleteProject = useCallback((id: number) => runMutation(async () => {
    await taskflowApi.deleteProject(id);
    setProjects((current) => current.filter((item) => item.id !== id));
    setTasksByProject((current) => {
      const next = { ...current };
      delete next[id];
      return next;
    });
  }), [runMutation]);

  const createTask = useCallback((payload: TaskPayload) => runMutation(async () => {
    const task = await taskflowApi.createTask(payload);
    setTasksByProject((current) => ({
      ...current,
      [task.projeto_id]: [...(current[task.projeto_id] ?? []), task],
    }));
    return task;
  }), [runMutation]);

  const updateTask = useCallback((id: number, projectId: number, payload: TaskUpdatePayload) => runMutation(async () => {
    const task = await taskflowApi.updateTask(id, payload);
    setTasksByProject((current) => ({
      ...current,
      [projectId]: (current[projectId] ?? []).map((item) => item.id === id ? task : item),
    }));
    return task;
  }), [runMutation]);

  const deleteTask = useCallback((id: number, projectId: number) => runMutation(async () => {
    await taskflowApi.deleteTask(id);
    setTasksByProject((current) => ({
      ...current,
      [projectId]: (current[projectId] ?? []).filter((item) => item.id !== id),
    }));
  }), [runMutation]);

  const tasks = Object.values(tasksByProject).flat();

  return {
    projects,
    tasksByProject,
    tasks,
    loading,
    saving,
    loadingProjectId,
    error,
    setError,
    refresh,
    readProject,
    createProject,
    updateProject,
    deleteProject,
    createTask,
    updateTask,
    deleteTask,
  };
}
