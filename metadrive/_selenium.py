'''
Provides a function to get a new browser with session in specific directory.

get_browser(profile_name='default', profiles_dir='.chrome-profile', local=DEVELOPMENT)

# To create selenium driver may use something like:
docker run -d -p 4444:4444 selenium/standalone-chrome:3.7.1-beryllium
'''
import os
import pathlib

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

def get_browser(
        profile_name='selenium',
        porfiles_dir='.metadrive/sessions',
        driver_location='',
        headless=False,
        load_images=True,
        load_adblocker=True,
        recreate_profile=False,
        download_to=''
    ):

    '''
    Gets a new browser, with session in specific directory.
    '''
    # ------------- OPTIONS SECTION ------------ #
    OPTIONS = Options()

    OPTIONS.add_argument("--window-size=1600,900")
    OPTIONS.add_argument("--disable-infobars")
    OPTIONS.add_argument('--no-sandbox')
    OPTIONS.add_argument('--disable-dev-shm-usage')
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
        profile = os.path.join(
            str(pathlib.Path.home()),
            os.path.join(porfiles_dir, profile_name))
    else:
        profile = None

    if profile is not None:

        OPTIONS.add_argument("--user-data-dir={}".format(profile));

        if not profile:
            os.makedirs(profile)
        else:
            if recreate_profile:
                import shutil
                shutil.rmtree(profile)

    if local:
        if CHROME_DRIVER_LOCATION:
            browser = webdriver.Chrome(
                CHROME_DRIVER_LOCATION,
                chrome_options=OPTIONS)
        else:
            browser = webdriver.Chrome(
                chrome_options=OPTIONS)
    else:
        browser = webdriver.Remote(
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

    return browser

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
