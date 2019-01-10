import random
import requests

from metadrive._requests import get_session
from metadrive import utils

class UserAgents:

    @classmethod
    def random_android(self):

        if not hasattr(self, 'user_agents'):
            self.user_agents = requests.get(
                'https://raw.githubusercontent.com/N0taN3rd/userAgentLists/master/json/android-browser.json').json()

        user_agent = random.choice(self.user_agents).get('ua')

        return user_agent

class RequestsCookieAuthentication:

    def __init__(self, raw_cookie, key_name, proxies={}):
        self.key_name = key_name
        self.raw_cookie = raw_cookie
        self.proxies = proxies

    def authenticate(self):
        session = get_session()
        session.metaname = utils.get_metaname(self.key_name)

        if self.raw_cookie is None:

            session_data = utils.load_session_data(namespace=self.key_name)

            if session_data:
                session.cookies.update(
                    requests.utils.cookiejar_from_dict(
                        session_data))
                return session

            else:
                credential = utils.get_or_ask_credentials(
                    namespace=self.key_name,
                    variables=['cookie'])

                if credential:
                    session.headers.update(dict({
                        'content-type':'text/plain',
                    }, **credential))
                else:
                    raise Warning("Credential is not provided, some data may not be retrieved.")

        else:
            session.headers.update({
                'content-type':'text/plain',
                'cookie': self.raw_cookie
            })

        return session
