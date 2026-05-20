class EstoqueError(Exception):
    """Erro base do sistema."""


class ProdutoDuplicadoError(EstoqueError):
    """Produto com código duplicado."""


class ProdutoNaoEncontradoError(EstoqueError):
    """Produto não encontrado."""


class EstoqueInsuficienteError(EstoqueError):
    """Estoque insuficiente para venda."""


class ValidacaoError(EstoqueError):
    """Erro de validação."""