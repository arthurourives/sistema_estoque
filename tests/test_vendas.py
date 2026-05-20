import tempfile
import unittest
from pathlib import Path

from estoque.estoque import Estoque
from estoque.exceptions import EstoqueInsuficienteError
from estoque.produto import Produto
from estoque.storage import JSONStorage


class TestVendas(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        arquivo = Path(self.temp_dir.name) / "teste_vendas.json"

        storage = JSONStorage(arquivo)

        self.estoque = Estoque(storage)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_venda_reduz_estoque(self):
        self.estoque.adicionar_produto(
            Produto(
                codigo="GPU001",
                nome="RTX",
                categoria="GPU",
                preco=5000,
                quantidade=10,
            )
        )

        self.estoque.registrar_venda("GPU001", 3)

        produto = self.estoque.buscar_produto("GPU001")

        self.assertEqual(produto.quantidade, 7)

    def test_venda_sem_estoque(self):
        self.estoque.adicionar_produto(
            Produto(
                codigo="GPU001",
                nome="RTX",
                categoria="GPU",
                preco=5000,
                quantidade=1,
            )
        )

        with self.assertRaises(EstoqueInsuficienteError):
            self.estoque.registrar_venda("GPU001", 5)


if __name__ == "__main__":
    unittest.main()