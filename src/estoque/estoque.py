import logging
from typing import List

from .exceptions import (
    EstoqueInsuficienteError,
    ProdutoDuplicadoError,
    ProdutoNaoEncontradoError,
)
from .produto import Produto
from .storage import JSONStorage
from .validators import (
    validar_codigo,
    validar_preco,
    validar_quantidade,
    validar_texto,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)


class Estoque:
    """
    Estrutura principal do sistema.

    Mantém:
    - vetor ordenado por código
    - busca binária
    - vetor não ordenado para busca linear
    """

    def __init__(self, storage: JSONStorage | None = None) -> None:
        self.storage = storage or JSONStorage()

        self._produtos: List[Produto] = self.storage.carregar()

        self._produtos.sort(key=lambda produto: produto.codigo)

    @property
    def produtos(self) -> List[Produto]:
        return self._produtos

    def adicionar_produto(self, produto: Produto) -> None:
        validar_codigo(produto.codigo)
        validar_texto(produto.nome, "Nome")
        validar_texto(produto.categoria, "Categoria")
        validar_preco(produto.preco)
        validar_quantidade(produto.quantidade)

        if self.buscar_produto(produto.codigo):
            raise ProdutoDuplicadoError(
                f"Produto '{produto.codigo}' já existe."
            )

        self._inserir_ordenado(produto)

        self.storage.salvar(self._produtos)

        logging.info("Produto cadastrado: %s", produto.codigo)

    def _inserir_ordenado(self, produto: Produto) -> None:
        indice = 0

        while (
            indice < len(self._produtos)
            and self._produtos[indice].codigo < produto.codigo
        ):
            indice += 1

        self._produtos.insert(indice, produto)

    def buscar_produto(self, codigo: str) -> Produto | None:
        """
        Busca binária manual.
        Complexidade:
        O(log n)
        """

        esquerda = 0
        direita = len(self._produtos) - 1

        while esquerda <= direita:
            meio = (esquerda + direita) // 2

            produto = self._produtos[meio]

            if produto.codigo == codigo:
                return produto

            if produto.codigo < codigo:
                esquerda = meio + 1
            else:
                direita = meio - 1

        return None

    def buscar_por_nome(self, nome: str) -> List[Produto]:
        """
        Busca linear em vetor não ordenado.
        Complexidade:
        O(n)
        """

        termo = nome.lower()

        return [
            produto
            for produto in self._produtos
            if termo in produto.nome.lower()
        ]

    def listar_produtos(self) -> List[Produto]:
        return self._produtos

    def listar_por_categoria(self, categoria: str) -> List[Produto]:
        categoria = categoria.lower()

        return [
            produto
            for produto in self._produtos
            if produto.categoria.lower() == categoria
        ]

    def remover_produto(self, codigo: str) -> None:
        produto = self.buscar_produto(codigo)

        if not produto:
            raise ProdutoNaoEncontradoError(
                f"Produto '{codigo}' não encontrado."
            )

        self._produtos.remove(produto)

        self.storage.salvar(self._produtos)

        logging.info("Produto removido: %s", codigo)

    def editar_produto(
        self,
        codigo: str,
        nome: str | None = None,
        categoria: str | None = None,
        preco: float | None = None,
        quantidade: int | None = None,
    ) -> Produto:
        produto = self.buscar_produto(codigo)

        if not produto:
            raise ProdutoNaoEncontradoError(
                f"Produto '{codigo}' não encontrado."
            )

        if nome is not None:
            validar_texto(nome, "Nome")
            produto.nome = nome

        if categoria is not None:
            validar_texto(categoria, "Categoria")
            produto.categoria = categoria

        if preco is not None:
            validar_preco(preco)
            produto.preco = preco

        if quantidade is not None:
            validar_quantidade(quantidade)
            produto.quantidade = quantidade

        self.storage.salvar(self._produtos)

        logging.info("Produto atualizado: %s", codigo)

        return produto

    def registrar_venda(self, codigo: str, quantidade: int) -> Produto:
        validar_quantidade(quantidade)

        produto = self.buscar_produto(codigo)

        if not produto:
            raise ProdutoNaoEncontradoError(
                f"Produto '{codigo}' não encontrado."
            )

        if produto.quantidade < quantidade:
            raise EstoqueInsuficienteError(
                "Estoque insuficiente para venda."
            )

        produto.quantidade -= quantidade

        self.storage.salvar(self._produtos)

        logging.info(
            "Venda registrada: %s (%s unidades)",
            codigo,
            quantidade,
        )

        return produto

    def relatorio_estoque_baixo(
        self,
        limite: int = 5,
    ) -> List[Produto]:
        return [
            produto
            for produto in self._produtos
            if produto.quantidade <= limite
        ]

    def produto_menor_preco(self) -> Produto | None:
        if not self._produtos:
            return None

        return min(self._produtos, key=lambda produto: produto.preco)

    def produto_maior_preco(self) -> Produto | None:
        if not self._produtos:
            return None

        return max(self._produtos, key=lambda produto: produto.preco)