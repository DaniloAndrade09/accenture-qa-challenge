# language: pt

@frontend @webtables
Funcionalidade: Gerenciamento de funcionarios no Web Tables
  Como analista de Quality Engineering
  Quero cadastrar, editar e excluir funcionarios
  Para validar as operacoes da tabela

  Cenário: Cadastrar, editar e excluir um funcionario
    Dado que acesso a pagina Web Tables
    Quando cadastro um novo funcionario
    Então o funcionario deve aparecer na tabela
    Quando altero o salario do funcionario para 7500
    Então o novo salario deve aparecer na tabela
    Quando excluo o funcionario cadastrado
    Então o funcionario nao deve mais aparecer na tabela
  @bonus
  Cenário: Cadastrar e excluir 12 funcionarios automaticamente
    Dado que acesso a pagina Web Tables
    Quando cadastro 12 funcionarios diferentes
    Então os 12 funcionarios devem estar cadastrados
    Quando excluo os 12 funcionarios cadastrados
    Então nenhum dos 12 funcionarios deve permanecer na tabela