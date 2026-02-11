# Plano 05: Mover e Reordenar Post-its

## Objetivo
Implementar funcionalidade de mover post-its entre posições do grid

## Tarefas

### 5.1 Modo de Movimentação
- [x] Binding `m` - Entrar em modo "Move"
- [x] Indicador visual do modo move ativo
- [x] Selecionar post-it para mover
- [x] Setas direcionais para mover post-it

### 5.2 Lógica de Troca
- [x] Implementar swap entre duas posições
- [ ] Mover post-it para posição vazia (swap apenas entre post-its)
- [x] Trocar post-its de posição
- [x] Atualizar propriedade `position` de ambos

### 5.3 Feedback Visual
- [x] Destacar post-it sendo movido
- [x] Indicar posição de destino
- [x] Animação ou efeito de movimento
- [x] Confirmar com Enter, cancelar com Escape

### 5.4 Alternativa: Drag & Drop
- [ ] ⚠️ Implementado mas não funcional — Textual não tem drag & drop nativo; implementação via mouse events precisa de ajustes
- [ ] Clicar e arrastar post-it
- [ ] Soltar em nova posição

### 5.5 Atalhos de Posição
- [ ] Números 1-9: mover post-it selecionado para posição específica
- [ ] Shift + números: trocar posições diretamente

### 5.6 Navegação por Setas (extra)
- [x] Setas direcionais navegam entre post-its/slots no modo normal
- [x] Validação de bounds para evitar erros de index

## Resultado Esperado
Usuário pode reorganizar post-its livremente entre as 9 posições do grid
