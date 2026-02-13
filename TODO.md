# TUI Notes — TODO

> Gerado em 2026-02-13. Revisão de todos os planos (PLAN_01 a PLAN_09).

## Resumo

| Plano | Status | Pendente |
|-------|--------|----------|
| PLAN 01 — Project Setup | ✅ Completo | — |
| PLAN 02 — Basic Structure | ✅ Completo | — |
| PLAN 03 — Edit Functionality | ✅ Completo | — |
| PLAN 04 — Add/Remove | ✅ Completo | — |
| PLAN 05 — Move/Reorder | ⚠️ Parcial | 2 itens pendentes |
| PLAN 06 — Persistence | ✅ Completo | — |
| PLAN 07 — Polish | ⚠️ Parcial | 7 itens pendentes |
| PLAN 08 — Testing | ✅ Completo | — |
| PLAN 09 — Deployment | ⚠️ Parcial | 10 itens pendentes |
| Refactoring (SOLID/DRY/KISS) | ✅ Completo | — |

**Total: 115 feitos / 19 pendentes / 1 não implementado (drag & drop)**

---

## Itens Pendentes por Plano

### PLAN 05 — Move/Reorder

- [ ] Atalhos numéricos 1-9: mover post-it selecionado para posição específica
- [ ] Shift + números: trocar posições diretamente

### PLAN 07 — Polish

#### 7.2 Busca e Filtros
- [ ] Binding `/` — Abrir busca
- [ ] Buscar em títulos e conteúdos
- [ ] Destacar post-its que correspondem
- [ ] `n` / `N` — Próximo/anterior resultado

#### 7.3 Temas
- [ ] Tema claro e escuro
- [ ] Binding `t` — Toggle theme
- [ ] Ajustar cores dos post-its para cada tema

### PLAN 09 — Deployment

#### 9.1 Documentação
- [ ] Criar CHANGELOG.md

#### 9.2 Instalação
- [ ] Testar em ambiente virtual limpo

#### 9.3 Publicação no PyPI (Opcional)
- [ ] Criar conta no PyPI
- [ ] Configurar token de autenticação
- [ ] Build: `python -m build`
- [ ] Upload: `twine upload dist/*`
- [ ] Testar instalação: `pip install tui-notes`

#### 9.4 GitHub Release
- [ ] Criar tag de versão (v1.0.0)
- [ ] Criar release no GitHub
- [ ] Adicionar notas de lançamento

#### 9.6 CI/CD (Opcional)
- [ ] GitHub Actions para testes automáticos
- [ ] GitHub Actions para publicação automática no PyPI

#### 9.7 Verificação Final
- [ ] Testar em macOS (se disponível)
- [ ] Testar em Windows (se disponível)

---

## Itens Não Implementados (decisão consciente)

- ~~Drag & Drop (PLAN 05.4)~~ — Textual não suporta drag & drop nativo

---

## Itens Concluídos (referência rápida)

<details>
<summary>Clique para expandir (115 itens)</summary>

### PLAN 01 — Project Setup ✅
- [x] pyproject.toml, requirements.txt, .gitignore, README.md
- [x] Estrutura de diretórios (tui_notes/, tests/)
- [x] Entry point `tui-notes`, instalação via pip

### PLAN 02 — Basic Structure ✅
- [x] Widget PostIt (Container, propriedades reativas)
- [x] Grid 3x3 com tamanhos automáticos
- [x] NotesApp com Header, Footer, bindings
- [x] Estilização CSS (cores alternadas, responsividade)

### PLAN 03 — Edit Functionality ✅
- [x] EditPostItScreen (ModalScreen)
- [x] Input para título, TextArea para conteúdo
- [x] Bindings: `e` editar, `Enter` confirmar, `Escape` cancelar
- [x] Navegação por setas, indicador visual de foco

### PLAN 04 — Add/Remove ✅
- [x] Gerenciamento de posições (0-8)
- [x] `a` adicionar, `d` remover com confirmação
- [x] EmptySlot placeholder em posições vazias
- [x] Grid mantém sempre 9 filhos

### PLAN 05 — Move/Reorder (parcial)
- [x] Modo Move (`m` + setas + `Enter`/`Escape`)
- [x] Swap entre PostIt↔PostIt e PostIt↔EmptySlot
- [x] Feedback visual (borda laranja no post-it sendo movido)

### PLAN 06 — Persistence ✅
- [x] JSON em ~/.config/tui-notes/notes.json (Linux)
- [x] Atomic writes via .tmp + rename
- [x] Auto-save em add/delete/edit/move
- [x] Ctrl+S salvar manual, Ctrl+R recarregar
- [x] Validação de dados na carga

### PLAN 07 — Polish (parcial)
- [x] Cores personalizadas (`c` — 6 cores)
- [x] Exportação Markdown (`Ctrl+E`)
- [x] Help Screen (`?`)
- [x] Contador de post-its no subtitle

### PLAN 08 — Testing ✅
- [x] 30 testes (16 storage + 14 app)
- [x] black, isort, pylint configurados (10/10)
- [x] Docstrings e type hints em todo o código

### PLAN 09 — Deployment (parcial)
- [x] README.md completo
- [x] `pip install -e .` e `tui-notes` funcionando
- [x] Documentação de instalação via git e pipx
- [x] Testado em Linux

### Refactoring ✅
- [x] Separação em widgets/, screens/, constants.py
- [x] PostIt.to_dict() / from_dict() (DRY)
- [x] Métodos extraídos (_swap_post_its, _move_to_empty, etc.)
- [x] _get_grid() helper, _calc_target_idx @staticmethod
- [x] _validate_note() em storage.py

</details>
