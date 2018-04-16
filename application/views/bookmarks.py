from application.basehandler import *
import logging

""" BOOKMARKS """

class Handling( BaseHandler ):
    def get(self, action, data):
        redirect_if_not_logged(self)

        template = ''
        variables = {
            'session': self.session,
            'nav_bookmarks': True,
            'title': 'Bookmarks'
        }

        if data:
            hw = Hardware().get_by_id( int( data ) )
            pass

        user = UserData.query().filter( UserData.nickname == users.get_current_user().nickname() ).get()

        if action == 'view':
            template = 'bookmarks/view.html'
            bookmarks = []

            for bookmark in ndb.get_multi(user.bookmarks):
                if bookmark:
                    bookmarks.append(bookmark)

            variables['bookmarks'] = bookmarks

        if action == 'add':
            if not hw.key in user.bookmarks:
                user.bookmarks.append(hw.key)
                user.put()
            self.redirect(self.request.referer)
            return

        if action == 'delete':
            user.bookmarks.remove(hw.key)
            user.put()
            self.redirect(self.request.referer)
            return

        render(template, variables, self)
