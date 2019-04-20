'''
Provides a function to get a new browser with session in specific directory.

get_drive(profile='default', profiles_dir='.chrome-profile', local=DEVELOPMENT)

# To create selenium driver may use something like:
docker run -d -p 4444:4444 selenium/standalone-chrome:3.7.1-beryllium
'''
import os
import inspect
import pathlib

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from metadrive import config
from deprecated import deprecated

class TabsMixin:

    def open_tab(self, name, url=None):
        if name not in self.tabs:
            if url is not None:
                self.execute_script("window.open('{}', '_blank');".format(url))
                self.tabs[name] = self.window_handles[-1]
            else:
                raise Exception('Tab not found, and url not provided.')
        else:
            self.switch_to.window(self.tabs[name])
    def current_tab(self):
        return next(filter(lambda x: x[1] == self.current_window_handle, self.tabs.items()))

    def switch_tab(self, name):
        self.open_tab(name)

    def close_tab(self, name):
        self.switch_tab(name)
        self.close()


class Chrome(webdriver.Chrome, TabsMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabs = {'default': self.current_window_handle}
        self.metaname = ''

class Remote(webdriver.Remote, TabsMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabs = {'default': self.current_window_handle}
        self.metaname = ''

def get_drive(
        driver_location=config.CHROME_DRIVER,
        profile='default',
        porfiles_dir='.metadrive/sessions/_selenium',
        headless=False,
        load_images=True,
        load_adblocker=True,
        recreate_profile=False,
        download_to='',
        proxies='default',
    ):

    '''
    Gets a new browser, with session in specific directory.

    proxies = {
        'httpProxy': None,
        'sslProxy': None,
        'socksProxy': '127.0.0.1:9999',
    }

    Can use requests-like proxy specification, e.g.:

    proxies= {
        'http': 'socks5h://127.0.0.1:9999',
        'https': 'socks5h://127.0.0.1:9999'
    }

    '''
    if proxies == 'default':
        proxies = config.ENSURE_PROXIES()

    if not proxies:
        proxies = {
            'httpProxy': None,
            'sslProxy': None,
            'socksProxy': None
        }

    # ------------- PROXIES SECTION ------------ #
    proxy = {'proxyType': 'MANUAL'}
    for key in proxies:
        if proxies[key] is not None:
            if key == 'http_proxy':
                Key = 'httpProxy'
            elif key == 'ssl_proxy':
                Key = 'sslProxy'
            elif key == 'socks_proxy':
                Key = 'socksProxy'
            else:
                Key = key

            if Key in ['http', 'https']:
                Value = proxies[key].rsplit('//', 1)[-1]
                proxy['socksProxy'] = Value
            else:
                proxy[Key] = proxies[key]

    if len(proxy) <= 1:
        proxy = None

    # ------------- OPTIONS SECTION ------------ #
    OPTIONS = Options()

    OPTIONS.add_argument("--window-size=1600,900")
    OPTIONS.add_argument("--disable-infobars")
    OPTIONS.add_argument('--no-sandbox')
    OPTIONS.add_argument('--disable-dev-shm-usage')

    if isinstance(proxy, dict):

        if proxy.get('socksProxy') is not None:
            OPTIONS.add_argument(
                '--proxy-server=socks5://{}'.format(
                    proxy['socksProxy']))
        elif proxy.get('sslProxy') is not None:
            OPTIONS.add_argument(
                '--proxy-server=https://{}'.format(
                    proxy['sslProxy']))
        elif proxy.get('httpProxy') is not None:
            OPTIONS.add_argument(
                '--proxy-server=http://{}'.format(
                    proxy['httpProxy']))


#    OPTIONS.add_argument('--ignore-ssl-errors=yes')
#    OPTIONS.add_argument('--ssl-protocol=any')
#    OPTIONS.add_argument('--web-security=no')


    PREFERENCES = {}
    #OPTIONS.experimental_options["prefs"] = PREFERENCES

    if headless:
        OPTIONS.add_argument('--headless')

    if load_images:
        PREFERENCES["profile.default_content_settings"] = {"images": 0}
        PREFERENCES["profile.managed_default_content_settings"] = {"images": 0}
    else:
        PREFERENCES["profile.default_content_settings"] = {"images": 2}
        PREFERENCES["profile.managed_default_content_settings"] = {"images": 2}

    if download_to:
        PREFERENCES.update(
            {'download.default_directory' : download_to,
             'download.prompt_for_download': False,
             'download.directory_upgrade': True,
             'safebrowsing.enabled': False,
             'safebrowsing.disable_download_protection': True})

    OPTIONS.add_experimental_option('prefs', PREFERENCES)

    if load_adblocker:
        try:
            # OPTIONS.add_extension(os.path.join(os.getcwd(), 'subtools/extensions/ghostery.crx'))
            OPTIONS.add_extension(
                os.path.join(os.getcwd(), 'subtools/selenium/extensions/ublock_origin.crx'))
        except:
            pass

    # ------------- INITIALIZATION SECTION ------------ #
    if driver_location.startswith('http'):
        # e.g.: http://0.0.0.0:4444/wd/hub
        SELENIUM_HUB_URL = driver_location
        CHROME_DRIVER_LOCATION = ''
        local = False
    else:
        SELENIUM_HUB_URL = ''
        CHROME_DRIVER_LOCATION = driver_location
        local = True


    if local:
        profile_path = os.path.join(
            str(pathlib.Path.home()),
            os.path.join(porfiles_dir, profile))
    else:
        profile_path = None

    if profile_path is not None:

        OPTIONS.add_argument("--user-data-dir={}".format(profile_path));

        if not profile_path:
            os.makedirs(profile_path)
        else:
            if recreate_profile:
                import shutil
                shutil.rmtree(profile_path)

    if local:
        if CHROME_DRIVER_LOCATION:
            browser = Chrome(
                CHROME_DRIVER_LOCATION,
                chrome_options=OPTIONS)
        else:
            browser = Chrome(
                chrome_options=OPTIONS)
    else:
        browser = Remote(
            SELENIUM_HUB_URL,
            dict(
                webdriver.DesiredCapabilities.CHROME,
                **OPTIONS.to_capabilities()
            )
        )

    if download_to:

        browser.command_executor._commands["send_command"] = (
            "POST", '/session/$sessionId/chromium/send_command')

        browser.desired_capabilities['browserName'] = 'ur mum'

        browser.execute(
            "send_command", {
                'cmd': 'Page.setDownloadBehavior',
                'params': {
                    'behavior': 'allow',
                    'downloadPath': download_to}})

    if proxy is not None:
        browser.desired_capabilities.update(
            {'proxy': proxy}
        )

    browser.profile = profile
    browser.subtool = '_selenium'
    browser.caller_module = inspect.getmodule(inspect.currentframe().f_back)

    return browser

@deprecated(reason="Use get_drive() instead.")
def get_driver(
        driver_location=config.CHROME_DRIVER,
        profile='default',
        porfiles_dir='.metadrive/sessions/_selenium',
        headless=False,
        load_images=True,
        load_adblocker=True,
        recreate_profile=False,
        download_to='',
        proxies='default',
    ):

    return get_drive(
        driver_location=driver_location,
        profile=profile,
        porfiles_dir=porfiles_dir,
        headless=headless,
        load_images=load_images,
        load_adblocker=load_adblocker,
        recreate_profile=recreate_profile,
        download_to=download_to,
        proxies=proxies
    )


def save_as(element, driver):
    '''
    Click "Save as ..." on element with driver.
    '''
    from selenium.webdriver.common.action_chains import ActionChains
    ActionChains(driver).context_click(element).perform()

    import pyautogui
    import base64
    from PIL import Image
    from io import BytesIO

    as__ = Image.open(
        BytesIO(
            base64.b64decode(
                'iVBORw0KGgoAAAANSUhEUgAAACMAAAAQCAIAAAATVVENAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4gsTAjMlHs+8UAAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAABrElEQVQ4y2P8//8/A10AEwO9wKhNlAAWZM7SFStXrVn78tUrXl5eTzfXvOwsFhYWiPiSZcs/ffrExsbm7elRUlhAjlX/kcCOXbsfPX7879+/e/fvewcELVm2/P///w8ePDSxsrl3//7///+/fft26cqV/2QBlNBzd3WRlZFhZGRUVFAIDw05efo0AwMDCwvL////r9+4+fnLF05OTl1tbfJCjxE5Px06cnThkiVPnjxlYGD4/uO7nKzckvlzGRgY9h04uHzVqsuXr6ioqKQlJ9nZWFMUem/fvTM0tzx4+Mjfv3////+/eOmy6PhEZO///Plz1dq1RhZWX758oSj0vn/7/u/fPw01VSYmpg8fP67buBEi/vDho+MnT/78+ZONjU1QQJCRkZGJmZmBgeHYiRPzFy2GqHnz9m3vhIlv3r6FcOcvWnzsxAmcaU9aWqogJzs5I0tQUICPl8/R3v7kqdMMDAw/f/2cOn3m/QcPGJmYpKUk+7o6OTk4GBgYLl66vH3XrsS4WAYGhg8fPixauszf10dEWJiBgWH9pk2ebm5WFhY442m0jBi0NgEAiOU/HUCPdjUAAAAASUVORK5CYII=')))

    position = pyautogui.locateOnScreen(as__)

    if position:
        print(position)
        pyautogui.click(x=position[0],y=position[1])
    else:
        print('Could find "Save as ..." position. Try local, non-headless.')
