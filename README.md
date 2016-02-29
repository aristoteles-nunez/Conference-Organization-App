# Conference-Organization-App
Cloud-based API server to support a provided conference organization application using Google App Engine with Python.

# Design choices made for adding Sessions to a Conference

* The same approach used to create a new Conference was followed, so, as well as there is an attribute in Conference model
called `organizerUserId` to store the relationship with the user, in Session model there is an attribute called 
`conferenceId`, with the difference that the type used was `ndb.KeyProperty`. 
* To obtain all sessions given a conference key, inheritance was used.
* To store the speaker a String field was used, this can be improved, maybe using a new Entity, but for simplicity 
this option was used.


