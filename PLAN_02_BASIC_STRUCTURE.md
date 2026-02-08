# Plano 02: Estrutura Básica da Aplicação

## Objetivo
Criar a estrutura básica da aplicação com grid de 9 post-its

## Tarefas

### 2.1 Widget PostIt
- [ ] Criar classe `PostIt` herdando de `Container`
- [ ] Adicionar propriedades reativas:
  - `title: str` (título do post-it)
  - `content: str` (conteúdo do post-it)
  - `position: int` (posição no grid 0-8)
- [ ] Compor widget com:
  - Static para título
  - TextArea ou Static para conteúdo
  - Bordas e padding
- [ ] Adicionar cores/estilo visual de post-it

### 2.2 Layout Grid 3x3
- [ ] Criar Grid com 3 colunas e 3 linhas
- [ ] Configurar tamanhos automáticos/proporcionais
- [ ] Garantir que o grid ocupe toda a tela disponível

### 2.3 Aplicação Principal
- [ ] Criar classe `NotesApp` herdando de `App`
- [ ] Adicionar Header e Footer
- [ ] Inicializar grid com 9 post-its vazios
- [ ] Implementar composição básica
- [ ] Adicionar bindings básicos no Footer

### 2.4 Estilização CSS (style.tcss)
- [ ] Estilos para o grid (espaçamento, cores)
- [ ] Estilos para post-its (bordas, cores de fundo)
- [ ] Cores diferentes para cada post-it (ou alternância)
- [ ] Responsividade básica

## Resultado Esperado
Aplicação exibe grid 3x3 com 9 post-its vazios, cada um com título e área de conteúdo
