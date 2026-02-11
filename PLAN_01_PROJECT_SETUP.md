# Plano 01: Configuração do Projeto

## Objetivo
Configurar a estrutura base do projeto tui-notes com Python e Textual

## Tarefas

### 1.1 Estrutura de Arquivos
- [x] Criar `pyproject.toml` para configuração do projeto
- [x] Criar `requirements.txt` com dependências
- [x] Criar `.gitignore` para Python
- [x] Criar `README.md` com descrição do projeto
- [x] Criar estrutura de diretórios:
  ```
  tui-notes/
  ├── tui_notes/
  │   ├── __init__.py
  │   ├── __main__.py
  │   ├── app.py
  │   └── style.tcss
  └── tests/
  ```

### 1.2 Configuração do pyproject.toml
- [x] Definir metadados do projeto (nome, versão, descrição)
- [x] Configurar entry point: `tui-notes`
- [x] Adicionar dependências (textual)
- [x] Configurar para instalação via pip

### 1.3 Requirements
- [x] textual>=0.50.0
- [x] typing-extensions (se necessário para Python < 3.10)

### 1.4 Verificação
- [x] Testar instalação local: `pip install -e .`
- [x] Verificar comando: `tui-notes --help` ou `tui-notes`

## Resultado Esperado
Projeto instalável via pip que pode ser executado diretamente no terminal com o comando `tui-notes`
