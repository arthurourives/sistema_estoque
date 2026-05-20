import tempfile
import unittest
from pathlib import Path

from estoque.estoque import Estoque
from estoque.produto import Produto
from estoque.storage import JSONStorage


class TestBusca(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        arquivo = Path(self.temp_dir.name) / "teste_busca.json"

        storage = JSONStorage(arquivo)

        self.estoque = Estoque(storage)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_busca_binaria(self):
        self.estoque.adicionar_produto(
            Produto(
                codigo="A001",
                nome="Mouse",
                categoria="Periférico",
                preco=100,
                quantidade=5,
            )
        )

        self.estoque.adicionar_produto(
            Produto(
                codigo="A002",
                nome="Teclado",
                categoria="Periférico",
                preco=200,
                quantidade=5,
            )
        )

        produto = self.estoque.buscar_produto("A002")

        self.assertIsNotNone(produto)
        self.assertEqual(produto.nome, "Teclado")

    def test_busca_nome(self):
        self.estoque.adicionar_produto(
            Produto(
                codigo="A001",
                nome="Mouse Gamer",
                categoria="Periférico",
                preco=100,
                quantidade=5,
            )
        )

        resultados = self.estoque.buscar_por_nome("mouse")

        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].codigo, "A001")


if __name__ == "__main__":
    unittest.main()