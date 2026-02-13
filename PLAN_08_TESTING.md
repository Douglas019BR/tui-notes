# Plano 08: Testes e Qualidade

## Objetivo
Garantir qualidade e confiabilidade do código

## Tarefas

### 8.1 Configuração de Testes
- [x] Instalar pytest
- [x] Instalar pytest-asyncio para testes async
- [x] Criar estrutura de testes em `tests/`
- [x] Configurar pyproject.toml (asyncio_mode, testpaths)

### 8.2 Testes Unitários
- [x] Testar classe PostIt (cor, título)
- [x] Testar gerenciamento de posições (grid 9 children)
- [x] Testar lógica de add/delete (grid mantém 9)
- [x] Testar lógica de move mode

### 8.3 Testes de Persistência
- [x] Testar salvamento de dados (JSON válido, unicode)
- [x] Testar carregamento de dados (roundtrip, color_index)
- [x] Testar criação de diretório (data dir/file paths)
- [x] Testar tratamento de erros (JSON inválido, estrutura errada, notas inválidas)

### 8.4 Testes de Integração
- [x] Testar fluxo completo: adicionar notas únicas
- [x] Testar fluxo: adicionar → deletar (grid mantém 9)
- [x] Testar edge cases (grid cheio com 9+, grid vazio)

### 8.5 Linting e Formatação
- [x] Configurar black (formatação)
- [x] Configurar pylint (linting) — 10/10
- [x] Configurar isort (import sorting)
- [x] Criar requirements-dev.txt com todas as ferramentas

### 8.6 Documentação do Código
- [x] Docstrings em classes principais
- [x] Type hints
- [x] Documentar estrutura de dados (storage.py)

## Resultado Esperado
Código bem testado, formatado e documentado seguindo boas práticas
