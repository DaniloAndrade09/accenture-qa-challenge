from behave import given, when, then

from pages.sortable_page import SortablePage


@given("que acesso a pagina Sortable")
def acessar_sortable(context):
    context.sortable = SortablePage(context.driver)
    context.sortable.abrir()


@then("os elementos devem estar na ordem inicial")
def validar_ordem_inicial(context):
    context.sortable.validar_ordem_inicial()
    print("Ordem inicial validada:", context.sortable.obter_ordem())


@when("arrasto o ultimo elemento para a primeira posicao")
def arrastar_ultimo_elemento(context):
    context.sortable.mover_ultimo_para_primeiro()
    print("Drag and Drop executado")


@then("a lista deve refletir a nova ordem")
def validar_nova_ordem(context):
    context.sortable.validar_nova_ordem()
    print("Nova ordem validada:", context.sortable.obter_ordem())
