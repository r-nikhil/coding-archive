var google = require('googleapis-plus');

var REDIRECT_URL = "http://localhost"
var event = {
  'summary': 'Google I/O 2015',
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2015-05-28T09:00:00-07:00', //ISOString
    'timeZone': 'America/Los_Angeles'
  },
  'end': {
    'dateTime': '2015-05-28T17:00:00-07:00',
    'timeZone': 'America/Los_Angeles'
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2' //Refer recurrence rule to know more
  ],
  'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'}
  ],
  'reminders': {
    'useDefault': false,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10}
    ]
  }
};
var OAuth2Client = google.OAuth2Client;
var auth = new OAuth2Client(CLIENT_ID, CLIENT_SECRET, REDIRECT_URL);
auth.getToken(code, function (err, tokens) {
  oauth2Client.setCredentials(tokens);
});

auth.setCredentials({access_token: tokens.access_token, refresh_token: tokens.refresh_token});

var object = {
  auth: auth,
  calendarId: 'primary',
  resource: event
}
googleplus.discover('calendar', 'v3').execute(function (err, client) {
//get the google calendar api
  if (err) {
    console.log('Err', err);
    return;
  }
//using the client access the calendar event and insert
  client.calendar.events.create(object).withAuthClient(auth).execute(callback);
});
var object = {
  auth: auth,
  calendarId: 'primary',
  eventId : id,
  resource: event
};
googleplus.discover('calendar', 'v3').execute(function (err, client) {
  if (err) {
    console.log('Err', err);
    return;
  }
  client.calendar.events.update(object).withAuthClient(auth).execute(callback);
});
