# This includes the methods available to items of the source for user with session.
import bs4

class Topic:

    def __init__(self, idea_url, session):
        self.session = session
        self.idea_url = idea_url
        if '://www.halfbakery.com/lr/' not in self.idea_url:
            self.idea_url = self.idea_url.replace(
                '://www.halfbakery.com/',
                '://www.halfbakery.com/lr/'
            )

    def update(self):
        '''
        Edits own idea.
        '''
        raise NotImplemented

    def delete(self):
        '''
        Deletes own idea.
        '''
        raise NotImplemented

    def vote(self, value: int):
        '''
        Changes your vote on an idea. Value can be betwee -1, 0, 1.
        '''
        page = self.session.get(self.idea_url)
        if page.ok:
            soup = bs4.BeautifulSoup(page.content, 'html.parser')
            sig = soup.find('input', {'name': 'sig'})
            if sig:
                sig = sig.attrs['value']
            else:
                raise Exception("Log in to vote.")
        else:
            raise Exception("Log in to vote.")

        if value == -1:
            self.session.get(
                self.idea_url,
                params={
                    'op': 'nay',
                    'sig': sig
                }
            )

        if value == 0:
            self.session.get(
                self.idea_url,
                params={
                    'op': 'unvote',
                    'sig': sig
                }
            )
        if value == 1:
            self.session.get(
                self.idea_url,
                params={
                    'op': 'aye',
                    'sig': sig
                }
            )


    def addnote(self, text):
        '''
        Creates an annotation to an idea.
        '''
        raise NotImplemented

    def updnote(self, anno_url, text):
        '''
        Edits own annotation to an idea.
        '''
        raise NotImplemented

    def delnote(self, anno_url):
        '''
        Deletes own annotation from an idea.
        '''
        raise NotImplemented
