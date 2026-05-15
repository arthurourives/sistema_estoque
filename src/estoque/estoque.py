import json
from pathlib import Path

from .produto import Produto


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "estoque.json"


class Estoque:
    def __init__(self, arquivo=DATA_FILE):
        self.arquivo = Path(arquivo)

        self.produtos_nao_ordenados = []
        self.produtos_ordenados = []

        self._carregar_dados()

    def adicionar_produto(self, produto):
        if self.buscar_produto(produto.codigo):
            raise ValueError("Já existe um produto com esse código.")

        self.produtos_nao_ordenados.append(produto)

        self._inserir_ordenado(produto)

        self._salvar_dados()

    def _inserir_ordenado(self, novo_produto):
        posicao = 0

        for i, produto in enumerate(self.produtos_ordenados):
            if novo_produto.codigo > produto.codigo:
                posicao = i + 1
            else:
                break

        self.produtos_ordenados.insert(posicao, novo_produto)

    def buscar_produto(self, codigo):
        for produto in self.produtos_ordenados:
            if produto.codigo == codigo:
                return produto

        return None

    def listar_produtos(self):
        return self.produtos_ordenados

    def remover_produto(self, codigo):
        produto = self.buscar_produto(codigo)

        if not produto:
            return False

        self.produtos_nao_ordenados.remove(produto)
        self.produtos_ordenados.remove(produto)

        self._salvar_dados()

        return True

    def atualizar_quantidade(self, codigo, quantidade):
        produto = self.buscar_produto(codigo)

        if not produto:
            raise ValueError("Produto não encontrado.")

        if quantidade < 0:
            raise ValueError("Quantidade inválida.")

        produto.quantidade = quantidade

        self._salvar_dados()

    def _salvar_dados(self):
        self.arquivo.parent.mkdir(parents=True, exist_ok=True)

        dados = []

        for produto in self.produtos_nao_ordenados:
            dados.append({
                "codigo": produto.codigo,
                "nome": produto.nome,
                "categoria": produto.categoria,
                "preco": produto.preco,
                "quantidade": produto.quantidade
            })

        with open(self.arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(
                dados,
                arquivo,
                indent=4,
                ensure_ascii=False
            )

    def _carregar_dados(self):
        if not self.arquivo.exists():
            return

        try:
            with open(self.arquivo, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            for item in dados:
                produto = Produto(
                    item["codigo"],
                    item["nome"],
                    item["categoria"],
                    item["preco"],
                    item["quantidade"]
                )

                self.produtos_nao_ordenados.append(produto)

                self._inserir_ordenado(produto)

        except json.JSONDecodeError:
            pass