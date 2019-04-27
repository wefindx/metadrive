import os
import pathlib
from metadrive import config

def set_proxies(proxies):

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

    return proxy

def init_profile(profile, porfiles_dir, recreate_profile):

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

    return local
