# Plano 06: Persistência de Dados

## Objetivo
Salvar e carregar post-its de arquivo para manter dados entre sessões

## Tarefas

### 6.1 Formato de Dados
- [x] Escolher formato: JSON
- [x] Estrutura de dados com version e post_its

### 6.2 Localização do Arquivo
- [x] Usar diretório padrão do usuário
- [x] Linux: `~/.config/tui-notes/notes.json`
- [x] Mac: `~/Library/Application Support/tui-notes/notes.json`
- [x] Windows: `%APPDATA%/tui-notes/notes.json`
- [x] Criar diretório se não existir

### 6.3 Salvamento Automático
- [x] Salvar ao editar post-it
- [x] Salvar ao adicionar/remover post-it
- [x] Salvar ao mover post-it
- [x] Tratamento de erros de escrita (atomic write via .tmp)

### 6.4 Carregamento
- [x] Carregar dados ao iniciar aplicação
- [x] Se arquivo não existir, iniciar com grid vazio
- [x] Validação de dados carregados
- [x] Tratamento de erros de leitura/formato

### 6.5 Bindings Adicionais
- [x] `Ctrl+S` - Salvar manualmente (feedback visual)
- [x] `Ctrl+R` - Recarregar do arquivo

## Resultado Esperado
Post-its são salvos automaticamente e restaurados ao reabrir a aplicação
