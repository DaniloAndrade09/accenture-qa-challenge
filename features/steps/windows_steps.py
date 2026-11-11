import sys
from pathlib import Path

from behave import given, when, then

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pages.browser_windows_page import BrowserWindowsPage


@given("que acesso a pagina Browser Windows")
def acessar_browser_windows(context):
    context.browser_windows = BrowserWindowsPage(context.driver)
    context.browser_windows.abrir()


@when("clico no botao para abrir uma nova janela")
def abrir_nova_janela(context):
    context.browser_windows.abrir_nova_janela()


@then("devo visualizar a mensagem This is a sample page")
def validar_mensagem(context):
    context.browser_windows.validar_texto()


@then("devo conseguir fechar a nova janela")
def fechar_nova_janela(context):
    context.browser_windows.fechar_nova_janela()
