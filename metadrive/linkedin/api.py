from selenium.webdriver.common.keys import Keys

class Topic:
    def __init__(self, topic_url, session):
        self.driver = session

    def comment(self, text):
        self.driver.get(topic_url)
        self.driver.find_element_by_class_name('mentions-texteditor__content').click()
        self.driver.send_keys(text)
        self.driver.find_element_by_class_name('feed-shared-comment-box__submit-button').click()

class Contact:
    pass

class Message:
    pass
