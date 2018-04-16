from application.basehandler import *
import logging


""" CATEGORIES & LOCATIONS """

class Handling( BaseHandler ):
	def get(self, action, data):
		redirect_if_not_logged(self)

		template = ''
		variables = {
			'session': self.session,
			'nav_admin': True
		}

		if data:
			pass

		if action == 'all':
			template = 'labels/all.html'
			variables['labels'] = Label.query()
			variables['title'] = 'Labels verwalten'

		if action == 'view':
			template = 'labels/one.html'
			variables['label'] = Label.query(Label.tags == data).get()
			variables['tag'] = data
			variables['title'] = 'Label editieren'

		if action == 'delete':
			label = Label.query(Label.tags == data).get()
			label.tags.remove(data)
			label.put()

			for hw in Hardware.query(Hardware.labels == data).fetch():
				hw.labels.remove(data)
				hw.put()

			self.redirect( '/labels/all/' )

			return

		render(template, variables, self)

	def post(self, action, data):
		redirect_if_not_logged(self)

		if action == 'create':
			label = Label.query(Label.category == self.request.get('category')).get()
			if not label:
				Label(
					tags     = [self.request.get('tag')],
					category = self.request.get('category')
				).put()
			else:
				label.tags.append(self.request.get('tag'))
				label.put()

			self.redirect( '/labels/all/' )

			return

		if action == 'edit':
			label = Label.query(Label.tags == data).get()
			label.tags.remove(data)

			if(label.category != self.request.get('category')):
				label.put()
				label = Label.query(Label.category == self.request.get('category')).get()

			if not self.request.get('tag') in label.tags:
				label.tags.append(self.request.get('tag'))
			
			label.put()

			for hw in Hardware.query(Hardware.labels == data).fetch():
				hw.labels.remove(data)
				hw.labels.append(self.request.get('tag'))
				hw.put()

			self.redirect( '/labels/all/' )

			return
