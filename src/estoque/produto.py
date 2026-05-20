from dataclasses import dataclass, asdict


@dataclass(slots=True)
class Produto:
    codigo: str
    nome: str
    categoria: str
    preco: float
    quantidade: int

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Produto":
        return cls(
            codigo=data["codigo"],
            nome=data["nome"],
            categoria=data["categoria"],
            preco=float(data["preco"]),
            quantidade=int(data["quantidade"]),
        )

    def __repr__(self) -> str:
        return (
            f"Produto(codigo='{self.codigo}', "
            f"nome='{self.nome}', "
            f"categoria='{self.categoria}', "
            f"preco={self.preco}, "
            f"quantidade={self.quantidade})"
        )