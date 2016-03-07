# Conference-Organization-App
Cloud-based API server to support a provided conference organization application using Google App Engine with Python.


App Engine application for the Udacity training course.

## Design choices made for adding Sessions to a Conference

* The same approach used to create a new Conference was followed, so, as well as there is an attribute in Conference model
called `organizerUserId` to store the relationship with the user, in Session model there is an attribute called 
`conferenceId`, with the difference that the type used was `ndb.KeyProperty`. 
* To obtain all sessions given a conference key, inheritance was used.
* To store the speaker a String field was used, this can be improved, maybe using a new Entity, but for simplicity 
this option was used.

## Indexes and queries
In this part, indexes and querys for sessions where added:

* Endpoint to filter sessions by highlights (`getConferenceSessionsByHighlight`).
* Endpoint to filter sessions by date (`getConferenceSessionsByDate`). The result contains all the records with 
the date greater (or equal) than the one specified.
* The `index.yaml` file was updated automatically updated whenever the dev_appserver detects that a new type of 
query is run.

## Query related problem
> Let’s say that you don't like workshops and you don't like sessions after 7 pm. How would you handle a query 
  for all non-workshop sessions before 7 pm? What is the problem for implementing this query? What ways to 
  solve it did you think of?
    
In this case the first try was:

```
sevenPm = datetime.strptime("19:00", '%H:%M').time()
sessions = Session.query(ancestor=conf)
sessions = sessions.filter(Session.typeOfSession != "Workshop")
sessions = sessions.filter(Session.startTime < sevenPm)
```

But it throws the following Exception:

```
Encountered unexpected error from ProtoRPC method implementation: BadRequestError (Only one inequality filter per 
query is supported. Encountered both typeOfSession and startTime)
```

To solve the problem, I leave only one inequality filter and iterate over the results to detect every session under 
seven pm.

```
sevenPm = datetime.strptime("19:00", '%H:%M').time()
sessions = Session.query(ancestor=conf)
sessions = sessions.filter(Session.typeOfSession != "Workshop")
return SessionForms(items=[self._copySessionToForm(session) for session in sessions
                           if session.startTime < sevenPm])
```

## Products
- [App Engine][1]

## Language
- [Python][2]

## APIs
- [Google Cloud Endpoints][3]

## Setup Instructions
1. Update the value of `application` in `app.yaml` to the app ID you
   have registered in the App Engine admin console and would like to use to host
   your instance of this sample.
1. Update the values at the top of `settings.py` to
   reflect the respective client IDs you have registered in the
   [Developer Console][4].
1. Update the value of CLIENT_ID in `static/js/app.js` to the Web client ID
1. (Optional) Mark the configuration files as unchanged as follows:
   `$ git update-index --assume-unchanged app.yaml settings.py static/js/app.js`
1. Run the app with the devserver using `dev_appserver.py DIR`, and ensure it's running by visiting your local server's address (by default [localhost:8080][5].)
1. (Optional) Generate your client library(ies) with [the endpoints tool][6].
1. Deploy your application.


[1]: https://developers.google.com/appengine
[2]: http://python.org
[3]: https://developers.google.com/appengine/docs/python/endpoints/
[4]: https://console.developers.google.com/
[5]: https://localhost:8080/
[6]: https://developers.google.com/appengine/docs/python/endpoints/endpoints_tool