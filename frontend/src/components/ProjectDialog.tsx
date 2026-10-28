import { useState, type FormEvent } from "react";
import { X } from "lucide-react";
import type { Project, ProjectPayload } from "../types";

interface ProjectDialogProps {
  project: Project | null;
  onClose: () => void;
  onSubmit: (payload: ProjectPayload) => Promise<unknown>;
}

export function ProjectDialog({ project, onClose, onSubmit }: ProjectDialogProps) {
  const [name, setName] = useState(project?.nome ?? "");
  const [description, setDescription] = useState(project?.descricao ?? "");
  const [submitting, setSubmitting] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLocalError(null);
    setSubmitting(true);
    try {
      await onSubmit({ nome: name.trim(), descricao: description.trim() || null });
      onClose();
    } catch (cause) {
      setLocalError(cause instanceof Error ? cause.message : "Não foi possível salvar o projeto.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="dialog-backdrop" onMouseDown={(event) => event.target === event.currentTarget && onClose()}>
      <section className="dialog" role="dialog" aria-modal="true" aria-labelledby="project-dialog-title">
        <div className="dialog-heading">
          <div>
            <span className="eyebrow">ESPAÇO DE TRABALHO</span>
            <h2 id="project-dialog-title">{project ? "Editar projeto" : "Novo projeto"}</h2>
            <p>Um bom plano começa com um espaço para organizar as ideias.</p>
          </div>
          <button className="icon-button" type="button" onClick={onClose} aria-label="Fechar">
            <X size={19} />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="dialog-form">
          <label className="field-label" htmlFor="project-name">Nome do projeto</label>
          <input id="project-name" autoFocus required maxLength={255} value={name} onChange={(event) => setName(event.target.value)} placeholder="Ex.: Redesign do site" />
          <label className="field-label" htmlFor="project-description">Descrição <span>opcional</span></label>
          <textarea id="project-description" rows={3} maxLength={255} value={description} onChange={(event) => setDescription(event.target.value)} placeholder="O que você quer realizar?" />
          {localError && <p className="form-error" role="alert">{localError}</p>}
          <div className="dialog-actions">
            <button className="button button-quiet" type="button" onClick={onClose}>Cancelar</button>
            <button className="button button-primary" type="submit" disabled={submitting || !name.trim()}>
              {submitting ? "Salvando…" : project ? "Salvar alterações" : "Criar projeto"}
            </button>
          </div>
        </form>
      </section>
    </div>
  );
}
