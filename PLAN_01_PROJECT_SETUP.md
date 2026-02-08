# Plano 01: Configuração do Projeto

## Objetivo
Configurar a estrutura base do projeto tui-notes com Python e Textual

## Tarefas

### 1.1 Estrutura de Arquivos
- [ ] Criar `pyproject.toml` para configuração do projeto
- [ ] Criar `requirements.txt` com dependências
- [ ] Criar `.gitignore` para Python
- [ ] Criar `README.md` com descrição do projeto
- [ ] Criar estrutura de diretórios:
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
- [ ] Definir metadados do projeto (nome, versão, descrição)
- [ ] Configurar entry point: `tui-notes`
- [ ] Adicionar dependências (textual)
- [ ] Configurar para instalação via pip

### 1.3 Requirements
- [ ] textual>=0.50.0
- [ ] typing-extensions (se necessário para Python < 3.10)

### 1.4 Verificação
- [ ] Testar instalação local: `pip install -e .`
- [ ] Verificar comando: `tui-notes --help` ou `tui-notes`

## Resultado Esperado
Projeto instalável via pip que pode ser executado diretamente no terminal com o comando `tui-notes`
