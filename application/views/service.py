from application.basehandler import *
import csv, logging


class DeleteAll( BaseHandler ):
	def get(self):
		redirect_if_not_admin(self)

		db.delete(Hardware.all())
		db.delete(Reservation.all())
		db.delete(Category.all())
		db.delete(Location.all())

class HardwareDelete( BaseHandler ):
	def get(self):
		redirect_if_not_admin(self)

		db.delete(Hardware.all())


class ReservationDelete( BaseHandler ):
	def get(self):
		redirect_if_not_admin(self)

		db.delete(Reservation.all())

class DeleteCatLox( BaseHandler ):
	def get(self):
		redirect_if_not_admin(self)

		db.delete(Category.all())
		db.delete(Location.all())

class CSVCheck( BaseHandler ):
	def get(self):
		redirect_if_not_admin(self)

		render( 'index/csvcheck.html', {}, self)

	def post(self):
		redirect_if_not_admin(self)

		csv_data = self.request.get('csvimport')
		fileReader = csv.reader(csv_data.split("\n"))

		for row in fileReader:
			count = 1
			hw = Hardware()

			for val in row:
				if val == '\N':
					val = ''
				if count == 1:
					self.response.out.write(int(val))
				if count == 2:
					self.response.out.write(val)
				if count == 3:
					self.response.out.write(val)
				if count == 4:
					self.response.out.write(val)
				if count == 5:
					self.response.out.write(val)
				if count == 7:
					self.response.out.write(int(val))
				if count == 8:
					self.response.out.write(val)
				if count == 9:
					self.response.out.write(val)
				if count == 10:
					self.response.out.write(int(val))
				if count == 11:
					self.response.out.write(val)

				count += 1

class HardwareExport(BaseHandler):
	def get(self, _count, _offset):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('Inventarnummer, Titel, Beschreibung, Zubehoer, Seriennummer, Jahr, Preis, Unsichtbar, Labels\n')

		for hw in Hardware.query().fetch(int(_count), offset=int(_offset)):
			self.response.out.write(hw.inventory_number)
			self.response.out.write(';')
			self.response.out.write(hw.title)
			self.response.out.write(';')
			self.response.out.write(hw.description)
			self.response.out.write(';')
			self.response.out.write(hw.accessories)
			self.response.out.write(';')
			self.response.out.write(hw.serial_number)
			self.response.out.write(';')
			self.response.out.write(hw.year)
			self.response.out.write(';')
			self.response.out.write(hw.costs)
			self.response.out.write(';')
			self.response.out.write(hw.invisible)
			self.response.out.write(';')
			self.response.out.write(hw.labels)
			self.response.out.write('\n')

# class HardwareExport( BaseHandler ):
# 	def get(self, _offset, lecount):

# 		self.response.headers['Content-Type'] = 'text/plain'
# 		self.response.out.write('#, Inventarnummer, Titel, Beschreibung, Zubehoer, Seriennummer, Jahr, Preis, Unsichtbar, Labels\n')

#         c = 1

#         for hw in Hardware.query().fetch(int(_count), offset=int(_offset)):
# 			self.response.out.write(c)
# 			self.response.out.write(',')
# 			self.response.out.write(hw.inventory_number)
# 			self.response.out.write(',')
# 			self.response.out.write(hw.title)
# 			self.response.out.write(',')
# 			self.response.out.write(hw.description)
# 			self.response.out.write(',')
# 			self.response.out.write(hw.accessories)
# 			self.response.out.write(',')
# 			self.response.out.write(hw.serial_number)
# 			self.response.out.write(',')
# 			self.response.out.write(hw.year)
# 			self.response.out.write(',')
# 			self.response.out.write(hw.costs)
# 			self.response.out.write(',')
# 			self.response.out.write(hw.invisible)
# 			self.response.out.write(',')
# 			self.response.out.write(hw.labels)
# 			self.response.out.write('\n')

# 			c += 1

