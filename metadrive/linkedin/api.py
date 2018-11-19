from selenium.webdriver.common.keys import Keys

class Topic:
    def __init__(self, topic_url, session):
        self.driver = session
        self.driver.get(topic_url)

    def comment(self, text):
        field = self.driver.find_element_by_class_name('mentions-texteditor__contenteditable')
        field.send_keys(text)
        button = self.driver.find_element_by_class_name('feed-shared-comment-box__submit-button')
        button.click()

class Contact:
    pass

class Message:
    pass
