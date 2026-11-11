# language: pt

Funcionalidade: Gerenciamento de livros via API DemoQA
  Como usuário da plataforma DemoQA
  Quero criar minha conta e reservar livros
  Para validar o funcionamento da API BookStore

  @api
  Cenário: Criar usuário e reservar dois livros com sucesso
    Dado que eu crio um novo usuário na API DemoQA
    E que eu gero um token de acesso válido
    E que o usuário está autorizado
    Quando eu consulto os livros disponíveis
    E seleciono dois livros diferentes
    E adiciono os dois livros à coleção do usuário
    Então a API deve retornar os dados do usuário
    E os dois livros selecionados devem estar na coleção
