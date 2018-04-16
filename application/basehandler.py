import datetime
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'application'))

import jinja2
import webapp2

from google.appengine.api import users
from application.models import *

def overdue_check(value):
	return value < datetime.date.today()

def check_hw_state(reservations):
    if reservations:
        for r in reservations:
            reservation = reservation_by_id(r.integer_id())
            if reservation.state == 2 and reservation.until > datetime.date.today():
                return 1
            elif reservation.state == 2 and reservation.until <= datetime.date.today():
                return 2
    else:
        return 0

    return 0

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
jinja_environment.filters['overdue'] = overdue_check
jinja_environment.filters['chckhwstt'] = check_hw_state

from webapp2_extras import sessions

""" BASIC FUNCTIONS """

def redirect_if_not_admin(self):
	if not self.session[ 'admin' ]:
		self.redirect('/')

def redirect_if_not_logged(self):
	if not self.session[ 'logged' ]:
		self.redirect('/')

def user_by_id(id):
	return UserData.get_by_id(id)

def reservation_by_id(id):
	return Reservation.get_by_id(id)

def hardware_by_id(id):
	return Hardware.get_by_id(id)

def render(template, template_values, self):
	template = jinja_environment.get_template(template)
	self.response.out.write( template.render(template_values))

def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days) + 1):
		yield start_date + datetime.timedelta(n)

def filter_reservations_by_dates(between, until, reservations = Reservation.query()):
	found = []

	for reservation in reservations:
		if reservation.between >= between and reservation.until <= until:
		# if reservation.between < until and reservation.until > between:
			found.append(reservation)

	return found

def convert_to_single_date(reservations):
	dates = []

	for reservation in reservations:
		if reservation.state > 0:
			for single_date in daterange(reservation.between, reservation.until):
				dates.append(single_date)

	return dates

def getOverDue():
	return Reservation.query().filter( Reservation.until <= datetime.datetime.now())

def get_wishes():
	return Reservation.query().filter(Reservation.state == 0)

def get_overdue():
	return Reservation.query().filter(
					Reservation.until <= datetime.datetime.now(),
					Reservation.state == 2
				 )

def get_overdue_and_inactive():
	return Reservation.query().filter(
					Reservation.until <= datetime.datetime.now(),
					Reservation.state == 1
				 )

def get_overdue_and_inactive_older_then(days):
	return Reservation.query().filter(
					Reservation.until <= datetime.datetime.now()-datetime.timedelta(days=days),
					Reservation.state == 1
				 )

def get_over_due_and_active():
	return Reservation.query().filter( Reservation.until <= datetime.datetime.now())

def get_by_user(user):
	return Reservation.query().filter( Reservation.user == user.key)

def get_overdue_by_user(user):
	return Reservation.query().filter( Reservation.user == user.key, Reservation.until < datetime.datetime.now())

def get_overdue_and_active_by_user(user):
	return Reservation.query().filter(
					Reservation.user == user.key,
					Reservation.until < datetime.datetime.now(),
					Reservation.state == 2
				 )


def get_not_overdue_by_user(user):
	return Reservation.query().filter( Reservation.user == user.key, Reservation.until >= datetime.datetime.now())

""" BASEHANDLER """


class BaseHandler(webapp2.RequestHandler):
	def dispatch(self):
		# Get a session store for this request.
		self.session_store = sessions.get_store(request=self.request)

		try:
			# Dispatch the request.
			webapp2.RequestHandler.dispatch(self)
		finally:
			# Save all sessions.
			self.session_store.save_sessions(self.response)

	@webapp2.cached_property
	def session(self):
		# Returns a session using the default cookie key.
		return self.session_store.get_session()
