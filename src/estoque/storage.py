import json
from pathlib import Path
from typing import List

from .produto import Produto


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "estoque.json"


class JSONStorage:
    def __init__(self, arquivo: Path = DATA_FILE) -> None:
        self.arquivo = arquivo
        self.arquivo.parent.mkdir(parents=True, exist_ok=True)

    def carregar(self) -> List[Produto]:
        if not self.arquivo.exists():
            return []

        with self.arquivo.open("r", encoding="utf-8") as file:
            dados = json.load(file)

        return [Produto.from_dict(item) for item in dados]

    def salvar(self, produtos: List[Produto]) -> None:
        dados = [produto.to_dict() for produto in produtos]

        with self.arquivo.open("w", encoding="utf-8") as file:
            json.dump(dados, file, indent=4, ensure_ascii=False)