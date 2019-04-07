import os
import pathlib
import requests
from metadrive import config
from metadrive import utils

SUBTOOL = os.path.basename(__file__).split('.py')[0]

def get_session(*args, **kwargs):
    return requests.Session(*args, **kwargs)

class RequestsDrive(requests.Session):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response = None
        self.desired_capabilities = {}
        self.metaname = ''

    def get(self, *args, **kwargs):
        self.response = super().get(*args, **kwargs)

        if hasattr(self, 'profile'):
            session_data = requests.utils.dict_from_cookiejar(self.cookies)

            session_prefix_file = os.path.join(
                SUBTOOL, '{drive_id}/cookies.json'.format(
                    drive_id=self.profile
            ))

            utils.save_session_data(session_prefix_file, session_data)

    def quit(self):
        del self


def get_drive(
        profile='default',
        porfiles_dir='.metadrive/sessions/_requests',
        recreate_profile=False,
        proxies='default'):

    ## ----------- TO MOVE TO MIXIN --------------- #
    if proxies == 'default':
        proxies = config.ENSURE_PROXIES()

    if not proxies:
        proxies = {
            'httpProxy': None,
            'sslProxy': None,
            'socksProxy': None
        }

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

    # Initialization section
    local = True

    if local:
        profile_path = os.path.join(
            str(pathlib.Path.home()),
            os.path.join(porfiles_dir, profile))
    else:
        profile_path = None

    if profile_path is not None:

        if not os.path.exists(profile_path):
            os.makedirs(profile_path)

        elif recreate_profile:
            import shutil
            shutil.rmtree(profile_path)

    ## ----------- TO MOVE TO MIXIN --------------- #

    # Instantiating Drive

    if local:
        drive = RequestsDrive()
        drive.subtool = SUBTOOL
        drive.profile = profile
    else:
        drive = None


    if drive is not None:

        session_prefix_file = os.path.join(
            drive.subtool, '{drive_id}/cookies.json'.format(
                drive_id=profile
        ))

        if os.path.exists(os.path.join(config.SESSIONS_DIR, session_prefix_file)):
            session_data = utils.load_session_data(session_prefix_file)
        else:
            session_data = requests.utils.dict_from_cookiejar(drive.cookies)
            # utils.save_session_data(session_prefix_file, session_data)

        if session_data:
            drive.cookies.update(
                requests.utils.cookiejar_from_dict(
                    session_data
                )
            )

        if proxy is not None:
            drive.desired_capabilities.update(
                {'proxy': proxy}
            )

    return drive
