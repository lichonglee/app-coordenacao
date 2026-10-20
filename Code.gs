/**
 * Agenda Clara — Google Apps Script backend
 * Configure America/Sao_Paulo as the script time zone before deploying.
 */
const APP = {
  title: 'Agenda Clara',
  categories: ['Pessoal', 'Universitário', 'Profissional'],
  colors: { 'Pessoal': CalendarApp.EventColor.PALE_BLUE, 'Universitário': CalendarApp.EventColor.MAUVE, 'Profissional': CalendarApp.EventColor.PALE_GREEN }
};

function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle(APP.title)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function getInitialData() {
  const calendar = CalendarApp.getDefaultCalendar();
  const now = new Date();
  const start = new Date(now.getFullYear(), now.getMonth(), 1);
  const end = new Date(now.getFullYear(), now.getMonth() + 2, 1);
  return {
    calendarName: calendar.getName(),
    calendarUrl: 'https://calendar.google.com/calendar/u/0/r/week',
    events: readEvents_(calendar, start, end),
    timezone: Session.getScriptTimeZone()
  };
}

function getEvents(fromDate, toDate) {
  const start = parseDate_(fromDate);
  const end = parseDate_(toDate);
  if (end <= start) throw new Error('O período final deve ser posterior ao inicial.');
  return readEvents_(CalendarApp.getDefaultCalendar(), start, end);
}

function createAppointment(data) {
  validateAppointment_(data);
  const calendar = CalendarApp.getDefaultCalendar();
  const start = parseDateTime_(data.date, data.startTime);
  const end = parseDateTime_(data.date, data.endTime);
  if (end <= start) throw new Error('O horário final deve ser posterior ao inicial.');
  const title = (data.title || '').trim();
  const description = [data.description || '', 'Categoria: ' + data.category, data.reminderLabel ? 'Lembrete: ' + data.reminderLabel : ''].filter(Boolean).join('\n');
  const event = calendar.createEvent(title, start, end, { description: description, location: data.location || '' });
  event.setColor(APP.colors[data.category] || CalendarApp.EventColor.BLUE);
  const reminder = Number(data.reminderMinutes || 0);
  if (reminder > 0 && reminder <= 40320) event.addPopupReminder(reminder);
  return { id: event.getId(), title: event.getTitle(), start: event.getStartTime().toISOString(), end: event.getEndTime().toISOString(), category: data.category, description: description };
}

function createQuickReminder(data) {
  data.category = data.category || 'Profissional';
  data.reminderLabel = data.reminderLabel || 'Lembrete';
  return createAppointment(data);
}

function readEvents_(calendar, start, end) {
  return calendar.getEvents(start, end).map(function (event) {
    const description = event.getDescription() || '';
    const categoryMatch = description.match(/Categoria: (Pessoal|Universitário|Profissional)/);
    return {
      id: event.getId(), title: event.getTitle(), start: event.getStartTime().toISOString(), end: event.getEndTime().toISOString(),
      allDay: event.isAllDayEvent(), location: event.getLocation(), description: description,
      category: categoryMatch ? categoryMatch[1] : 'Profissional'
    };
  });
}

function validateAppointment_(data) {
  if (!data || !String(data.title || '').trim()) throw new Error('Informe o título do compromisso.');
  if (APP.categories.indexOf(data.category) < 0) throw new Error('Escolha uma categoria válida.');
  if (!/^\d{4}-\d{2}-\d{2}$/.test(data.date || '') || !/^\d{2}:\d{2}$/.test(data.startTime || '') || !/^\d{2}:\d{2}$/.test(data.endTime || '')) throw new Error('Informe data e horários válidos.');
}

function parseDate_(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value || '')) throw new Error('Data inválida.');
  const p = value.split('-').map(Number);
  return new Date(p[0], p[1] - 1, p[2]);
}

function parseDateTime_(date, time) {
  const d = parseDate_(date);
  const t = time.split(':').map(Number);
  if (t[0] > 23 || t[1] > 59) throw new Error('Horário inválido.');
  d.setHours(t[0], t[1], 0, 0);
  return d;
}
