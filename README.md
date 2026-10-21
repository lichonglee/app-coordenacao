# EBPÓS Coordenação

Aplicativo de coordenação acadêmica derivado do `app-agenda`, com agenda por turma, módulo e professor, conciliação, painel financeiro, edição dos cadastros, mensagens e tema claro/escuro.

## Cadastro inicial

A base veio de `Coordenção_ebpos.xlsx` (Planilha1): 136 registros, 13 turmas, 18 professores e 36 módulos distintos. Foram preservados turma, professor, data, módulo, avaliação e valor. A planilha não informava horários nem duração; esses dados precisam ser preenchidos para conciliação precisa e importação direta ao Google Calendar. A Planilha2 continha valores sem rótulos suficientes e não foi importada. O conteúdo inicial está embutido no app; o arquivo XLSX não é necessário em execução.

O valor da coluna G foi tratado como pagamento por sessão, de acordo com os registros. Confirme essa interpretação antes de usar o painel em fechamento contábil.

## Funcionalidades

- Criar, atualizar, remover e filtrar sessões por turma, professor e período; exportar a agenda filtrada em PDF A4 de uma página com cabeçalho inspirado no cronograma Word e agrupamento de até três dias consecutivos por módulo, aceitando datas ISO e DD/MM/AAAA e validando viradas de mês e ano.
- Conciliação de conflitos por professor. Quando não há horários, sessões na mesma data geram alerta para revisão.
- Financeiro de valores cadastrados, status, data “Receber NF” e exportação com seleção de colunas para Excel ou PDF.
- Envio de módulos selecionados individualmente para uma agenda Google conectada, como evento de dia inteiro, com título turma - módulo - professor; valida sábado/domingo. Exportação ICS continua disponível.
- Guia de avaliação de professores: leitura de planilhas XLS/XLSX, médias gerais e por critério, comentários abertos e mini relatório exportável. A avaliação de exemplo fornecida está carregada.
- Visão geral com gráfico das médias por curso, paletas em escala escura para clara e seletor de ordenação dos módulos por sequência cronológica ou nota.
- Arquivamento e restauração de turmas, preservando os registros.
- Painel individual de professores combina as avaliações da base e pesquisas XLS/XLSX; pesquisas repetidas são identificadas e podem ser removidas.
- Cartões para lembrete individual e espelho de todos os módulos do professor. Revise e envie via WhatsApp ou e-mail.
- Atualização/importação por CSV UTF-8 e backup JSON no navegador.
- Importação direta para Calendar com Apps Script, após autorização.
- Marca EBPÓS, logo oficial e modo claro/escuro.

A exportação ICS preenche 09:00–17:00 quando a fonte não informa horários e mostra um aviso. Revise esses eventos antes de importar.

## Demonstração local

Abra `Index.html` no navegador. O app usa `localStorage` do navegador atual.

## Implantação no Google Apps Script

1. Crie projeto independente em [script.google.com](https://script.google.com/).
2. Copie `Code.gs` e crie um arquivo HTML chamado `Index`, colando o conteúdo de `Index.html`.
3. Configure `appsscript.json`, fuso `America/Sao_Paulo` e autorize Google Calendar executando `getInitialData`.
4. Implante como aplicativo da web para a conta da coordenação.

Os registros iniciais estão embutidos no template e a logo é Data URI. Os dados alterados ficam no navegador. Para uma equipe compartilhar uma única base editável, será necessário configurar um armazenamento compartilhado.