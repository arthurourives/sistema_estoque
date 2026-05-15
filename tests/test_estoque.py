from estoque.produto import Produto


def test_produto_criado():
    produto = Produto(
        codigo="CPU-001",
        nome="Ryzen 7",
        categoria="Processador",
        preco=1500.0,
        quantidade=5
    )

    assert produto.codigo == "CPU-001"