import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  ArrowRight,
  Check,
  ChevronDown,
  CircleCheck,
  FolderKanban,
  LayoutDashboard,
  LoaderCircle,
  Menu,
  Plus,
  RefreshCw,
  Search,
  Sparkles,
  SquarePen,
  X,
} from "lucide-react";
import { ProjectDialog } from "./components/ProjectDialog";
import { TaskDialog } from "./components/TaskDialog";
import { TaskRow } from "./components/TaskRow";
import { useTaskflow } from "./hooks/useTaskflow";
import type { Project, ProjectPayload, Task, TaskPayload, TaskUpdatePayload } from "./types";

type DialogState =
  | { kind: "project"; project: Project | null }
  | { kind: "task"; task: Task | null }
  | null;
type StatusFilter = "all" | "open" | "done";

const dateLabel = new Intl.DateTimeFormat("pt-BR", {
  weekday: "long",
  day: "numeric",
  month: "long",
}).format(new Date());

function App() {
  const {
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
  } = useTaskflow();

  const [activeProjectId, setActiveProjectId] = useState<number | null>(null);
  const [projectQuery, setProjectQuery] = useState("");
  const [taskQuery, setTaskQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("all");
  const [dialog, setDialog] = useState<DialogState>(null);
  const [mobileNavOpen, setMobileNavOpen] = useState(false);

  useEffect(() => {
    if (projects.length === 0) {
      setActiveProjectId(null);
    } else if (activeProjectId === null || !projects.some((project) => project.id === activeProjectId)) {
      setActiveProjectId(projects[0].id);
    }
  }, [projects, activeProjectId]);

  const activeProject = projects.find((project) => project.id === activeProjectId) ?? null;
  const activeTasks = activeProject ? tasksByProject[activeProject.id] ?? [] : [];
  const completedCount = activeTasks.filter((task) => task.concluida).length;
  const openCount = activeTasks.length - completedCount;
  const allCompleted = tasks.filter((task) => task.concluida).length;
  const progress = activeTasks.length ? Math.round((completedCount / activeTasks.length) * 100) : 0;

  const visibleProjects = useMemo(() => {
    const query = projectQuery.trim().toLocaleLowerCase("pt-BR");
    return projects.filter((project) => `${project.nome} ${project.descricao ?? ""}`.toLocaleLowerCase("pt-BR").includes(query));
  }, [projects, projectQuery]);

  const visibleTasks = useMemo(() => {
    const query = taskQuery.trim().toLocaleLowerCase("pt-BR");
    return activeTasks.filter((task) => {
      const matchesSearch = `${task.titulo} ${task.descricao ?? ""}`.toLocaleLowerCase("pt-BR").includes(query);
      const matchesStatus = statusFilter === "all" || (statusFilter === "done" ? task.concluida : !task.concluida);
      return matchesSearch && matchesStatus;
    });
  }, [activeTasks, taskQuery, statusFilter]);

  async function handleProjectSubmit(payload: ProjectPayload) {
    if (dialog?.kind === "project" && dialog.project) {
      return updateProject(dialog.project.id, payload);
    }
    const project = await createProject(payload);
    setActiveProjectId(project.id);
    setStatusFilter("all");
    setTaskQuery("");
    return project;
  }

  async function handleTaskSubmit(payload: TaskPayload | TaskUpdatePayload) {
    if (dialog?.kind === "task" && dialog.task) {
      return updateTask(dialog.task.id, dialog.task.projeto_id, payload as TaskUpdatePayload);
    }
    const task = await createTask(payload as TaskPayload);
    setActiveProjectId(task.projeto_id);
    return task;
  }

  async function handleDeleteProject(project: Project) {
    if (!window.confirm(`Excluir o projeto “${project.nome}”? A API não permite excluir projetos que ainda tenham tarefas.`)) return;
    setError(null);
    try {
      await deleteProject(project.id);
    } catch {
      // A mensagem da API é apresentada no aviso global do dashboard.
    }
  }

  async function handleDeleteTask(task: Task) {
    if (!window.confirm(`Excluir a tarefa “${task.titulo}”?`)) return;
    setError(null);
    try {
      await deleteTask(task.id, task.projeto_id);
    } catch {
      // A mensagem da API é apresentada no aviso global do dashboard.
    }
  }

  async function handleToggleTask(task: Task) {
    setError(null);
    try {
      await updateTask(task.id, task.projeto_id, { concluida: !task.concluida });
    } catch {
      // A mensagem da API é apresentada no aviso global do dashboard.
    }
  }

  function chooseProject(id: number) {
    setActiveProjectId(id);
    setStatusFilter("all");
    setTaskQuery("");
    setMobileNavOpen(false);
    void readProject(id).catch(() => undefined);
  }

  return (
    <div className="app-shell">
      <aside className={`sidebar ${mobileNavOpen ? "mobile-open" : ""}`}>
        <div className="brand-lockup">
          <div className="brand-mark" aria-hidden="true"><span /><span /><span /></div>
          <div className="brand-name">task<span>flow</span><small>WORKSPACE</small></div>
          <button className="icon-button mobile-close" type="button" onClick={() => setMobileNavOpen(false)} aria-label="Fechar menu"><X size={18} /></button>
        </div>

        <button className="workspace-switcher" type="button" aria-label="Workspace TaskFlow">
          <span className="workspace-avatar">T</span>
          <span className="workspace-copy"><strong>Meu workspace</strong><small>Plano pessoal</small></span>
          <ChevronDown size={15} />
        </button>

        <div className="sidebar-section-label">MENU</div>
        <button className="primary-nav active" type="button" onClick={() => setMobileNavOpen(false)}>
          <LayoutDashboard size={17} strokeWidth={1.8} /><span>Visão geral</span><span className="nav-active-mark" />
        </button>

        <div className="project-section-head">
          <span className="sidebar-section-label">PROJETOS <span className="project-count">{projects.length}</span></span>
          <button className="icon-button small sidebar-add" type="button" onClick={() => setDialog({ kind: "project", project: null })} aria-label="Adicionar projeto"><Plus size={16} /></button>
        </div>
        <label className="sidebar-search">
          <Search size={14} />
          <input value={projectQuery} onChange={(event) => setProjectQuery(event.target.value)} placeholder="Encontrar projeto" aria-label="Buscar projetos" />
          {projectQuery && <button type="button" onClick={() => setProjectQuery("")} aria-label="Limpar busca"><X size={13} /></button>}
        </label>
        <div className="project-list">
          {visibleProjects.map((project, index) => (
            <div key={project.id} className={`project-nav-item ${activeProjectId === project.id ? "selected" : ""}`}>
              <button className="project-nav-button" type="button" onClick={() => chooseProject(project.id)} aria-busy={loadingProjectId === project.id}>
                <span className={`project-color color-${index % 5}`}><FolderKanban size={14} /></span>
                <span className="project-nav-name">{project.nome}</span>
                {loadingProjectId === project.id ? <LoaderCircle size={12} className="spin project-loading" /> : <span className="project-task-count">{tasksByProject[project.id]?.length ?? "—"}</span>}
              </button>
              <div className="project-actions">
                <button className="icon-button mini" type="button" onClick={() => setDialog({ kind: "project", project })} aria-label={`Editar ${project.nome}`}><SquarePen size={13} /></button>
                <button className="icon-button mini danger" type="button" onClick={() => void handleDeleteProject(project)} aria-label={`Excluir ${project.nome}`}><X size={14} /></button>
              </div>
            </div>
          ))}
          {!loading && visibleProjects.length === 0 && (
            <p className="sidebar-empty">{projects.length ? "Nenhum projeto encontrado." : "Seus projetos aparecem aqui."}</p>
          )}
        </div>

        <div className="sidebar-bottom">
          <div className={`api-status ${error ? "offline" : loading ? "connecting" : "online"}`}>
            <span className="api-status-dot" />
            <span><strong>{error ? "API indisponível" : loading ? "Conectando à API" : "API conectada"}</strong><small>{error ? "Verifique sua conexão" : "Sincronização ativa"}</small></span>
            {!loading && <Activity size={15} />}
          </div>
          <div className="sidebar-credit"><span className="mini-avatar">TF</span><span><strong>TaskFlow</strong><small>Seu espaço de foco</small></span><button className="icon-button small" type="button" aria-label="Opções do workspace"><ChevronDown size={15} /></button></div>
        </div>
      </aside>

      {mobileNavOpen && <button className="mobile-scrim" type="button" onClick={() => setMobileNavOpen(false)} aria-label="Fechar navegação" />}

      <main className="main-area">
        <header className="topbar">
          <button className="icon-button mobile-menu" type="button" onClick={() => setMobileNavOpen(true)} aria-label="Abrir menu"><Menu size={20} /></button>
          <div className="breadcrumb"><span>Workspace</span><span className="crumb-divider">/</span><strong>{activeProject?.nome ?? "Visão geral"}</strong></div>
          <div className="topbar-right">
            <label className="global-search"><Search size={16} /><input value={taskQuery} onChange={(event) => setTaskQuery(event.target.value)} placeholder="Buscar tarefas…" aria-label="Buscar tarefas" /><kbd>⌘ K</kbd></label>
            <span className={`sync-indicator ${saving ? "is-saving" : ""}`} title={saving ? "Salvando alterações" : "Sincronização ativa"} aria-label={saving ? "Salvando alterações" : "Sincronização ativa"} />
            <span className="top-avatar">TF</span>
          </div>
        </header>

        <div className="dashboard-content">
          <section className="welcome-row">
            <div>
              <div className="date-line"><span className="date-sparkle"><Sparkles size={13} /></span>{dateLabel}</div>
              <h1>Seu dia, no seu ritmo<span>.</span></h1>
              <p>Um passo de cada vez. O resto flui.</p>
            </div>
            <button className="button button-primary new-task-button" type="button" onClick={() => setDialog({ kind: "task", task: null })} disabled={!projects.length}>
              <Plus size={17} /> Nova tarefa
            </button>
          </section>

          {error && (
            <div className="error-banner" role="alert">
              <span className="error-icon"><Activity size={16} /></span>
              <div><strong>Não foi possível sincronizar</strong><p>{error}</p></div>
              <button className="button button-quiet retry-button" type="button" onClick={() => void refresh()} disabled={loading}><RefreshCw size={14} className={loading ? "spin" : ""} /> Tentar novamente</button>
              <button className="icon-button small error-dismiss" type="button" onClick={() => setError(null)} aria-label="Fechar aviso"><X size={15} /></button>
            </div>
          )}

          <section className="metrics-grid" aria-label="Resumo geral">
            <article className="metric-card">
              <div className="metric-icon lilac"><FolderKanban size={18} /></div>
              <span className="metric-label">Projetos ativos</span>
              <strong className="metric-value">{projects.length.toString().padStart(2, "0")}</strong>
              <span className="metric-caption">seus espaços de trabalho</span>
              <span className="metric-decoration metric-decoration-lilac" />
            </article>
            <article className="metric-card">
              <div className="metric-icon mint"><Check size={18} /></div>
              <span className="metric-label">Tarefas concluídas</span>
              <strong className="metric-value">{allCompleted.toString().padStart(2, "0")}</strong>
              <span className="metric-caption">de {tasks.length} tarefas no total</span>
              <span className="metric-decoration metric-decoration-mint" />
            </article>
            <article className="metric-card accent-card">
              <div className="metric-icon apricot"><Activity size={18} /></div>
              <span className="metric-label">Em andamento</span>
              <strong className="metric-value">{(tasks.length - allCompleted).toString().padStart(2, "0")}</strong>
              <span className="metric-caption">próximos passos pela frente</span>
              <span className="metric-decoration metric-decoration-apricot" />
            </article>
          </section>

          <div className="workspace-grid">
            <section className="task-panel">
              <div className="panel-heading">
                <div>
                  <span className="eyebrow">SEU FOCO AGORA</span>
                  <h2>{activeProject ? activeProject.nome : "Projetos e tarefas"}</h2>
                  <p>{activeProject?.descricao || (activeProject ? "Tudo o que você precisa avançar, em um só lugar." : "Escolha um projeto para acompanhar seu progresso.")}</p>
                </div>
                {activeProject && <button className="icon-button edit-project-button" type="button" onClick={() => setDialog({ kind: "project", project: activeProject })} aria-label="Editar projeto selecionado"><SquarePen size={16} /></button>}
              </div>

              {activeProject && (
                <>
                  <div className="task-toolbar">
                    <div className="filter-tabs" role="tablist" aria-label="Filtrar tarefas">
                      <button className={statusFilter === "all" ? "active" : ""} type="button" role="tab" aria-selected={statusFilter === "all"} onClick={() => setStatusFilter("all")}>Todas <span>{activeTasks.length}</span></button>
                      <button className={statusFilter === "open" ? "active" : ""} type="button" role="tab" aria-selected={statusFilter === "open"} onClick={() => setStatusFilter("open")}>Pendentes <span>{openCount}</span></button>
                      <button className={statusFilter === "done" ? "active" : ""} type="button" role="tab" aria-selected={statusFilter === "done"} onClick={() => setStatusFilter("done")}>Concluídas <span>{completedCount}</span></button>
                    </div>
                    <button className="icon-button small refresh-tasks" type="button" onClick={() => void refresh()} disabled={loading} aria-label="Atualizar projetos e tarefas"><RefreshCw size={15} className={loading ? "spin" : ""} /></button>
                  </div>

                  <div className="task-list" aria-live="polite">
                    {loading ? (
                      <div className="loading-state"><LoaderCircle size={22} className="spin" /><span>Carregando seus projetos…</span></div>
                    ) : visibleTasks.length ? (
                      visibleTasks.map((task) => (
                        <TaskRow
                          key={task.id}
                          task={task}
                          saving={saving}
                          onToggle={() => void handleToggleTask(task)}
                          onEdit={() => setDialog({ kind: "task", task })}
                          onDelete={() => void handleDeleteTask(task)}
                        />
                      ))
                    ) : activeTasks.length === 0 ? (
                      <div className="empty-state task-empty">
                        <span className="empty-art"><CircleCheck size={25} /></span>
                        <h3>Uma página em branco, cheia de possibilidades.</h3>
                        <p>Adicione a primeira tarefa e transforme uma ideia em próximo passo.</p>
                        <button className="button button-primary" type="button" onClick={() => setDialog({ kind: "task", task: null })}><Plus size={16} /> Criar primeira tarefa</button>
                      </div>
                    ) : (
                      <div className="empty-state search-empty">
                        <span className="empty-art"><Search size={23} /></span>
                        <h3>Nada por aqui por enquanto.</h3>
                        <p>{taskQuery ? "Tente outro termo ou limpe a busca." : "Nenhuma tarefa corresponde a este filtro."}</p>
                        {(taskQuery || statusFilter !== "all") && <button className="text-button" type="button" onClick={() => { setTaskQuery(""); setStatusFilter("all"); }}>Limpar busca e filtros <ArrowRight size={14} /></button>}
                      </div>
                    )}
                  </div>

                  {activeTasks.length > 0 && <div className="list-footer"><span><span className="footer-dot" /> Atualizado com a API TaskFlow</span><span>{visibleTasks.length} de {activeTasks.length} tarefas</span></div>}
                </>
              )}

              {!activeProject && (
                <div className="empty-state project-empty">
                  <span className="empty-art project-empty-art"><FolderKanban size={24} /></span>
                  <h3>{loading ? "Preparando seu espaço…" : error ? "Conecte-se para continuar." : "Comece por um novo projeto."}</h3>
                  <p>{loading ? "Estamos buscando seus projetos." : error ? "Confira se a API está em execução e tente novamente." : "Reúna tarefas, acompanhe o progresso e mantenha o foco no que importa."}</p>
                  {error ? <button className="button button-primary" type="button" onClick={() => void refresh()} disabled={loading}><RefreshCw size={15} /> Tentar novamente</button> : !loading && <button className="button button-primary" type="button" onClick={() => setDialog({ kind: "project", project: null })}><Plus size={16} /> Criar primeiro projeto</button>}
                </div>
              )}
            </section>

            <aside className="insight-column">
              <section className="progress-card">
                <div className="side-card-heading"><div><span className="eyebrow">VISÃO DO PROJETO</span><h2>Seu progresso</h2></div><span className="progress-icon"><Activity size={16} /></span></div>
                <div className="progress-display">
                  <div className="progress-ring" style={{ "--progress": `${progress}%` } as React.CSSProperties}>
                    <div><strong>{progress}<span>%</span></strong><small>concluído</small></div>
                  </div>
                  <div className="progress-copy"><strong>{activeProject?.nome ?? "Selecione um projeto"}</strong><span>{activeTasks.length ? `${completedCount} de ${activeTasks.length} tarefas concluídas` : "Seu próximo passo começa aqui"}</span></div>
                </div>
                <div className="progress-track"><span style={{ width: `${progress}%` }} /></div>
                <div className="progress-legend"><span><i className="legend-open" />Pendentes <strong>{openCount}</strong></span><span><i className="legend-done" />Feitas <strong>{completedCount}</strong></span></div>
              </section>

              <section className="focus-card">
                <div className="focus-illustration" aria-hidden="true"><span className="focus-orbit orbit-one" /><span className="focus-orbit orbit-two" /><span className="focus-star star-one">✦</span><span className="focus-star star-two">✳</span><div className="focus-check"><Check size={18} strokeWidth={2.5} /></div></div>
                <span className="eyebrow">UM LEMBRETE AMIGÁVEL</span>
                <h2>Pequenos passos também são progresso.</h2>
                <p>Escolha uma tarefa e avance no seu tempo. Você está construindo algo bom.</p>
              </section>

              <button className="quick-add-card" type="button" onClick={() => setDialog({ kind: "project", project: null })}>
                <span className="quick-add-icon"><Plus size={17} /></span>
                <span><strong>Novo projeto</strong><small>Abra espaço para uma ideia</small></span>
                <ArrowRight size={16} />
              </button>
              <div className="sidebar-independent-note"><span className="footer-dot" /> Seus dados ficam sincronizados com a API do projeto.</div>
            </aside>
          </div>

          <footer className="page-footer"><span>TaskFlow <span>·</span> feito para fazer as coisas fluírem.</span><span>{dateLabel}</span></footer>
        </div>
      </main>

      {dialog?.kind === "project" && <ProjectDialog project={dialog.project} onClose={() => setDialog(null)} onSubmit={handleProjectSubmit} />}
      {dialog?.kind === "task" && activeProject && <TaskDialog task={dialog.task} projectId={activeProject.id} projects={projects} onClose={() => setDialog(null)} onSubmit={handleTaskSubmit} />}
      {dialog?.kind === "task" && !activeProject && <TaskDialog task={null} projectId={projects[0]?.id ?? 0} projects={projects} onClose={() => setDialog(null)} onSubmit={handleTaskSubmit} />}
    </div>
  );
}

export default App;
