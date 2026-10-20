# Agenda Clara

Agenda pessoal responsiva para celular e computador, integrada à agenda padrão do Google Calendar por Google Apps Script.

## O que está incluído

- Cadastro de compromissos pessoais, universitários e profissionais.
- Prévia automática dos compromissos já existentes na data escolhida no formulário.
- A página abre com Consulta rápida visível, intervalo do dia atual até dois meses à frente e resultados carregados automaticamente.
- Opção de criar compromissos de dia inteiro.
- Escolha da agenda Google própria em que cada compromisso será criado.
- Lembretes rápidos como preparar apresentação, subir conteúdo e avaliar a turma.
- Alertas pop-up criados no próprio evento do Google Calendar.
- Consulta rápida de horários vagos por um ou vários meses (até 12), das 9h às 17h ou em dias inteiros. Quando fins de semana estão marcados, a consulta mostra somente blocos de sexta a domingo como dia inteiro; qualquer compromisso nesses dias marca o bloco em vermelho com observações.
- Texto para WhatsApp com os fins de semana livres agrupados por mês, sem horários; é possível marcar uma opção para incluir também os fins de semana ocupados no mesmo formato.
- Cartão Conciliação identifica sobreposições de horários em agendas distintas, com nome e cor de cada agenda.
- Relatórios mensais ou por intervalo, com impressão/salvamento em PDF pelo navegador.
- Layout responsivo para celular e web.
- Tema escuro e controles para ocultar ou restaurar cartões; os cartões restantes se reorganizam automaticamente.
- A consulta de disponibilidade identifica cada conflito com o nome da agenda e uma cor própria.
- Na Consulta rápida, é possível selecionar uma ou várias agendas e combinar seus conflitos.
- Agenda próxima aparece primeiro e a grade ajusta a largura quando uma coluna fica sem cartões visíveis.
- Demonstração local sem conexão à conta Google.
- Identificação da versão (`v2.7`) e data atual (DD/MM/AAAA) ao lado do nome do app.

## Apps Script é uma boa opção?

Sim, para uma aplicação individual como esta. O Apps Script hospeda a interface web e, depois da autorização do titular da conta, acessa o calendário padrão sem manter uma senha ou token em um servidor de terceiros. O projeto pode ser usado sem custo em contas Google comuns, respeitando as cotas aplicáveis do Google. Alertas configurados aqui são lembretes pop-up do próprio Calendar; a entrega de notificações no celular depende das configurações do Google Calendar no aparelho.

## Implantação na sua conta Google

1. Acesse [script.google.com](https://script.google.com/) e crie um projeto independente.
2. Nas configurações do projeto, defina o fuso horário como **America/Sao_Paulo**.
3. No editor, substitua o conteúdo de `Code.gs` pelo arquivo homônimo deste repositório. Crie um arquivo HTML chamado `Index` e cole nele o conteúdo de `Index.html`.
4. Em **Configurações do projeto**, habilite a exibição do arquivo de manifesto `appsscript.json` e substitua pelo manifesto deste repositório (ou configure o mesmo fuso horário e escopo `https://www.googleapis.com/auth/calendar`).
5. Selecione `getInitialData` no editor e execute uma vez. Revise e conceda o acesso solicitado ao seu Google Calendar.
6. Clique em **Implantar → Nova implantação → Aplicativo da Web**. Selecione **Executar como: eu** e limite o acesso a **Somente eu** para uso pessoal. Implante e abra a URL gerada.
7. No celular, abra essa URL no navegador e adicione à tela inicial para acesso rápido.

O Google entrega o app hospedado em seus próprios domínios. Para uso pessoal, mantenha o acesso restrito à sua conta e não compartilhe a URL de implantação.

## Demonstração local

Abra `Index.html` no navegador. A demonstração usa exemplos e guarda os novos itens localmente no navegador, sem acessar nem alterar sua conta Google. O botão Google Calendar apenas abre o calendário.

## Limites da consulta de disponibilidade

A busca considera das 9h às 17h ou o dia inteiro, conforme a opção marcada, e os eventos que ocupam horário nas agendas próprias da conta. Selecione os meses inicial e final, em um intervalo de até 12 meses. As setas deslocam o período completo em um mês. Marcar **Fins de semana** consulta sábado e domingo como dias inteiros; se houver compromisso, o dia aparece em vermelho com o título e horário em uma observação. O texto copiado informa apenas os horários livres; não envia mensagens ao WhatsApp. Agendas compartilhadas de outras pessoas não entram na consulta. Confira feriados e exceções antes de confirmar um horário.

## Arquivos

- `Code.gs` — conexão segura com CalendarApp e operações de agenda.
- `Index.html` — interface responsiva e demonstração local.
- `appsscript.json` — fuso horário e permissões solicitadas.
