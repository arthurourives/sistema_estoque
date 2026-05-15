class Produto:
    def __init__(self, codigo, nome, categoria, preco, quantidade):
        if preco < 0:
            raise ValueError("O preço deve ser positivo.")

        if quantidade < 0:
            raise ValueError("A quantidade não pode ser negativa.")

        self.codigo = codigo
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
        self.quantidade = quantidade

    def __repr__(self):
        return (
            f"[{self.codigo}] "
            f"{self.nome} | "
            f"Categoria: {self.categoria} | "
            f"Preço: R$ {self.preco:.2f} | "
            f"Qtd: {self.quantidade}"
        )