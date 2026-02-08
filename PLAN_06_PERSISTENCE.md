# Plano 06: Persistência de Dados

## Objetivo
Salvar e carregar post-its de arquivo para manter dados entre sessões

## Tarefas

### 6.1 Formato de Dados
- [ ] Escolher formato: JSON ou YAML
- [ ] Estrutura de dados:
  ```json
  {
    "post_its": [
      {
        "position": 0,
        "title": "Título",
        "content": "Conteúdo...",
        "color": "yellow"
      }
    ]
  }
  ```

### 6.2 Localização do Arquivo
- [ ] Usar diretório padrão do usuário
- [ ] Linux/Mac: `~/.config/tui-notes/notes.json`
- [ ] Windows: `%APPDATA%/tui-notes/notes.json`
- [ ] Criar diretório se não existir

### 6.3 Salvamento Automático
- [ ] Salvar ao editar post-it
- [ ] Salvar ao adicionar/remover post-it
- [ ] Salvar ao mover post-it
- [ ] Tratamento de erros de escrita

### 6.4 Carregamento
- [ ] Carregar dados ao iniciar aplicação
- [ ] Se arquivo não existir, iniciar com grid vazio
- [ ] Validação de dados carregados
- [ ] Tratamento de erros de leitura/formato

### 6.5 Bindings Adicionais
- [ ] `Ctrl+S` - Salvar manualmente (feedback visual)
- [ ] `Ctrl+R` - Recarregar do arquivo

## Resultado Esperado
Post-its são salvos automaticamente e restaurados ao reabrir a aplicação
