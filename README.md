# Agenda Clara

Agenda pessoal responsiva para celular e computador, integrada à agenda padrão do Google Calendar por Google Apps Script.

## O que está incluído

- Cadastro de compromissos pessoais, universitários e profissionais.
- Lembretes rápidos como preparar apresentação, subir conteúdo e avaliar a turma.
- Alertas pop-up criados no próprio evento do Google Calendar.
- Consulta rápida de horários vagos em dias úteis, das 9h às 17h, considerando compromissos existentes.
- Texto de disponibilidade para copiar e colar no WhatsApp.
- Relatórios mensais ou por intervalo, com impressão/salvamento em PDF pelo navegador.
- Layout responsivo para celular e web.
- Demonstração local sem conexão à conta Google.

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

A busca considera segunda a sexta, das 9h às 17h, e os eventos que ocupam horário no calendário padrão. O texto copiado informa os intervalos sugeridos; não envia mensagens ao WhatsApp. Confira feriados, outros calendários e exceções antes de confirmar um horário.

## Arquivos

- `Code.gs` — conexão segura com CalendarApp e operações de agenda.
- `Index.html` — interface responsiva e demonstração local.
- `appsscript.json` — fuso horário e permissões solicitadas.
