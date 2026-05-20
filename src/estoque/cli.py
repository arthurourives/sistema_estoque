import argparse
from typing import Iterable

from .estoque import Estoque
from .exceptions import EstoqueError
from .produto import Produto


class EstoqueArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage()

        if "unrecognized arguments:" in message:
            argumento = (
                message.split("unrecognized arguments:")[-1]
                .strip()
                .split()[0]
                .lstrip("-")
            )

            print(
                f"Erro: argumento inválido "
                f"'{argumento}'"
            )

            raise SystemExit(2)

        if "required" in message:
            print(
                "Erro: parâmetros obrigatórios ausentes."
            )

            raise SystemExit(2)

        if "invalid" in message:
            print(
                f"Erro: valor inválido."
            )

            raise SystemExit(2)

        print(f"Erro: {message}")

        raise SystemExit(2)

def imprimir_produtos(
    produtos: Iterable[Produto],
) -> None:
    for produto in produtos:
        print(
            f"[{produto.codigo}] "
            f"{produto.nome} | "
            f"{produto.categoria} | "
            f"R$ {produto.preco:.2f} | "
            f"Qtd: {produto.quantidade}"
        )


def imprimir_vendas(
    vendas: list[dict],
) -> None:
    for venda in vendas:
        print(
            f"[{venda['timestamp']}] "
            f"{venda['codigo']} | "
            f"{venda['nome']} | "
            f"Qtd: {venda['quantidade']} | "
            f"Unitário: R$ "
            f"{venda['valor_unitario']:.2f} | "
            f"Total: R$ "
            f"{venda['valor_total']:.2f}"
        )


def criar_parser() -> argparse.ArgumentParser:
    parser = EstoqueArgumentParser(
        prog="estoque",
        description=(
            "Sistema CLI de gerenciamento "
            "de estoque"
        ),
    )

    subparsers = parser.add_subparsers(
        dest="comando"
    )

    cadastrar = subparsers.add_parser(
        "cadastrar"
    )

    cadastrar.add_argument(
        "--codigo",
        required=True,
    )

    cadastrar.add_argument(
        "--nome",
        required=True,
    )

    cadastrar.add_argument(
        "--categoria",
        required=True,
    )

    cadastrar.add_argument(
        "--preco",
        type=float,
        required=True,
    )

    cadastrar.add_argument(
        "--quantidade",
        type=int,
        required=True,
    )

    subparsers.add_parser("listar")

    buscar = subparsers.add_parser(
        "buscar"
    )

    buscar.add_argument(
        "--codigo",
        required=True,
    )

    buscar_nome = subparsers.add_parser(
        "buscar-nome"
    )

    buscar_nome.add_argument(
        "--nome",
        required=True,
    )

    remover = subparsers.add_parser(
        "remover"
    )

    remover.add_argument(
        "--codigo",
        required=True,
    )

    editar = subparsers.add_parser(
        "editar"
    )

    editar.add_argument(
        "--codigo",
        required=True,
    )

    editar.add_argument("--nome")

    editar.add_argument("--categoria")

    editar.add_argument(
        "--preco",
        type=float,
    )

    editar.add_argument(
        "--quantidade",
        type=int,
    )

    venda = subparsers.add_parser(
        "vender"
    )

    venda.add_argument(
        "--codigo",
        required=True,
    )

    venda.add_argument(
        "--quantidade",
        type=int,
        required=True,
    )

    categoria = subparsers.add_parser(
        "categoria"
    )

    categoria.add_argument(
        "--nome",
        required=True,
    )

    baixo = subparsers.add_parser(
        "estoque-baixo"
    )

    baixo.add_argument(
        "--limite",
        type=int,
        default=5,
    )

    subparsers.add_parser(
        "menor-preco"
    )

    subparsers.add_parser(
        "maior-preco"
    )

    subparsers.add_parser(
        "listar-vendas"
    )

    return parser


def main() -> None:
    parser = criar_parser()

    args = parser.parse_args()

    estoque = Estoque()

    try:
        match args.comando:
            case "cadastrar":
                produto = Produto(
                    codigo=args.codigo,
                    nome=args.nome,
                    categoria=args.categoria,
                    preco=args.preco,
                    quantidade=args.quantidade,
                )

                estoque.adicionar_produto(
                    produto
                )

                print(
                    "Produto cadastrado "
                    "com sucesso."
                )

            case "listar":
                imprimir_produtos(
                    estoque.listar_produtos()
                )

            case "buscar":
                produto = estoque.buscar_produto(
                    args.codigo
                )

                if not produto:
                    print(
                        "Produto não encontrado."
                    )

                    return

                imprimir_produtos([produto])

            case "buscar-nome":
                produtos = (
                    estoque.buscar_por_nome(
                        args.nome
                    )
                )

                if not produtos:
                    print(
                        "Nenhum produto encontrado."
                    )

                    return

                imprimir_produtos(produtos)

            case "remover":
                estoque.remover_produto(
                    args.codigo
                )

                print(
                    "Produto removido "
                    "com sucesso."
                )

            case "editar":
                produto = (
                    estoque.editar_produto(
                        codigo=args.codigo,
                        nome=args.nome,
                        categoria=args.categoria,
                        preco=args.preco,
                        quantidade=args.quantidade,
                    )
                )

                print("Produto atualizado:")

                imprimir_produtos([produto])

            case "vender":
                produto = (
                    estoque.registrar_venda(
                        codigo=args.codigo,
                        quantidade=args.quantidade,
                    )
                )

                print("Venda registrada:")

                imprimir_produtos([produto])

            case "categoria":
                produtos = (
                    estoque.listar_por_categoria(
                        args.nome
                    )
                )

                imprimir_produtos(produtos)

            case "estoque-baixo":
                produtos = (
                    estoque.relatorio_estoque_baixo(
                        args.limite
                    )
                )

                imprimir_produtos(produtos)

            case "menor-preco":
                produto = (
                    estoque.produto_menor_preco()
                )

                if produto:
                    imprimir_produtos(
                        [produto]
                    )

            case "maior-preco":
                produto = (
                    estoque.produto_maior_preco()
                )

                if produto:
                    imprimir_produtos(
                        [produto]
                    )

            case "listar-vendas":
                vendas = (
                    estoque.listar_vendas()
                )

                if not vendas:
                    print(
                        "Nenhuma venda registrada."
                    )

                    return

                imprimir_vendas(vendas)

            case _:
                parser.print_help()

    except EstoqueError as erro:
        print(f"Erro: {erro}")