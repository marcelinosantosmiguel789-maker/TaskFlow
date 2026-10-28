import { Check, Circle, Pencil, Trash2 } from "lucide-react";
import type { Task } from "../types";

interface TaskRowProps {
  task: Task;
  saving: boolean;
  onToggle: () => void;
  onEdit: () => void;
  onDelete: () => void;
}

export function TaskRow({ task, saving, onToggle, onEdit, onDelete }: TaskRowProps) {
  return (
    <article className={`task-row ${task.concluida ? "is-complete" : ""}`}>
      <button
        className={`task-check ${task.concluida ? "checked" : ""}`}
        type="button"
        onClick={onToggle}
        disabled={saving}
        aria-label={task.concluida ? `Marcar ${task.titulo} como pendente` : `Concluir ${task.titulo}`}
        aria-pressed={task.concluida}
      >
        {task.concluida ? <Check size={14} strokeWidth={3} /> : <Circle size={19} strokeWidth={1.6} />}
      </button>
      <div className="task-copy">
        <h3>{task.titulo}</h3>
        {task.descricao && <p>{task.descricao}</p>}
      </div>
      <span className={`status-pill ${task.concluida ? "done" : "pending"}`}>
        <span className="status-dot" />{task.concluida ? "Concluída" : "Pendente"}
      </span>
      <div className="task-actions">
        <button className="icon-button small" type="button" onClick={onEdit} disabled={saving} aria-label={`Editar ${task.titulo}`}>
          <Pencil size={15} />
        </button>
        <button className="icon-button small danger" type="button" onClick={onDelete} disabled={saving} aria-label={`Excluir ${task.titulo}`}>
          <Trash2 size={15} />
        </button>
      </div>
    </article>
  );
}
