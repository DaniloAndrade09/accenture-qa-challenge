import sys
from pathlib import Path

from behave import given, when, then

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pages.practice_form_page import PracticeFormPage


@given("que acesso o formulario Practice Form")
def acessar_formulario(context):
    context.formulario = PracticeFormPage(context.driver)
    context.formulario.abrir()


@when("preencho todos os campos do formulario")
def preencher_formulario(context):
    context.formulario.preencher()


@when("envio o formulario")
def enviar_formulario(context):
    context.formulario.enviar()


@then("devo visualizar o popup de confirmacao")
def validar_confirmacao(context):
    context.formulario.validar_popup()


@then("devo conseguir fechar o popup")
def fechar_confirmacao(context):
    context.formulario.fechar_popup()
