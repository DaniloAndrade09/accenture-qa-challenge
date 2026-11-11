import time
import sys
from pathlib import Path
from uuid import uuid4

from behave import given, when, then

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pages.web_tables_page import WebTablesPage


@given("que acesso a pagina Web Tables")
def acessar_tabela(context):
    context.tabela = WebTablesPage(context.driver)
    context.tabela.abrir()


@when("cadastro um novo funcionario")
def cadastrar_funcionario(context):
    context.email_funcionario = (
        f"qa_{uuid4().hex[:10]}@example.com"
    )

    context.tabela.cadastrar(
        nome="Teste",
        sobrenome="Accenture",
        email=context.email_funcionario,
        idade=30,
        salario=5000,
        departamento="Quality Engineering",
    )


@then("o funcionario deve aparecer na tabela")
def validar_cadastro(context):
    context.tabela.validar_registro(
        context.email_funcionario
    )


@when("altero o salario do funcionario para 7500")
def editar_funcionario(context):
    context.tabela.editar(
        context.email_funcionario,
        novo_salario=7500,
    )


@then("o novo salario deve aparecer na tabela")
def validar_edicao(context):
    context.tabela.validar_salario(
        context.email_funcionario,
        salario=7500,
    )


@when("excluo o funcionario cadastrado")
def excluir_funcionario(context):
    context.tabela.excluir(
        context.email_funcionario
    )


@then("o funcionario nao deve mais aparecer na tabela")
def validar_exclusao(context):
    context.tabela.validar_exclusao(
        context.email_funcionario
    )

@when("cadastro 12 funcionarios diferentes")
def cadastrar_doze_funcionarios(context):
    context.emails_bonus = []

    for indice in range(1, 13):
        email = f"qa_bonus_{uuid4().hex[:10]}@example.com"

        context.tabela.cadastrar(
            nome=f"Funcionario{indice}",
            sobrenome="Accenture",
            email=email,
            idade=25 + indice,
            salario=4000 + indice * 100,
            departamento="Quality Engineering",
        )

        context.tabela.validar_registro(email)
        context.emails_bonus.append(email)

    assert len(context.emails_bonus) == 12


@then("os 12 funcionarios devem estar cadastrados")
def validar_doze_funcionarios(context):
    assert len(context.emails_bonus) == 12

    for email in context.emails_bonus:
        context.tabela.validar_registro(email)



def diagnosticar_ids_antes_exclusao(context):
    from collections import Counter
    from selenium.webdriver.common.by import By

    linhas = context.tabela.driver.find_elements(
        By.CSS_SELECTOR, "tbody tr"
    )

    registros = []

    for linha in linhas:
        email = next(
            (e for e in context.emails_bonus if e in linha.text),
            None
        )

        if email:
            botao = linha.find_element(
                By.CSS_SELECTOR, "[id^='delete-record-']"
            )
            registros.append(
                (email, botao.get_attribute("id"))
            )

    print("\n=== IDS ANTES DA EXCLUSAO ===")

    for email, identificador in registros:
        print(email, "->", identificador)

    contagem = Counter(identificador for _, identificador in registros)

    print("Total encontrado:", len(registros))
    print(
        "IDs duplicados:",
        {k: v for k, v in contagem.items() if v > 1}
    )


@when("excluo os 12 funcionarios cadastrados")
def excluir_doze_funcionarios(context):
    diagnosticar_ids_antes_exclusao(context)
    emails = set(context.emails_bonus)

    # Limpar qualquer filtro anterior
    busca = context.tabela.driver.find_element("id", "searchBox")
    busca.clear()

    for numero in range(1, 13):
        # Restaurar a exibicao antes de cada exclusao
        context.tabela.configurar_paginacao(20)

        linhas = context.tabela.driver.find_elements(
            "css selector", "tbody tr"
        )

        encontrado = None
        email_encontrado = None

        for linha in linhas:
            for email in emails:
                if email in linha.text:
                    encontrado = linha
                    email_encontrado = email
                    break
            if encontrado:
                break

        if encontrado is None:
            from pathlib import Path

            pasta = Path("reports/diagnostico_webtables")
            pasta.mkdir(parents=True, exist_ok=True)

            driver = context.tabela.driver

            (pasta / "pagina.html").write_text(
                driver.page_source, encoding="utf-8"
            )

            driver.save_screenshot(
                str(pasta / "tela.png")
            )

            print("\n=== DIAGNOSTICO WEB TABLES ===")
            print("URL:", driver.current_url)
            print("Titulo:", driver.title)

            print("Linhas:", [
                linha.text
                for linha in driver.find_elements(
                    "css selector", "tbody tr"
                )
            ])

            print("Seletores de paginacao:", [
                (s.get_attribute("value"), s.get_attribute("outerHTML"))
                for s in driver.find_elements(
                    "css selector", "select"
                )
            ])

            print("Pesquisa:", [
                campo.get_attribute("value")
                for campo in driver.find_elements(
                    "id", "searchBox"
                )
            ])

            print("Diagnostico salvo em:", pasta.resolve())

            raise AssertionError(
                f"Nenhum registro de teste encontrado. "
                f"Restantes: {sorted(emails)}"
            )

        botao = encontrado.find_element(
            "css selector", "[id^='delete-record-']"
        )

        botao.click()

        from selenium.webdriver.support.ui import WebDriverWait

        WebDriverWait(context.tabela.driver, 15).until(
            lambda driver: not any(
                email_encontrado in linha.text
                for linha in driver.find_elements(
                    "css selector", "tbody tr"
                )
            )
        )

        emails.remove(email_encontrado)

        print(
            f"Exclusao {numero}/12 concluida. "
            f"Restantes: {len(emails)}"
        )

    assert not emails, f"Registros restantes: {emails}"


@then("nenhum dos 12 funcionarios deve permanecer na tabela")
def validar_exclusao_doze(context):
    for email in context.emails_bonus:
        context.tabela.validar_exclusao(email)
