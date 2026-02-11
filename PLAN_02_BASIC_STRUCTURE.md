# Plano 02: Estrutura Básica da Aplicação

## Objetivo
Criar a estrutura básica da aplicação com grid de 9 post-its

## Tarefas

### 2.1 Widget PostIt
- [x] Criar classe `PostIt` herdando de `Container`
- [x] Adicionar propriedades reativas:
  - `title: str` (título do post-it)
  - `content: str` (conteúdo do post-it)
  - `position: int` (posição no grid 0-8)
- [x] Compor widget com:
  - Static para título
  - TextArea ou Static para conteúdo
  - Bordas e padding
- [x] Adicionar cores/estilo visual de post-it

### 2.2 Layout Grid 3x3
- [x] Criar Grid com 3 colunas e 3 linhas
- [x] Configurar tamanhos automáticos/proporcionais
- [x] Garantir que o grid ocupe toda a tela disponível

### 2.3 Aplicação Principal
- [x] Criar classe `NotesApp` herdando de `App`
- [x] Adicionar Header e Footer
- [x] Inicializar grid com 9 post-its vazios
- [x] Implementar composição básica
- [x] Adicionar bindings básicos no Footer

### 2.4 Estilização CSS (style.tcss)
- [x] Estilos para o grid (espaçamento, cores)
- [x] Estilos para post-its (bordas, cores de fundo)
- [x] Cores diferentes para cada post-it (ou alternância)
- [x] Responsividade básica

## Resultado Esperado
Aplicação exibe grid 3x3 com 9 post-its vazios, cada um com título e área de conteúdo
