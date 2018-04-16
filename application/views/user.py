from application.basehandler import *


""" USERS """

class Handling( BaseHandler ):
	def get(self, action, data):
		redirect_if_not_logged(self)

		template = ''
		variables = {
			'session': self.session,
			'nav_admin': True
		}

		if data:
			user = UserData.get_by_id( int( data ) )
			variables['user'] = user

		if action == 'all':
			template = 'user/all.html'
			variables['title'] = 'Alle Benutzer'
			variables['users'] = UserData.query()

		if action == 'view':
			template = 'user/one.html'
			variables['title'] = 'Benutzer editieren'
			variables['reservations'] = get_by_user(user).fetch()
			variables['overdone'] = get_overdue_and_active_by_user(user).fetch()
			variables['admin'] = self.session['admin']

		if action == 'create':
			template = 'user/create_edit.html'
			variables['user'] = None
			variables['admin'] = self.session['admin']
		
		if action == 'edit':
			template = 'user/create_edit.html'
			variables['reservations'] = get_by_user(user).fetch()
			variables['overdone'] = get_overdue_and_active_by_user(user).fetch()
			variables['admin'] = self.session['admin']

		if action == 'toggleadmin':
			if(user.admin):
				user.admin = False
			else:
				user.admin = True

			user.put()
			self.redirect(self.request.referer)

			return

		if action == 'togglelock':
			if(user.locked):
				user.locked = False
			else:
				user.locked = True

			user.put()
			self.redirect(self.request.referer)

			return

		render(template, variables, self)

	def post(self, action, data):
		redirect_if_not_logged(self)

		template = ''
		variables = {
			'session': self.session,
			'nav_admin': True
		}

		if data:
			user = UserData().get_by_id( int( data ) )

		if action == 'create':
			user = UserData()
			
		if action == 'create' or action == 'edit':
			user.firstname = self.request.get('firstname')
			user.lastname = self.request.get('lastname')
			user.nickname = user.firstname.lower() + '.' + user.lastname.lower()
			user.admin = bool( self.request.get('admin') )
			user.locked = bool( self.request.get('locked') )

			user.put()

			self.redirect('/users/view/' + str(user.key.integer_id()))

			return

