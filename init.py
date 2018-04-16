import webapp2

from application.urls import *

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'B3tt1na',
}

app = webapp2.WSGIApplication(routing, config=config, debug=True)
