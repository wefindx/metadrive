# this includes the methods available to items of the source


class Topic:

    def __init__(self, session):
        self.type = '::mindey/topic#halfbakery'

    def new_idea(self, title, summary, text):
        pass

    def edit_idea(self, title, summary, text):
        pass

    def delete_idea(self):
        pass

    def vote_idea(self, value):
        pass

    def new_anno(self, text):
        pass

    def edit_anno(self, text):
        pass

    def delete_anno(self):
        pass