class HardwareImport( BaseHandler ):
	def get(self):
		redirect_if_not_admin(self)

		render( 'index/hardwareimport.html', {}, self)
	def post(self):
		redirect_if_not_admin(self)

		csv_data = self.request.get('csvimport')
		fileReader = csv.reader(csv_data.split("\n"))

		for row in fileReader:
			count = 1
			hw = Hardware()

			for val in row:

				try:
					unicode(val, "ascii")
				except UnicodeDecodeError:
					val = unicode(val, "utf-8")

				if val == '\n':
					val = ''
				if count == 1:
					hw.old_id = int(val)
				if count == 2:
					hw.title = val
				if count == 3:
					hw.description = val
				if count == 4:
					hw.accessories = val
				if count == 5:
					location = return_location(locations[val])
					hw.location = location
					hw.location_id = location.key().id()
				if count == 7:
					hw.inventory_number = int(val)
				if count == 8:
					category = return_category(categories[val])
					hw.category = category
					hw.category_id = category.key().id()
				if count == 9:
					hw.serial_number = val
				if count == 10:
					hw.year = int(val)
				if count == 11:
					hw.costs = val

				count += 1

			hw.invisible = False
			hw.put()

categories = {
	"41": "Beamer",
	"44": "Diverses",
	"45": "Drucker",
	"46": "DVD-Player",
	"47": "Fernseher",
	"48": "Fotokamera",
	"52": "Laufwerk",
	"54": "Licht",
	"59": "Netzwerk",
	"60": "Scanner",
	"61": "Stativ",
	"62": "Telefon",
	"65": "Videokamera",
	"66": "Videokarte",
	"67": "Webkamera",
	"68": "Buerozubehoer",
	"70": "Videorecorder",
	"72": "Tastatur, Maus usw",
	"74": "Energie",
	"75": "Kabelschloss",
	"76": "Werkzeug",
	"79": "Schluessel",
	"58": "Monitor Roehre",
	"80": "Monitor Flach",
	"81": "Adapter",
	"82": "Dongle",
	"40": "Audio-Mixer, Interface",
	"49": "Dia und OH-Projektor",
	"42": "Audio Rec/Play/Amp/Sets",
	"53": "Audio-Lautsprecher",
	"69": "Audio-Kopfhoerer",
	"55": "Audio-Mikro",
	"50": "Rechner PC",
	"77": "Rechner Apple"
}

locations = {
	"118": "Vortragsraum BSH EG",
	"119": "Senones",
	"141": "Treppenhaus, Gang BSH 1. OG",
	"143": "Terassenzimmer BSH 1.OG",
	"144": "Druckerzimmer BSH 1.OG",
	"140": "Gaestewohnung BSH 2.OG",
	"132": "Werkstatt BSH 1.UG",
	"131": "Serverraum BSH EG",
	"101": "Galerie BSH 2.OG",
	"104": "E-Room BSH EG",
	"106": "Office Regine Halter BSH 1.OG",
	"107": "Office Mischa Schaub BSH EG",
	"111": "Sitzungsraum gross BSH EG",
	"112": "Dozentenzimmer BSH 1.OG",
	"117": "Durchgang zum Hof BSH EG",
	"121": "Alte Kueche BSH EG",
	"123": "Aufgang Gaeste-Whg. BSH 1.OG",
	"124": "Entree BSH EG",
	"127": "Wintergarten BSH EG",
	"129": "Safe BSH EG",
	"130": "Mediaspace BSH UG",
	"142": "Office Elena Mores BSH 1.OG",
	"134": ".extern",
	"145": "IRoom BSH Hof",
	"126": ".www",
	"122": ".missing",
	"120": ".Benutzer",
	"96": ".in Reparatur",
	"146": "Sitzungsraum klein BSH 1.OG",
	"147": "Eckzimmer BSH 1.OG",
	"149": "Dachboden BSH 2.OG",
	"154": "Metall Lager BSH 1.UG",
	"155": "Heizungskeller BSH 1.UG",
	"156": "Kueche Staff BSH 1.OG",
	"153": "3D-Fraese BSH EG",
	"98": "Spiga 6.OG, Seminarraum",
	"97": "Spiga 5.OG, Student Thinkspace",
	"152": "Spiga 4.OG",
	"114": "Arbeitszimmer 35 BSH 1.OG (Rasso)",
	"128": "Balkenraum BSH 1.OG",
	"95": "Neues Lager BSH 1.OG Zi 36",
	"115": "Altes Lager, BSH EG",
	"110": "Studio BSH 3.OG",
	"133": "Spiga 4.OG AVStudio",
	"157": "Spiga 4 Videoschnitt",
	"116": "Projektraum BSH 2.OG",
	"160": "Spiga 4 Arbeitszimmer",
	"158": "Spiga 4 Plotter",
	"159": "Spiga 4 Depot",
	"109": "Arbeitszimmer 25 BSH 1.OG (Ralf)",
	"113": "Arbeitszimmer 31 BSH 1.OG (Mauro)",
	"102": "Alte Bibliothek BSH 1.OG"
}

