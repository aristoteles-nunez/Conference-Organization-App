#!/usr/bin/env python
import webapp2
from google.appengine.api import app_identity
from google.appengine.api import mail
from google.appengine.ext import ndb
from google.appengine.api import memcache
from conference import ConferenceApi
from models import Session

MEMCACHE_FEATURED_SPEAKER_KEY = "FEATURED_SPEAKER"




class SetAnnouncementHandler(webapp2.RequestHandler):
    def get(self):
        """Set Announcement in Memcache."""
        # TODO 1
        # use _cacheAnnouncement() to set announcement in Memcache
        ConferenceApi._cacheAnnouncement()
        self.response.set_status(204)


class SendConfirmationEmailHandler(webapp2.RequestHandler):
    def post(self):
        """Send email confirming Conference creation."""
        mail.send_mail(
            'noreply@%s.appspotmail.com' % (
                app_identity.get_application_id()),     # from
            self.request.get('email'),                  # to
            'You created a new Conference!',            # subj
            'Hi, you have created a following '         # body
            'conference:\r\n\r\n%s' % self.request.get(
                'conferenceInfo')
        )


class FeaturedSpeakerHandler(webapp2.RequestHandler):
    def post(self):
        """ Features the speaker and session names."""
        print("Executing Handler for featured speaker")
        speakerName = self.request.get('speaker')
        conferenceName = self.request.get('conferenceName')
        conferenceKey = self.request.get('conferenceKey')
        conf = ndb.Key(urlsafe=conferenceKey)
        sessions = Session.query(ancestor=conf).filter(Session.speaker == speakerName)
        print(sessions)
        if sessions.count() > 1:
            print("Inserting on cache...")
            displayedMessage = "{0} is the featured speaker in {1} " \
                               "conference performing in the sessions: " \
                               " {2}".format(speakerName,
                                             conferenceName,
                                             ",".join([str(session.name) for session in sessions]))
            memcache.set(MEMCACHE_FEATURED_SPEAKER_KEY, displayedMessage)



app = webapp2.WSGIApplication([
    ('/crons/set_announcement', SetAnnouncementHandler),
    ('/tasks/send_confirmation_email', SendConfirmationEmailHandler),
    ('/tasks/featured_speaker', FeaturedSpeakerHandler),
], debug=True)