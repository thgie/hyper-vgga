from google.appengine.ext import ndb

class Label(ndb.Model):
	category 	    	  = ndb.StringProperty()
	tags 		    	    = ndb.StringProperty(repeated=True)

class Hardware(ndb.Model):
	inventory_number	= ndb.IntegerProperty()
	title           	= ndb.StringProperty()
	description     	= ndb.TextProperty()
	accessories     	= ndb.TextProperty()
	serial_number  		= ndb.StringProperty()
	year            	= ndb.IntegerProperty()
	costs           	= ndb.StringProperty()
	invisible       	= ndb.BooleanProperty()
	reservations    	= ndb.KeyProperty(kind='Reservation', repeated=True)
	labels 		    	  = ndb.StringProperty(repeated=True)

class UserData(ndb.Model):
	user		    	  = ndb.UserProperty()
	nickname	    	= ndb.StringProperty()
	firstname	    	= ndb.StringProperty()
	lastname	    	= ndb.StringProperty()
	admin		    	  = ndb.BooleanProperty()
	locked		    	= ndb.BooleanProperty()
	bookmarks       = ndb.KeyProperty(kind='Hardware', repeated=True)

class Reservation(ndb.Model):
	between		    	  = ndb.DateProperty()
	until		    	    = ndb.DateProperty()
	why			          = ndb.TextProperty()
	user		    	    = ndb.KeyProperty(kind='UserData')
	item		    	    = ndb.KeyProperty(kind='Hardware')
	state		    	    = ndb.IntegerProperty()
