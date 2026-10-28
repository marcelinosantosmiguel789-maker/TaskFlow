import { useState, type FormEvent } from "react";
import { X } from "lucide-react";
import type { Project, Task, TaskPayload, TaskUpdatePayload } from "../types";

interface TaskDialogProps {
  task: Task | null;
  projectId: number;
  projects: Project[];
  onClose: () => void;
  onSubmit: (payload: TaskPayload | TaskUpdatePayload) => Promise<unknown>;
}

export function TaskDialog({ task, projectId, projects, onClose, onSubmit }: TaskDialogProps) {
  const [title, setTitle] = useState(task?.titulo ?? "");
  const [description, setDescription] = useState(task?.descricao ?? "");
  const [selectedProject, setSelectedProject] = useState(String(task?.projeto_id ?? projectId));
  const [submitting, setSubmitting] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLocalError(null);
    setSubmitting(true);
    const common = { titulo: title.trim(), descricao: description.trim() || null };
    try {
      await onSubmit(task ? common : { ...common, projeto_id: Number(selectedProject) });
      onClose();
    } catch (cause) {
      setLocalError(cause instanceof Error ? cause.message : "Não foi possível salvar a tarefa.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="dialog-backdrop" onMouseDown={(event) => event.target === event.currentTarget && onClose()}>
      <section className="dialog" role="dialog" aria-modal="true" aria-labelledby="task-dialog-title">
        <div className="dialog-heading">
          <div>
            <span className="eyebrow">{task ? "ATUALIZE SEU PLANO" : "UM PASSO DE CADA VEZ"}</span>
            <h2 id="task-dialog-title">{task ? "Editar tarefa" : "Nova tarefa"}</h2>
            <p>Registre o próximo passo e deixe o progresso acontecer.</p>
          </div>
          <button className="icon-button" type="button" onClick={onClose} aria-label="Fechar">
            <X size={19} />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="dialog-form">
          <label className="field-label" htmlFor="task-title">O que precisa ser feito?</label>
          <input id="task-title" autoFocus required maxLength={255} value={title} onChange={(event) => setTitle(event.target.value)} placeholder="Ex.: Revisar a proposta" />
          <label className="field-label" htmlFor="task-description">Detalhes <span>opcional</span></label>
          <textarea id="task-description" rows={3} maxLength={255} value={description} onChange={(event) => setDescription(event.target.value)} placeholder="Adicione um pouco de contexto…" />
          {!task && (
            <>
              <label className="field-label" htmlFor="task-project">Projeto</label>
              <select id="task-project" required value={selectedProject} onChange={(event) => setSelectedProject(event.target.value)}>
                {projects.map((project) => <option key={project.id} value={project.id}>{project.nome}</option>)}
              </select>
            </>
          )}
          {localError && <p className="form-error" role="alert">{localError}</p>}
          <div className="dialog-actions">
            <button className="button button-quiet" type="button" onClick={onClose}>Cancelar</button>
            <button className="button button-primary" type="submit" disabled={submitting || !title.trim()}>
              {submitting ? "Salvando…" : task ? "Salvar alterações" : "Adicionar tarefa"}
            </button>
          </div>
        </form>
      </section>
    </div>
  );
}
