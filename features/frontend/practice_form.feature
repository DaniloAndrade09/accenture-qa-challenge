# language: pt

@frontend
Funcionalidade: Preenchimento do Practice Form
  Como analista de Quality Engineering
  Quero automatizar o formulario DemoQA
  Para validar o envio e a confirmacao dos dados

  Cenário: Preencher e enviar o formulario com sucesso
    Dado que acesso o formulario Practice Form
    Quando preencho todos os campos do formulario
    E envio o formulario
    Então devo visualizar o popup de confirmacao
    E devo conseguir fechar o popup