class RecursoNaoEncontradoError(LookupError):
    pass


class DadosInvalidosError(ValueError):
    pass


class ProjetoNaoEncontradoError(RecursoNaoEncontradoError):
    pass


class TarefaNaoEncontradaError(RecursoNaoEncontradoError):
    pass


class UsuarioNaoEncontradoError(RecursoNaoEncontradoError):
    pass


class ProjetoComTarefasError(ValueError):
    pass


class EmailDuplicadoError(ValueError):
    pass
