import os
import inspect
import pathlib
import requests
from metadrive import config
from metadrive import utils
from metadrive import mixins

SUBTOOL = os.path.basename(__file__).split('.py')[0]

def get_session(*args, **kwargs):
    return requests.Session(*args, **kwargs)

class RequestsDrive(requests.Session):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response = None
        self.desired_capabilities = {}
        self.metaname = ''

    def common_before(self, *args, **kwargs):
        proxy = self.desired_capabilities.get('proxy')
        if isinstance(proxy, dict):
            socks = proxy.get('socksProxy')
            if isinstance(socks, str):
                proxies = {
                    'http': 'socks5h://{}'.format(socks),
                    'https': 'socks5h://{}'.format(socks)}
                kwargs.update({'proxies': proxies})

    def common_after(self, *args, **kwargs):
        if hasattr(self, 'profile'):

            cookies_data = requests.utils.dict_from_cookiejar(self.cookies)
            headers_data = requests.utils.dict_from_cookiejar(self.cookies)

            session_data = {
                'cookies': cookies_data,
                'headers': headers_data
            }

            session_prefix_file = os.path.join(
                SUBTOOL, '{drive_id}/session.json'.format(
                    drive_id=self.profile
            ))

            utils.save_session_data(session_prefix_file, session_data)

    def get(self, *args, **kwargs):
        self.common_before(self, *args, **kwargs)
        self.response = super().get(*args, **kwargs)
        self.common_after(self, *args, **kwargs)

    def post(self, *args, **kwargs):
        self.common_before(self, *args, **kwargs)
        self.response = super().post(*args, **kwargs)
        self.common_after(self, *args, **kwargs)

    def quit(self):
        del self


def get_drive(
        profile='default',
        porfiles_dir='.metadrive/sessions/_requests',
        recreate_profile=False,
        proxies='default'):

    ## ----------- TO MOVE TO MIXIN --------------- #
    proxy = mixins.set_proxies(proxies)
    local = mixins.init_profile(profile, porfiles_dir, recreate_profile)

    # Instantiating Drive

    if local:
        drive = RequestsDrive()
        drive.subtool = SUBTOOL
        drive.profile = profile
    else:
        drive = None


    if drive is not None:

        session_prefix_file = os.path.join(
            drive.subtool, '{drive_id}/session.json'.format(
                drive_id=profile
        ))

        if os.path.exists(os.path.join(config.SESSIONS_DIR, session_prefix_file)):
            session_data = utils.load_session_data(session_prefix_file)
        else:
            session_data = {
                'cookies': requests.utils.dict_from_cookiejar(drive.cookies),
                'headers': drive.headers
            }
            # utils.save_session_data(session_prefix_file, session_data)

        if session_data:
            drive.headers.update(
                session_data.get('headers') or {}
            )
            drive.cookies.update(
                requests.utils.cookiejar_from_dict(
                    session_data.get('cookies') or {}
                )
            )

        if proxy is not None:
            drive.desired_capabilities.update(
                {'proxy': proxy}
            )


        # LATER MOVE TO MIXIN
        drive.caller_module = inspect.getmodule(inspect.currentframe().f_back)

    return drive
