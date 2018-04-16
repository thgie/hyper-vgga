from application.basehandler import *
import difflib
import logging


""" HARDWARE """

class Handling( BaseHandler ):
	def get(self, action, data):
		redirect_if_not_logged(self)

		template = ''
		variables = {
			'session': self.session,
			'nav_hardware': True
		}

		if data:
			hw = Hardware().get_by_id( int( data ) )

		if action == 'all':
			template = 'hardware/all.html'
			variables['title'] = 'Hardware',
			variables['hws'] = Hardware.query()

		if action == 'view':
			template = 'hardware/one.html'
			variables['title'] = 'Hardware: ' + hw.title
			variables['hw'] = hw
			variables['reservations'] = ndb.get_multi(hw.reservations)

		if action == 'search':
			template = 'hardware/search.html'
			variables['title'] = 'Hardware suchen'
			variables['labels'] = Label.query()
			variables['hide_options'] = 'false'

		if action == 'create':
			template = 'hardware/create_edit.html'
			variables['title'] = 'Hardware hinzufuegen'
			variables['labels'] = Label.query()
			variables['hw'] = None

		if action == 'edit':
			template = 'hardware/create_edit.html'
			variables['title'] = hw.title + ' editieren'
			variables['labels'] = Label.query()
			variables['stichworte'] = Label.query(Label.category == 'Stichwort').get()
			categories = Label.query(Label.category == 'Kategorie').get()
			locations = Label.query(Label.category == 'Standort').get()
			for label in hw.labels:
				if label in categories.tags:
					variables['category'] = label
				if label in locations.tags:
					variables['location'] = label
			variables['hw'] = hw
			variables['edit'] = 'true'

		if action == 'delete':
			template = 'hardware/delete.html'
			variables['title'] = 'Hardware wirklich entfernen?'
			variables['hw'] = hw
			variables['reservations'] = ndb.get_multi( hw.reservations )

		if action == 'copy':
			hwc = {
				'inventory_number'	: 0,
				'title'           	: hw.title,
				'description'     	: hw.description,
				'accessories'     	: hw.accessories,
				'serial_number'  	: hw.serial_number,
				'year'            	: hw.year,
				'costs'           	: hw.costs,
				'invisible'       	: hw.invisible,
				'reservations'    	: hw.reservations,
				'labels' 		    : hw.labels
			}

			template = 'hardware/create_edit.html'
			variables['title'] = hw.title + ' kopieren'
			variables['labels'] = Label.query()
			variables['stichworte'] = Label.query(Label.category == 'Stichwort').get()
			categories = Label.query(Label.category == 'Kategorie').get()
			locations = Label.query(Label.category == 'Standort').get()
			for label in hw.labels:
				if label in categories.tags:
					variables['category'] = label
				if label in locations.tags:
					variables['location'] = label
			variables['hw'] = hwc
			variables['edit'] = 'true'
			variables['copy'] = 'true'

		render(template, variables, self)

	def post(self, action, data):
		redirect_if_not_logged(self)

		template = ''
		variables = {
			'session': self.session,
			'nav_hardware': True
		}

		if data:
			hw = Hardware().get_by_id( int( data ) )

		if action == 'search':
			search_string = self.request.get('search_string')
			serial = self.request.get('serial')
			inventory_number = self.request.get('inventory_number')
			tags = self.request.get_all('tag')
			category = self.request.get('category')
			location = self.request.get('location')

			found = []

			if inventory_number != '':
				found = Hardware.query(Hardware.inventory_number == int(inventory_number)).fetch()
			else:
				hws = Hardware.query()

				if len(tags) > 0:
					for tag in tags:
						hws = hws.filter(Hardware.labels == tag)
				if category != '-':
					hws = hws.filter(Hardware.labels == category)
				if location:
					if location != '-':
						hws = hws.filter(Hardware.labels == location)

				if search_string != '':
					for hw in hws:
						if hw.title.lower().find(search_string.lower()) > -1 or hw.description.lower().find(search_string.lower()) > -1:
							found.append(hw)
				if serial != '':
					for hw in hws:
						if hw.serial_number.lower().find(serial.lower()) > -1 and hw not in found:
							found.append(hw)
				else:
					found = hws.fetch()

			template = 'hardware/search.html'

			variables['title'] = 'Hardware Gefunden'
			variables['session'] = self.session
			variables['labels'] = Label.query()
			variables['search_labels'] = tags
			variables['search_category'] = category
			variables['search_location'] = location
			variables['found'] = found
			variables['hide_options'] = 'true'

			variables['search_string'] = search_string
			variables['serial'] = serial
			variables['inventory_number'] = inventory_number

		if action == 'create':
			hw = Hardware()
			
		if action == 'create' or action == 'edit':
			hw.inventory_number = int( self.request.get('inventory_number') )
			hw.title = self.request.get('title')
			hw.description = self.request.get('description')
			hw.accessories = self.request.get('accessories')
			hw.serial_number = self.request.get('serial_number')
			hw.costs = self.request.get('costs')
			hw.year = int( self.request.get('year') )
			hw.invisible = bool( self.request.get('invisible') )

			hw.labels = []

			for tag in self.request.get_all('tag'):
				if not tag in hw.labels:
					hw.labels.append(tag)
			
			hw.labels.append(self.request.get('category'))
			hw.labels.append(self.request.get('location'))

			hw.put()

			self.redirect('/hardware/view/' + str(hw.key.integer_id()))

			return

		if action == 'delete':
			hw.key.delete()

			template = 'index/message.html'
			variables['title'] = hw.title + ' wurde entfernt.'

		if action == 'invn':
			if Hardware.query().filter(Hardware.inventory_number == int(self.request.get('number'))).get():
				self.response.out.write('true')
			return

		render(template, variables, self)


def clone_entity(e, **extra_args):
	klass = e.__class__
	props = dict((k, v.__get__(e, klass)) for k, v in klass.properties().iteritems())
	props.update(extra_args)
	return klass(**props)
