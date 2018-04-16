from application.basehandler import *
import csv

""" INDEX / DASHBOARD """


class Index( BaseHandler ):
	def get(self):
		if users.get_current_user():

			user = UserData.query().filter( UserData.nickname == users.get_current_user().nickname() ).get()

			if not user:
				UserData( 
					user          = users.get_current_user(),
					nickname      = users.get_current_user().nickname(),
					firstname     = users.get_current_user().nickname().split('.')[0].capitalize(),
					lastname      = users.get_current_user().nickname().split('.')[1].capitalize(),
					admin         = False,
					locked        = False ).put()

				self.session[ 'admin' ]  = False
			else:
				self.session[ 'admin' ]  = user.admin

				if not user.firstname:
					user.firstname = user.nickname.split('.')[0].capitalize()
					user.lastname = user.nickname.split('.')[1].capitalize()
					user.put()
			
			self.session[ 'logged' ] = True
			self.session[ 'url' ]    = users.create_logout_url(self.request.uri)
			self.session[ 'logger' ] = 'Logout'

			variables = {
				'title': 'HyperWerk Verleih',
				'message': 'Willkommen. Dein HyperWerk Account berechtigt dich zum Zugang.</br></br>Regeln fuer Reservationen und Ausleihe werden durch dieses Dokument beschrieben. Ausleihende erklaeren sich durch den Gebrauch mit diesem einverstanden.',
				'session': self.session,
				'nav_dashboard': True
			}

			if user:
				if user.locked:
					self.session[ 'logged' ] = False
					self.session[ 'admin' ]  = False
					self.session[ 'url' ]    = users.create_login_url(self.request.uri)
					self.session[ 'logger' ] = 'Login'

					self.redirect(users.create_logout_url('/locked')) 
					return
				else:
					self.redirect('/dashboard')
			else:
					template = 'index/message.html'
					variables['title'] = 'Hallo Fremder'
					variables['message'] = 'Logge dich ein.'

					render(template, variables, self)

					return
		else:
			self.session[ 'logged' ] = False
			self.session[ 'admin' ]  = False
			self.session[ 'url' ]    = users.create_login_url(self.request.uri)
			self.session[ 'logger' ] = 'Login'


			template = 'index/message.html'
			variables = {
				'title': 'Willkommen',
				'message': 'Dein HyperWerk Account berechtigt dich zum Zugang. Regeln fuer Reservationen und Ausleihe werden durch <a href="https://sites.google.com/a/hyperwerk.ch/take5/intressource/verleih/regel">dieses Dokument</a> beschrieben. Ausleihende erklaeren sich durch den Gebrauch mit diesem einverstanden.',
				'session': self.session,
				'nav_dashboard': True
			}

			render(template, variables, self)

class Dashboard( BaseHandler ):
	def get(self):
		redirect_if_not_logged(self)

		template_values = {}
		user = UserData.query().filter( UserData.user == users.get_current_user() ).get()

		if self.session[ 'admin' ]:
			query = Reservation.query().filter(Reservation.until < datetime.datetime.now()).fetch(100)
			overdone = []

			for o in query:
				if o.state > 1:
					overdone.append(o)

			template_values = {
				'title'	      : 'Dashboard',
				'session'     : self.session,
				'wishes'      : get_wishes().fetch(),
				'overdone'    : get_overdue().fetch(),
				'user'        : user,
				'nav_dashboard': True

			}
		else:
			template_values = {
				'title'       : 'Dashboard',
				'session'     : self.session,
				'reservations': get_not_overdue_by_user(user).fetch(),
				'overdone'    : get_overdue_and_active_by_user(user).fetch(),
				'user'        : user,
				'nav_dashboard': True
			}

		render( 'index/dashboard.html', template_values, self)

class Locked( BaseHandler ):
	def get(self):
		template = 'index/message.html'
		
		variables = {
			'title': 'HyperWerk Verleih',
			'message': 'Du wurdest gesperrt. Melde dich beim Verleihteam.',
			'session': self.session,
		}

		render(template, variables, self)

class Numbers( BaseHandler ):
	def get(self, min, max):
		redirect_if_not_admin(self)
		template = 'index/numbers.html'

		existing = []
		nonexisting = []

		for i in range(int(min), int(max)):
			if Hardware.query(Hardware.inventory_number == i).get():
				existing.append(i)
			else:
				nonexisting.append(i)

		variables = {
			'title': 'Inventarnummern',
			'existing': existing,
			'nonexisting': nonexisting,
			'session': self.session,
			'nav_admin': True
		}

		render(template, variables, self)
