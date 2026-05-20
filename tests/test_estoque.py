import tempfile
import unittest
from pathlib import Path

from estoque.estoque import Estoque
from estoque.produto import Produto
from estoque.storage import JSONStorage


class TestEstoque(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        arquivo = Path(self.temp_dir.name) / "teste.json"

        storage = JSONStorage(arquivo)

        self.estoque = Estoque(storage)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_cadastro_produto(self):
        produto = Produto(
            codigo="CPU001",
            nome="Ryzen",
            categoria="CPU",
            preco=1000,
            quantidade=10,
        )

        self.estoque.adicionar_produto(produto)

        resultado = self.estoque.buscar_produto("CPU001")

        self.assertIsNotNone(resultado)


if __name__ == "__main__":
    unittest.main()