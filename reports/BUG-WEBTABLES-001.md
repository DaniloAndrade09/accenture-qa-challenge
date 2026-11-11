# BUG-WEBTABLES-001

## Titulo
Registros cadastrados desaparecem apos uma unica exclusao

## Ambiente
- Aplicacao: https://demoqa.com/webtables
- Automacao: Python, Selenium e Behave
- Cenario: cadastro e exclusao de 12 funcionarios

## Passos para reproduzir
1. Acessar Web Tables.
2. Configurar exibicao de 20 registros.
3. Cadastrar 12 funcionarios com e-mails diferentes.
4. Confirmar que os 12 registros estao presentes.
5. Excluir apenas um dos funcionarios.
6. Verificar os registros restantes.

## Resultado esperado
Apenas o funcionario selecionado deve ser excluido.
Os outros 11 devem permanecer na tabela.

## Resultado observado
Apos a primeira exclusao, todos os 12 registros
criados pelo teste desaparecem da tabela.
Permanecem apenas os tres registros originais.

## Evidencias
- 12 cadastros validados antes da exclusao.
- IDs de exclusao distintos: delete-record-4 a delete-record-15.
- Nenhum ID duplicado identificado.
- Apos a exclusao, apenas tres registros originais visiveis.
- Paginacao permaneceu configurada para 20 registros.
- Capturas em reports/diagnostico_webtables/.

## Status
Falha reproduzida pela automacao.
Causa interna da aplicacao ainda nao determinada.

## Impacto
O cenario bonus nao pode ser aprovado sem
validar corretamente a exclusao individual.
