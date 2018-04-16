from application.views import main, hardware, reservation, user, labels, bookmarks, service

routing = [
		
	('/', main.Index ),
	('/dashboard', main.Dashboard ),
	('/locked', main.Locked ),

	('/hardware/(.*)/(.*)', hardware.Handling),
	('/reservation/(.*)/(.*)', reservation.Handling),
	('/labels/(.*)/(.*)', labels.Handling),
	('/users/(.*)/(.*)', user.Handling),
	('/bookmarks/(.*)/(.*)', bookmarks.Handling),
	('/numbers/(.*)/(.*)', main.Numbers),

	('/fillinlager/(.*)/(.*)', service.FillInLager ),
	('/export/(.*)/(.*)', service.HardwareExport )


    # this urls were for importing and cleaning the old database

	# ('/deleteall', service.DeleteAll ),
	# ('/hardwareimport', service.HardwareImport ),
	# ('/hardwaredelete', service.HardwareDelete ),
	# ('/reservationimport', service.ReservationImport ),
	# ('/reservationdelete', service.ReservationDelete ),
	# ('/importcleanup', service.ImportCleanUp ),
	# ('/csvcheck', service.CSVCheck ),
	# ('/convertcatloc/(.*)/(.*)', service.ConvertCatLoc ),
	# ('/converttagstolabels/(.*)/(.*)', service.ConvertTagsToLabels )

]
