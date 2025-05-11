# 🧠 Simple Interpreter with PLY

Este é um interpretador simples implementado em Python usando [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/). Ele permite avaliar expressões matemáticas, atribuições de variáveis, estruturas de controle e outras construções básicas de linguagem.

## ▶️ Como Executar

### Executar de forma interativa

```bash
make run
```

ou

```bash
python src/main.py
```

Depois, digite expressões ou caminhos de arquivos `.txt`. Digite `exit` para sair.

### Executar um arquivo de exemplo

```
Enter expression or file path > examples/lootest1_basic.txt
```

## 📁 Exemplos

A pasta `examples/` contém diversos arquivos para testar recursos do interpretador, como:

* `test_script_extended.txt` — teste completo
* `test1_basic.txt` — expressões básicas
* `test2_if_else.txt` — condicionais
* `test3_while.txt` — loops
* `test4_functions.txt` — funções
* `test5_nested_blocks.txt` — blocos aninhados
* `test6_def.txt` — definições de funções

## ⚙️ Dependências

Instale as dependências com:

```bash
pip install -r requirements.txt
```

Dependências para linting:

```bash
pip install -r requirements-lint.txt
```

## 🧪 Verificações de Código

Formate e analise o código com:

```bash
make format      # Executa black + isort
make check       # Executa pylint + isort
make prepare-commit  # Executa tudo antes de um commit
```

## 📜 Licença

Este projeto é educacional e livre para uso acadêmico ou pessoal.
