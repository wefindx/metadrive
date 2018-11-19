from selenium.webdriver.common.keys import Keys

class Topic:
    def __init__(self, topic_url, session):
        self.driver = session
        self.driver.get(topic_url)

    def comment(self, text):
        self.driver.find_element_by_class_name('button comment').click()
        self.driver.find_element_by_class_name('mentions-texteditor__content').send_keys(text)
        self.driver.find_element_by_class_name('feed-shared-comment-box__submit-button button-primary-small').click()

class Contact:
    pass

class Message:
    pass
