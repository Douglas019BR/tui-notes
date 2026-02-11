# Plano 04: Adicionar e Remover Post-its

## Objetivo
Implementar funcionalidade de adicionar e remover post-its com rearranjo automático

## Tarefas

### 4.1 Gerenciamento de Post-its
- [x] Criar lista/dicionário para gerenciar post-its ativos
- [x] Rastrear posições ocupadas (0-8)
- [x] Implementar lógica de encontrar próxima posição livre

### 4.2 Adicionar Post-it
- [x] Binding `a` - Add post-it
- [x] Verificar se há espaço disponível (máximo 9)
- [x] Criar novo post-it na primeira posição livre
- [x] Opcionalmente: modal para título inicial
- [x] Feedback se grid estiver cheio

### 4.3 Remover Post-it
- [x] Binding `x` ou `d` - Delete/Remove post-it selecionado
- [x] Modal de confirmação (opcional)
- [x] Remover post-it e liberar posição
- [x] Rearranjar post-its restantes

### 4.4 Rearranjo Automático
- [x] Ao remover, mover post-its para ocupar espaços vazios
- [x] Manter ordem sequencial (0-8)
- [x] Atualizar propriedade `position` dos post-its
- [x] Animar transição (opcional, se Textual suportar)

### 4.5 Post-it Vazio/Placeholder
- [x] Exibir placeholder visual em posições vazias
- [x] Texto indicativo: "Vazio - Pressione 'a' para adicionar"
- [x] Estilo diferenciado (tracejado, cor suave)

## Resultado Esperado
Usuário pode adicionar até 9 post-its e remover qualquer um, com rearranjo automático das posições
