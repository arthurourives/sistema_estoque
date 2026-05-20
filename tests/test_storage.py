import tempfile
import unittest
from pathlib import Path

from estoque.estoque import Estoque
from estoque.produto import Produto
from estoque.storage import JSONStorage


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.arquivo = (
            Path(self.temp_dir.name) / "dados.json"
        )

        self.storage = JSONStorage(self.arquivo)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_persistencia(self):
        estoque = Estoque(self.storage)

        estoque.adicionar_produto(
            Produto(
                codigo="SSD001",
                nome="SSD NVME",
                categoria="Armazenamento",
                preco=500,
                quantidade=3,
            )
        )

        novo_estoque = Estoque(self.storage)

        produto = novo_estoque.buscar_produto("SSD001")

        self.assertIsNotNone(produto)
        self.assertEqual(produto.nome, "SSD NVME")


if __name__ == "__main__":
    unittest.main()