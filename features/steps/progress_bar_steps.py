from behave import given, when, then

from pages.progress_bar_page import ProgressBarPage


@given("que acesso a pagina Progress Bar")
def acessar_progress_bar(context):
    context.progress_bar = ProgressBarPage(context.driver)
    context.progress_bar.abrir()


@when("inicio a barra de progresso")
def iniciar_barra(context):
    context.progress_bar.iniciar()


@when("interrompo o progresso antes de ultrapassar 25 por cento")
def interromper_barra(context):
    context.progresso_parado = (
        context.progress_bar.parar_antes_de_25()
    )
    print(
        f"Progresso interrompido: "
        f"{context.progresso_parado}%"
    )


@then("a barra deve estar parada em no maximo 25 por cento")
def validar_parada(context):
    valor = context.progress_bar.validar_parado()
    assert valor <= 25
    print(f"Parada validada: {valor}%")


@when("reinicio o progresso ate 100 por cento")
def reiniciar_progresso(context):
    context.progress_bar.aguardar_100()


@then("a barra deve indicar 100 por cento")
def validar_cem_por_cento(context):
    valor = context.progress_bar.progresso()
    assert valor == 100, (
        f"Esperado 100%, encontrado {valor}%"
    )
    print("Progresso concluido: 100%")


@when("reseto a barra de progresso")
def resetar_barra(context):
    context.progress_bar.resetar()


@then("a barra deve retornar a zero")
def validar_reset(context):
    valor = context.progress_bar.progresso()
    assert valor == 0, (
        f"Esperado 0%, encontrado {valor}%"
    )
    print("Reset validado: 0%")
