# language: pt
@frontend @progressbar
Funcionalidade: Controle da barra de progresso
  Como analista de Quality Engineering
  Quero controlar a barra de progresso
  Para validar inicio, parada, conclusao e reset

  Cenario: Controlar o progresso ate a conclusao
    Dado que acesso a pagina Progress Bar
    Quando inicio a barra de progresso
    E interrompo o progresso antes de ultrapassar 25 por cento
    Entao a barra deve estar parada em no maximo 25 por cento
    Quando reinicio o progresso ate 100 por cento
    Entao a barra deve indicar 100 por cento
    Quando reseto a barra de progresso
    Entao a barra deve retornar a zero
