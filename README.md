# Sistema de Estoque de Hardware

CLI em Python para gerenciamento de estoque de hardware com persistência local em JSON.

## Funcionalidades

- Cadastro de produtos
- Edição de produtos
- Remoção de produtos
- Busca binária por código
- Busca por nome
- Registro de vendas
- Relatórios de estoque
- Persistência em JSON
- Testes automatizados

---

# Instalação

Clone o repositório:

```bash
git clone <repositorio>
cd sistema-estoque
```

Instale o projeto:

```bash
pip install -e .
```

---

# Uso

## Listar produtos

```bash
estoque listar
```

## Cadastrar produto

```bash
estoque cadastrar --codigo CPU001 --nome "Ryzen 7 7800X3D" --categoria Processador --preco 2899.90 --quantidade 10
```

## Buscar por código

```bash
estoque buscar --codigo CPU001
```

## Buscar por nome

```bash
estoque buscar-nome --nome Ryzen
```

## Editar produto

```bash
estoque editar --codigo CPU001 --preco 2599.90 --quantidade 8
```

## Registrar venda

```bash
estoque vender --codigo CPU001 --quantidade 2
```

## Remover produto

```bash
estoque remover --codigo CPU001
```

## Produtos por categoria

```bash
estoque categoria --nome Processador
```

## Relatório de estoque baixo

```bash
estoque estoque-baixo --limite 5
```

## Produto mais caro

```bash
estoque maior-preco
```

## Produto mais barato

```bash
estoque menor-preco
```

---

# Estrutura do Projeto

```text
src/estoque/
├── cli.py
├── estoque.py
├── produto.py
├── storage.py
├── validators.py
└── exceptions.py
```

---

# Persistência

Os dados são armazenados localmente em:

```text
data/estoque.json
```

---

# Testes

Executar todos os testes:

```bash
python -m unittest discover
```

---

# Tecnologias

- Python 3.10+
- argparse
- pathlib
- dataclasses
- unittest
- JSON