from application.basehandler import *
import difflib
import logging

""" RESERVATION """

class Handling( BaseHandler ):
	def get(self, action, data):
		redirect_if_not_logged(self)

		template = ''
		variables = {
			'session': self.session,
			'nav_admin': True
		}

		if data and action != 'create':
			reservation = Reservation().get_by_id( int( data ) )

		if action == 'all':
			template = 'reservation/all.html'
			variables['title'] = 'Alle Reservationen',
			variables['reservations'] = Reservation.query()

		if action == 'view':
			template = 'reservation/one.html'
			variables['title'] = 'Reservation ansehen'
			variables['reservation'] = reservation
			variables['user'] = reservation.user
			variables['item'] = reservation.item

		if action == 'search':
			template = 'reservation/search.html'
			variables['title'] = 'Reservation suchen'
			variables['users'] = UserData.query()
			variables['hide_options'] = 'false'

		if action == 'create':
			template = 'reservation/create_edit.html'

			hw = hardware_by_id(int(data))
			reservations = ndb.get_multi( hw.reservations )

			variables['title'] = 'Reservation taetigen'
			variables['reservation'] = None
			variables['reservations'] = reservations
			variables['dates'] = convert_to_single_date(reservations)
			variables['users'] = UserData.query()
			variables['myself'] = UserData.query().filter( UserData.nickname == users.get_current_user().nickname() ).get()
			variables['item'] = hw

		if action == 'edit':
			template = 'reservation/create_edit.html'

			hw = hardware_by_id(reservation.item.integer_id())
			reservations = ndb.get_multi( hw.reservations )

			variables['title'] = 'Reservation editieren'
			variables['reservation'] = reservation
			variables['between'] = reservation.between
			variables['until'] = reservation.until
			variables['reservations'] = reservations
			variables['dates'] = convert_to_single_date(reservations)
			variables['users'] = UserData.query()
			variables['myself'] = UserData.query().filter( UserData.nickname == users.get_current_user().nickname() ).get()
			variables['item'] = hw

		if action == 'delete':
			item = Hardware.get_by_id( reservation.item.integer_id() )

			try:
				item.reservations.remove( reservation.key )
				item.put()
			except:
				pass

			try:
				reservation.key.delete()
			except:
				pass

			self.redirect('/hardware/view/'+str(item.key.integer_id()))
			return

		if action == 'setstate':
			reservation.state = int(self.request.get('state'))
			reservation.put()

			self.redirect(self.request.referer)
			return

		if action == 'old':
			if not self.request.get('days'):
				data = 20
			else:
				data = int(self.request.get('days'))

			template = 'reservation/delold.html'
			variables['days'] = data
			variables['title'] = 'Alte Reservationen l&ouml;schen'
			variables['reservations'] = get_overdue_and_inactive_older_then(data).fetch()

		if action == 'delete-old':
			if not self.request.get('days'):
				data = 20
			else:
				data = int(self.request.get('days'))
				
			for reservation in get_overdue_and_inactive_older_then(data).fetch():
				item = Hardware.get_by_id( reservation.item.integer_id() )

				try:
					item.reservations.remove( reservation.key )
					item.put()
				except:
					pass

				try:
					reservation.key.delete()
				except:
					pass

				template = 'index/message.html'
				variables['title'] = 'Alte Reservationen no more'
				variables['message'] = 'Alle alten Reservationen wurden gel&ouml;scht.'

		render(template, variables, self)

	def post(self, action, data):
		redirect_if_not_logged(self)

		template = ''
		variables = {
			'session': self.session,
			'nav_admin': True
		}

		if data and action != 'create':
			reservation = Reservation().get_by_id( int( data ) )

		if action == 'create':
			item = Hardware.get_by_id( int( data ) )
			user = UserData.query().filter( UserData.nickname == self.request.get('nickname')).get()
			state = 0

			if self.session[ 'admin' ]:
				state = 1

			reservation = Reservation(	between = datetime.datetime.strptime(self.request.get('between'), '%d.%m.%Y' ).date(),
							until = datetime.datetime.strptime(self.request.get('until'), '%d.%m.%Y' ).date(),
							why = self.request.get('why'),
							user = user.key,
							item = item.key,
							state = state)
			reservation.put()

			item.reservations.append( reservation.key )
			item.put()

			if self.session[ 'admin' ]:
				self.redirect('/reservation/edit/' + str(reservation.key.integer_id()))
				return
			else:
				template = 'index/message.html'
				variables['title'] = 'Reservation hinzufuegen'
				variables['message'] = 'Reservationswunsch gesendet.'

		if action == 'edit':
			item = Hardware.get_by_id( reservation.item.id() )
			user = UserData.query().filter( UserData.nickname == self.request.get('nickname')).get()

			reservation.between = datetime.datetime.strptime(self.request.get('between'), '%d.%m.%Y' ).date()
			reservation.until = datetime.datetime.strptime(self.request.get('until'), '%d.%m.%Y' ).date()
			reservation.why = self.request.get('why')
			reservation.user = user.key

			if self.request.get('active'):
				reservation.active = True

			if self.request.get('archive'):
				reservation.active = False
				reservation.archive = True

				item.reservations.remove( reservation.key() )
				item.put()

			reservation.put()
			
			self.redirect('/reservation/edit/' + str(reservation.key.integer_id()))
			return

		if action == 'search':
			between = datetime.datetime.strptime('29.8.1981', '%d.%m.%Y' ).date()
			until = datetime.datetime.strptime('1.1.2100', '%d.%m.%Y' ).date()

			if self.request.get('between'):
				between = datetime.datetime.strptime(self.request.get('between'), '%d.%m.%Y' ).date()
			if self.request.get('until'):
				until = datetime.datetime.strptime(self.request.get('until'), '%d.%m.%Y' ).date()
			
			found_temp = []
			found = []

			if self.request.get('user'):
				user = user_by_id(int(self.request.get('user')))
				reservations = Reservation.query().filter(Reservation.user == user.key)
			else:
				reservations = Reservation.query()

			if self.request.get('why'):
				search_string = self.request.get('why')
				for reservation in reservations:
					if reservation.why.lower().find(search_string.lower()) > -1:
						found_temp.append(reservation)
			else:
				found_temp = reservations

			if self.request.get('active'):
				for f in found_temp:
					if f.state == 2:
						found.append(f)
			else:
				found = found_temp

			template = 'reservation/search.html'
			variables['title'] = 'Reservation gefunden'
			variables['users'] = UserData.query()
			variables['between'] = self.request.get('between')
			variables['until'] = self.request.get('until')
			variables['active'] = self.request.get('active')
			variables['found'] = filter_reservations_by_dates(between, until, found)
			variables['hide_options'] = 'true'

		render(template, variables, self)
