import sys
from pathlib import Path
from uuid import uuid4

from behave import given, when, then

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from clients.bookstore_api import BookStoreAPI


def validar_status(response, esperado, etapa):
    assert response.status_code == esperado, (
        f"{etapa} falhou. "
        f"HTTP esperado: {esperado}. "
        f"HTTP recebido: {response.status_code}. "
        f"Resposta: {response.text[:500]}"
    )


@given("que eu crio um novo usuário na API DemoQA")
def criar_usuario(context):
    context.api = BookStoreAPI()
    context.username = f"accenture_qa_{uuid4().hex[:12]}"
    context.password = "Qa@2026TesteSeguro!"

    response = context.api.create_user(
        context.username,
        context.password
    )

    validar_status(response, 201, "Criacao do usuario")

    dados = response.json()
    context.user_id = dados.get("userID")

    assert context.user_id, (
        "A API nao retornou o identificador do usuario."
    )

    print(f"Usuario criado: {context.username}")


@given("que eu gero um token de acesso válido")
def gerar_token(context):
    response = context.api.generate_token(
        context.username,
        context.password
    )

    validar_status(response, 200, "Geracao do token")

    dados = response.json()
    context.token = dados.get("token")

    assert context.token, (
        "A API nao retornou um token valido."
    )

    assert dados.get("status") == "Success", (
        f"Token nao autorizado: {dados}"
    )


@given("que o usuário está autorizado")
def verificar_autorizacao(context):
    response = context.api.authorize_user(
        context.username,
        context.password
    )

    validar_status(response, 200, "Autorizacao")

    assert response.json() is True, (
        "O usuario nao foi autorizado."
    )


@when("eu consulto os livros disponíveis")
def consultar_livros(context):
    response = context.api.list_books()

    validar_status(response, 200, "Consulta de livros")

    dados = response.json()
    context.livros_disponiveis = dados.get("books", [])

    assert len(context.livros_disponiveis) >= 2, (
        "A API retornou menos de dois livros."
    )


@when("seleciono dois livros diferentes")
def selecionar_livros(context):
    isbns = []

    for livro in context.livros_disponiveis:
        isbn = livro.get("isbn")

        if isbn and isbn not in isbns:
            isbns.append(isbn)

        if len(isbns) == 2:
            break

    assert len(isbns) == 2, (
        "Nao existem dois ISBNs diferentes disponiveis."
    )

    context.isbns_selecionados = isbns


@when("adiciono os dois livros à coleção do usuário")
def reservar_livros(context):
    response = context.api.reserve_books(
        context.user_id,
        context.token,
        context.isbns_selecionados
    )

    validar_status(response, 201, "Reserva de livros")


@then("a API deve retornar os dados do usuário")
def consultar_usuario(context):
    response = context.api.get_user(
        context.user_id,
        context.token
    )

    validar_status(response, 200, "Consulta do usuario")

    context.dados_usuario = response.json()

    assert context.dados_usuario.get("userId") == context.user_id, (
        "O ID retornado nao corresponde ao usuario criado."
    )


@then("os dois livros selecionados devem estar na coleção")
def validar_livros(context):
    livros = context.dados_usuario.get("books", [])

    isbns_retornados = {
        livro.get("isbn") for livro in livros
    }

    for isbn in context.isbns_selecionados:
        assert isbn in isbns_retornados, (
            f"O livro {isbn} nao foi encontrado na colecao."
        )

    print("Validacao concluida: dois livros encontrados.")
