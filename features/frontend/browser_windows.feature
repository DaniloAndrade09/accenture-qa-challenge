# language: pt

@frontend
Funcionalidade: Gerenciamento de janelas no DemoQA
  Como analista de Quality Engineering
  Quero validar a abertura de uma nova janela
  Para garantir o funcionamento da navegacao

  Cenário: Abrir uma nova janela e validar seu conteudo
    Dado que acesso a pagina Browser Windows
    Quando clico no botao para abrir uma nova janela
    Então devo visualizar a mensagem This is a sample page
    E devo conseguir fechar a nova janela