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
  const template = HtmlService.createTemplateFromFile('Index');
  template.runtime = 'apps-script';
  return template.evaluate()
    .setTitle(APP.title)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function getInitialData() {
  const calendars = getWritableCalendars_();
  const now = new Date();
  const start = new Date(now.getFullYear(), now.getMonth(), 1);
  const end = new Date(now.getFullYear(), now.getMonth() + 2, 1);
  const calendarList = calendars.map(function (calendar) { return { id: calendar.getId(), name: calendar.getName() }; });
  const calendarId = CalendarApp.getDefaultCalendar().getId();
  return {
    calendarName: CalendarApp.getDefaultCalendar().getName(),
    defaultCalendarId: calendarId,
    calendars: calendarList,
    calendarUrl: 'https://calendar.google.com/calendar/u/0/r/week',
    events: readEvents_(calendars, start, end),
    timezone: Session.getScriptTimeZone()
  };
}

function getEvents(fromDate, toDate) {
  const start = parseDate_(fromDate);
  const end = parseDate_(toDate);
  if (end <= start) throw new Error('O período final deve ser posterior ao inicial.');
  return readEvents_(getWritableCalendars_(), start, end);
}

function createAppointment(data) {
  validateAppointment_(data);
  const calendar = findWritableCalendar_(data.calendarId);
  const isAllDay = data.allDay === 'on' || data.allDay === true;
  const start = isAllDay ? parseDate_(data.date) : parseDateTime_(data.date, data.startTime);
  let end;
  if (isAllDay) {
    start.setHours(0, 0, 0, 0);
    end = new Date(start);
    end.setDate(end.getDate() + 1);
  } else {
    end = parseDateTime_(data.date, data.endTime);
    if (end <= start) throw new Error('O horário final deve ser posterior ao inicial.');
  }
  const title = (data.title || '').trim();
  const description = [data.description || '', 'Categoria: ' + data.category, data.reminderLabel ? 'Lembrete: ' + data.reminderLabel : ''].filter(Boolean).join('\n');
  const options = { description: description, location: data.location || '' };
  const event = isAllDay ? calendar.createAllDayEvent(title, start, options) : calendar.createEvent(title, start, end, options);
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

function readEvents_(calendars, start, end) {
  return calendars.reduce(function (all, calendar) {
    return all.concat(calendar.getEvents(start, end).map(function (event) {
    const description = event.getDescription() || '';
    const categoryMatch = description.match(/Categoria: (Pessoal|Universitário|Profissional)/);
    return {
      id: event.getId(), title: event.getTitle(), start: event.getStartTime().toISOString(), end: event.getEndTime().toISOString(),
      allDay: event.isAllDayEvent(), location: event.getLocation(), description: description,
      category: categoryMatch ? categoryMatch[1] : 'Profissional', calendarId: calendar.getId(), calendarName: calendar.getName()
    };
    }));
  }, []).sort(function (a, b) { return new Date(a.start) - new Date(b.start); });
}

function getWritableCalendars_() {
  const calendars = CalendarApp.getAllOwnedCalendars();
  const defaultCalendar = CalendarApp.getDefaultCalendar();
  if (!calendars.some(function (calendar) { return calendar.getId() === defaultCalendar.getId(); })) calendars.unshift(defaultCalendar);
  return calendars;
}

function findWritableCalendar_(calendarId) {
  const calendars = getWritableCalendars_();
  if (!calendarId) return CalendarApp.getDefaultCalendar();
  const calendar = calendars.find(function (item) { return item.getId() === calendarId; });
  if (!calendar) throw new Error('A agenda selecionada não está disponível para edição. Atualize a página e escolha uma agenda sua.');
  return calendar;
}

function validateAppointment_(data) {
  if (!data || !String(data.title || '').trim()) throw new Error('Informe o título do compromisso.');
  if (APP.categories.indexOf(data.category) < 0) throw new Error('Escolha uma categoria válida.');
  if (data.calendarId && typeof data.calendarId !== 'string') throw new Error('Agenda inválida.');
  if (!/^\d{4}-\d{2}-\d{2}$/.test(data.date || '')) throw new Error('Informe uma data válida.');
  if (data.allDay !== 'on' && data.allDay !== true && (!/^\d{2}:\d{2}$/.test(data.startTime || '') || !/^\d{2}:\d{2}$/.test(data.endTime || ''))) throw new Error('Informe horários válidos.');
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
