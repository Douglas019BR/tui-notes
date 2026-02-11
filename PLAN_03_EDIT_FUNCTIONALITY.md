# Plano 03: Funcionalidade de Edição

## Objetivo
Implementar edição de título e conteúdo dos post-its

## Tarefas

### 3.1 Modal de Edição
- [x] Criar `EditPostItScreen` herdando de `ModalScreen`
- [x] Adicionar Input para título
- [x] Adicionar TextArea para conteúdo
- [x] Adicionar botões "Save" e "Cancel"
- [x] Implementar retorno dos dados editados

### 3.2 Interação com PostIt
- [x] Adicionar evento de clique/seleção no PostIt
- [x] Ao clicar, abrir modal de edição com dados atuais
- [x] Ao salvar, atualizar título e conteúdo do PostIt
- [x] Adicionar feedback visual ao selecionar post-it

### 3.3 Bindings de Teclado
- [x] `e` - Editar post-it selecionado
- [x] `Enter` - Confirmar edição no modal
- [x] `Escape` - Cancelar edição

### 3.4 Navegação entre Post-its
- [x] Implementar foco/seleção entre post-its
- [x] Setas direcionais para navegar no grid
- [x] Indicador visual do post-it selecionado

## Resultado Esperado
Usuário pode navegar entre post-its e editar título/conteúdo de cada um através de modal
