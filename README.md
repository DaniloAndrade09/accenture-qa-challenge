# Accenture QA Automation Challenge

## Objetivo

Projeto de automacao de testes desenvolvido como desafio
tecnico para Quality Engineering, utilizando Python,
Selenium WebDriver, Behave e BDD.

## Tecnologias

- Python 3.12
- Selenium WebDriver
- Behave (BDD / Gherkin)
- Requests (API REST)
- Allure Report
- Git e GitHub

## Arquitetura

- `features/api/`: cenarios de testes de API
- `features/frontend/`: cenarios de interface web
- `features/steps/`: implementacao dos passos BDD
- `features/environment.py`: configuracao do navegador
- `pages/`: Page Object Model
- `clients/`: clientes para chamadas de API
- `fixtures/`: dados e arquivos de apoio
- `reports/`: relatorios e evidencias

## Cenarios automatizados

| Modulo | Validacao |
|---|---|
| BookStore API | Criacao de usuario, autenticacao e reserva de livros |
| Practice Form | Preenchimento e envio do formulario |
| Browser Windows | Abertura e fechamento de janela |
| Web Tables | Cadastro, edicao e exclusao de funcionarios |
| Progress Bar | Parada ate 25%, conclusao em 100% e reset |
| Sortable | Reordenacao de elementos com Drag and Drop |

## Instalacao

Criar o ambiente virtual:

```powershell
py -3.12 -m venv .venv
```

Ativar no PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar as dependencias:

```powershell
python -m pip install -r requirements.txt
```

## Executar os testes

Suite principal:

```powershell
python -m behave features --tags="not bonus"
```

Somente API:

```powershell
python -m behave features/api
```

Somente frontend:

```powershell
python -m behave features/frontend --tags="not bonus"
```

## Relatorio Allure

Gerar os resultados:

```powershell
python -m behave features --tags="not bonus" -f allure_behave.formatter:AllureFormatter -o reports/allure-results
```

Visualizar:

```powershell
allure serve reports/allure-results
```

O Allure CLI deve estar instalado separadamente.

## Resultados da execucao validada

- 6 features aprovadas
- 6 cenarios aprovados
- 36 steps aprovados
- 0 falhas
- 1 cenario bonus excluido

Esses resultados correspondem a uma execucao validada
da suite principal, nao a uma garantia de ausencia
de falhas em execucoes futuras.

## Defeito identificado

O cenario bonus de Web Tables apresentou comportamento
inesperado: apos cadastrar 12 funcionarios, a exclusao
de um registro fez os demais registros criados
desaparecerem da tabela.

O comportamento foi documentado em:

`reports/BUG-WEBTABLES-001.md`

A causa interna da aplicacao nao foi determinada.

## Observacoes

Os testes utilizam a aplicacao publica DemoQA.
A disponibilidade do ambiente e o comportamento
do navegador podem influenciar as execucoes.
