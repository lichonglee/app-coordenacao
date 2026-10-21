/**
 * EBPÓS Coordenação — exportação de módulos para Google Calendar.
 * O cadastro pedagógico do MVP fica no navegador; o Apps Script acrescenta
 * exportação segura dos compromissos para as agendas próprias do usuário.
 */
const APP = { title: 'EBPÓS Coordenação' };

function doGet() {
  const template = HtmlService.createTemplateFromFile('Index');
  template.runtime = 'apps-script';
  return template.evaluate().setTitle(APP.title).addMetaTag('viewport', 'width=device-width, initial-scale=1');
}


function getInitialData() {
  const calendars = CalendarApp.getAllOwnedCalendars();
  const defaultCalendar = CalendarApp.getDefaultCalendar();
  if (!calendars.some(function (c) { return c.getId() === defaultCalendar.getId(); })) calendars.unshift(defaultCalendar);
  return {
    calendars: calendars.map(function (c) { return { id: c.getId(), name: c.getName() }; }),
    defaultCalendarId: defaultCalendar.getId(),
    timezone: Session.getScriptTimeZone()
  };
}

function importModules(records, calendarId) {
  if (!Array.isArray(records) || records.length > 500) throw new Error('A importação deve conter até 500 módulos.');
  const calendar = findWritableCalendar_(calendarId);
  const created = [];
  records.forEach(function (item) {
    const title = String(item.title || '').trim();
    if (!title || !/^\d{4}-\d{2}-\d{2}$/.test(item.date || '') || !/^\d{2}:\d{2}$/.test(item.startTime || '') || !/^\d{2}:\d{2}$/.test(item.endTime || '')) {
      throw new Error('Há um módulo sem título, data ou horário válido: ' + title);
    }
    const start = parseDateTime_(item.date, item.startTime);
    const end = parseDateTime_(item.date, item.endTime);
    if (end <= start) throw new Error('O horário final deve ser posterior ao inicial em ' + title + '.');
    const description = [
      'Curso: ' + String(item.course || ''),
      'Módulo: ' + String(item.module || ''),
      'Professor: ' + String(item.teacher || ''),
      item.notes ? 'Observações: ' + String(item.notes) : ''
    ].filter(Boolean).join('\n');
    const event = calendar.createEvent(title, start, end, { description: description, location: String(item.location || '') });
    created.push({ id: event.getId(), title: event.getTitle() });
  });
  return { count: created.length, events: created };
}

function findWritableCalendar_(calendarId) {
  const calendars = CalendarApp.getAllOwnedCalendars();
  const fallback = CalendarApp.getDefaultCalendar();
  if (!calendarId) return fallback;
  const calendar = calendars.find(function (c) { return c.getId() === calendarId; });
  if (!calendar && fallback.getId() === calendarId) return fallback;
  if (!calendar) throw new Error('Agenda indisponível para edição. Atualize e selecione uma agenda própria.');
  return calendar;
}

function parseDateTime_(date, time) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || !/^\d{2}:\d{2}$/.test(time)) throw new Error('Data ou horário inválido.');
  const d = date.split('-').map(Number);
  const t = time.split(':').map(Number);
  if (t[0] > 23 || t[1] > 59) throw new Error('Horário inválido.');
  return new Date(d[0], d[1] - 1, d[2], t[0], t[1], 0, 0);
}
