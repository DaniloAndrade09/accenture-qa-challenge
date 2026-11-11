# language: pt
@frontend @sortable
Funcionalidade: Reordenacao de elementos com Drag and Drop
  Como analista de Quality Engineering
  Quero reorganizar os elementos da lista
  Para validar a funcionalidade Sortable

  Cenario: Reorganizar os elementos da lista
    Dado que acesso a pagina Sortable
    Entao os elementos devem estar na ordem inicial
    Quando arrasto o ultimo elemento para a primeira posicao
    Entao a lista deve refletir a nova ordem
