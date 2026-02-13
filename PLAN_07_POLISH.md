# Plano 07: Refinamentos e Melhorias

## Objetivo
Adicionar recursos adicionais e melhorar experiência do usuário

## Tarefas

### 7.1 Cores Personalizadas
- [x] Permitir escolher cor do post-it
- [x] Paleta de 6 cores (amarelo, verde, azul, rosa, laranja, roxo)
- [x] Binding `c` - Change color com modal de seleção
- [x] Salvar cor na persistência

### 7.2 Busca e Filtros
- [ ] Binding `/` - Abrir busca
- [ ] Buscar em títulos e conteúdos
- [ ] Destacar post-its que correspondem
- [ ] `n` / `N` - Próximo/anterior resultado

### 7.3 Temas
- [ ] Tema claro e escuro
- [ ] Binding `t` - Toggle theme
- [ ] Ajustar cores dos post-its para cada tema
- [ ] Salvar preferência de tema

### 7.4 Estatísticas
- [x] Contador de post-its no subtitle (via move_mode watcher)

### 7.5 Exportação
- [x] Binding `Ctrl+E` - Export para markdown
- [x] Exportar todos post-its para ~/tui-notes-export.md
- [x] Formato legível com títulos e conteúdos

### 7.6 Help Screen
- [x] Binding `?` - Mostrar ajuda
- [x] Listar todos os atalhos de teclado
- [x] Instruções de uso
- [x] Modal dedicada

### 7.7 Melhorias de UX
- [x] Mensagens de feedback (toast/notificações) — já existia
- [x] Confirmações para ações destrutivas — já existia

## Resultado Esperado
Aplicação polida com recursos adicionais e excelente experiência de usuário