def return_category(category_title):
	category = Category.all().filter('title = ', category_title).get()

	if not category:
		category = Category( title = category_title )
		category.put()

	return category

def return_location(location_title):
	location = Location.all().filter('title = ', location_title).get()

	if not location:
		location = Location( title = location_title )
		location.put()

	return location


class ReservationImport( BaseHandler ):
	def get(self):
		redirect_if_not_admin(self)

		render( 'index/reservationimport.html', {}, self)
	def post(self):
		redirect_if_not_admin(self)

		csv_data = self.request.get('csvimport')

		fileReader = csv.reader(csv_data.split("\n"))
		for row in fileReader:
			count = 1
			save = True
			res = Reservation()
			item = Hardware()
			save = True

			for val in row:

				try:
					unicode(val, "ascii")
				except UnicodeDecodeError:
					logging.error(val)
					val = unicode(val, "utf-8")
				
				if val == '\n':
					val = ''
				if count ==2:
					if val == 'sw':
						save = False
						break
				if count == 3:
					if Hardware.all().filter('old_id =', int(val)).get():
						item = Hardware.all().filter('old_id =', int(val)).get()
						res.item = item.key()
					else:
						save = False
				if count == 4:
					nickname = val.split('@')[0]
					user = UserData.all().filter('nickname =', nickname).get()

					if not user:
						user = UserData(
							    nickname   = nickname,
							    firstname   = nickname.split('.')[0].capitalize(),
							    lastname    = nickname.split('.')[1].capitalize(),
							    admin        = False,
							    locked       = False ).put()

						res.user = user
					else:
						res.user = user.key()

				if count == 5:
					res.between = datetime.datetime.strptime(val.split(' ')[0], '%Y-%m-%d' ).date()
				if count == 6:
					res.until = datetime.datetime.strptime(val.split(' ')[0], '%Y-%m-%d' ).date()
				if count == 7:
					res.why = val
				if count == 8:
					if val == 't':
						res.state = 2
					else:
						res.state = 1

				count += 1

			if save:
				if save:
					res.put()
					item.reservations.append( res.key() )
					item.put()



class ImportCleanUp( BaseHandler ):
	def get(self):
		redirect_if_not_admin(self)

		for hw in Hardware.all():
			if hw.title == None:
				hw.delete()

		for res in Reservation.all():
			if res.between == None:
				res.delete()
			if res.item == None:
				res.delete()

class ConvertCatLoc(BaseHandler):
	def get(self, _offset, _count):
		for hw in Hardware.query().fetch(int(_count), offset=int(_offset)):
			hw.tags = []
			hw.put()

			cat = Tag.query().filter( Tag.title == hw.category.get().title ).get()
			loc = Tag.query().filter( Tag.title == hw.location.get().title ).get()

			if not cat:
				cat = Tag(
					title = hw.category.get().title,
					category = 'category'
					).put()

				hw.tags.append(cat)
			else:
				hw.tags.append(cat.key)
			if not loc:
				loc = Tag(
					title = hw.location.get().title,
					category = 'location'
					).put()

				hw.tags.append(loc)
			else:
				hw.tags.append(loc.key)

			hw.put()

class ConvertTagsToLabels(BaseHandler):
	def get(self, _offset, _count):
		for hw in Hardware.query().fetch(int(_count), offset=int(_offset)):
			hw.labels = []
			hw.put()

			for t in ndb.get_multi(hw.tags):
				label = Label.query(Label.category == t.category).get()
				if not label:
					label = Label(category = t.category)
				if not t.title in label.tags:
					label.tags.append(t.title)
					label.put()
				
				if not t.title in hw.labels:
					hw.labels.append(t.title)
					hw.put()


class FillInLager(BaseHandler):
	def get(self, _offset, _count):

		locations = Label.query(Label.category == 'Standort').get()

		if not 'Lager' in locations.tags:
			locations.tags.append('Lager')
			locations.put()

		for hw in Hardware.query().fetch(int(_count), offset=int(_offset)):
			has_location = False
			for l in hw.labels:
				if l in locations.tags:
					has_location = True

			if not has_location:
				hw.labels.append('Lager')
				hw.put()
