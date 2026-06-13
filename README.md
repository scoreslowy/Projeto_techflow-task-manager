# TechFlow Task Manager

Sistema web acadêmico de gerenciamento de tarefas desenvolvido para a empresa fictícia **TechFlow Solutions**, atendendo a uma startup de logística que precisa acompanhar o fluxo de trabalho, priorizar atividades críticas e monitorar o andamento da equipe.

## Objetivo

Centralizar o cadastro e o acompanhamento das tarefas em um quadro simples, permitindo registrar, consultar, editar e excluir atividades do projeto.

## Escopo inicial

- Cadastro de tarefas com título e descrição;
- Consulta da lista de tarefas;
- Alteração do status entre A Fazer, Em Progresso e Concluído;
- Edição e exclusão de tarefas;
- Persistência local em SQLite;
- Testes automatizados;
- Integração contínua com GitHub Actions.

## Metodologia adotada

O projeto utiliza uma abordagem híbrida com **Kanban** para visualização do fluxo e práticas de **Scrum** para entregas incrementais. As tarefas são organizadas nas colunas `A Fazer`, `Em Progresso` e `Concluído`, com revisão frequente das prioridades.

## Tecnologias

- Python 3.11+
- Flask
- SQLite
- Pytest
- Ruff
- GitHub Actions

## Execução local

```bash
python -m venv .venv
```

No Windows:

```powershell
.venv\Scripts\activate
pip install -r requirements-dev.txt
$env:PYTHONPATH="src"
python app.py
```

No Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements-dev.txt
export PYTHONPATH=src
python app.py
```

Para inserir dados de demonstração antes de executar:

```bash
flask --app app seed-demo
```

Acesse `http://127.0.0.1:5000`.

## Testes e qualidade

```bash
pytest
ruff check .
```

## Organização

```text
src/        código-fonte
 tests/      testes automatizados
 docs/       documentação e diagramas
.github/    pipeline de integração contínua
```

## Licença

Projeto acadêmico distribuído sob licença MIT.
