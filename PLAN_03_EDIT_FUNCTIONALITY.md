# Plano 03: Funcionalidade de Edição

## Objetivo
Implementar edição de título e conteúdo dos post-its

## Tarefas

### 3.1 Modal de Edição
- [ ] Criar `EditPostItScreen` herdando de `ModalScreen`
- [ ] Adicionar Input para título
- [ ] Adicionar TextArea para conteúdo
- [ ] Adicionar botões "Save" e "Cancel"
- [ ] Implementar retorno dos dados editados

### 3.2 Interação com PostIt
- [ ] Adicionar evento de clique/seleção no PostIt
- [ ] Ao clicar, abrir modal de edição com dados atuais
- [ ] Ao salvar, atualizar título e conteúdo do PostIt
- [ ] Adicionar feedback visual ao selecionar post-it

### 3.3 Bindings de Teclado
- [ ] `e` - Editar post-it selecionado
- [ ] `Enter` - Confirmar edição no modal
- [ ] `Escape` - Cancelar edição

### 3.4 Navegação entre Post-its
- [ ] Implementar foco/seleção entre post-its
- [ ] Setas direcionais para navegar no grid
- [ ] Indicador visual do post-it selecionado

## Resultado Esperado
Usuário pode navegar entre post-its e editar título/conteúdo de cada um através de modal
