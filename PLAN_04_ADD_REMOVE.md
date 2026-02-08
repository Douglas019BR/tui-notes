# Plano 04: Adicionar e Remover Post-its

## Objetivo
Implementar funcionalidade de adicionar e remover post-its com rearranjo automático

## Tarefas

### 4.1 Gerenciamento de Post-its
- [ ] Criar lista/dicionário para gerenciar post-its ativos
- [ ] Rastrear posições ocupadas (0-8)
- [ ] Implementar lógica de encontrar próxima posição livre

### 4.2 Adicionar Post-it
- [ ] Binding `a` - Add post-it
- [ ] Verificar se há espaço disponível (máximo 9)
- [ ] Criar novo post-it na primeira posição livre
- [ ] Opcionalmente: modal para título inicial
- [ ] Feedback se grid estiver cheio

### 4.3 Remover Post-it
- [ ] Binding `x` ou `d` - Delete/Remove post-it selecionado
- [ ] Modal de confirmação (opcional)
- [ ] Remover post-it e liberar posição
- [ ] Rearranjar post-its restantes

### 4.4 Rearranjo Automático
- [ ] Ao remover, mover post-its para ocupar espaços vazios
- [ ] Manter ordem sequencial (0-8)
- [ ] Atualizar propriedade `position` dos post-its
- [ ] Animar transição (opcional, se Textual suportar)

### 4.5 Post-it Vazio/Placeholder
- [ ] Exibir placeholder visual em posições vazias
- [ ] Texto indicativo: "Vazio - Pressione 'a' para adicionar"
- [ ] Estilo diferenciado (tracejado, cor suave)

## Resultado Esperado
Usuário pode adicionar até 9 post-its e remover qualquer um, com rearranjo automático das posições
