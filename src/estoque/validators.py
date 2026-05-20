from .exceptions import ValidacaoError


def validar_codigo(codigo: str) -> None:
    if not codigo or not codigo.strip():
        raise ValidacaoError("Código não pode ser vazio.")


def validar_texto(valor: str, campo: str) -> None:
    if not valor or not valor.strip():
        raise ValidacaoError(f"{campo} não pode ser vazio.")


def validar_preco(preco: float) -> None:
    if preco <= 0:
        raise ValidacaoError("Preço deve ser positivo.")


def validar_quantidade(quantidade: int) -> None:
    if quantidade < 0:
        raise ValidacaoError("Quantidade não pode ser negativa.")