# Testes automatizados e integração contínua

## Estratégia de testes

O projeto utiliza Pytest para validar os fluxos essenciais do sistema:

1. disponibilidade do endpoint `/health`;
2. exibição de tarefas no quadro;
3. criação de tarefa válida;
4. rejeição de título inválido;
5. atualização de tarefa;
6. exclusão de tarefa;
7. retorno 404 para registros inexistentes.

Cada teste utiliza um banco SQLite temporário e independente. Isso evita interferência entre execuções e torna o resultado reproduzível.

## Pipeline

O workflow `.github/workflows/ci.yml` é executado em todo `push` e `pull_request` para a branch `main`. Ele:

- instala Python e as dependências;
- executa o Ruff para análise estática;
- executa a suíte do Pytest;
- calcula a cobertura de testes;
- publica `coverage.xml` como artefato da execução.

A integração contínua reduz o risco de introduzir regressões, pois qualquer alteração incompatível é sinalizada antes da entrega.
