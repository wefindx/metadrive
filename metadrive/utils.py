import os
import yaml
import json
import config
import requests
import gpgrecord

MAIN = 'main'


def get_metaname(namespace):
    return '-:{gituser}/+/{namespace}.md#{main}'.format(
        gituser=config.GITHUB_USER,
        namespace=namespace,
        main=MAIN
    )

def get_credential(namespace):
    '''
    namespace: -- service name, by directory

    Example:
    >>> get_credential('gmail')
    '''

    from metaform import get_schema

    try:
        data = get_schema(get_metaname(namespace))

        credential = gpgrecord.decrypt_data(data)

        return credential

    except:
        return None

def set_credential(namespace, credential):
    '''
    namespace: -- service name, by directory

    Example:
    >>> set_credential('gmail', {'username': '', 'password': ''})
    '''
    GPG_KEY = config.ENSURE_GPG()

    if credential:
        encrypted_credential = gpgrecord.encrypt_data(
            credential,
            GPG_KEY
        )

        content = '''## {main}
```yaml
{cont}
```'''.format(
            main=MAIN,
            cont=yaml.dump(encrypted_credential)
        )

        with open(
                os.path.join(
                    config.CREDENTIALS_DIR,
                    namespace+'.md'), 'w') as f:
            f.write(content)

        os.system('cd {}; git add .; git commit -m "update"; git push origin master'.format(
            config.REPO_PATH))

    return

def ensure_credentials(namespace, variables):
    credential = get_credential(namespace)

    if not credential:
        credential = {}

        for variable in variables:
            credential[variable] = input('{} = '.format(
                variable
            ))

        if all(credential.values()):
            set_credential(
                namespace,
                credential)
            return credential
        else:
            raise Exception('Some of the credentials were  not set.')
    else:
        return credential

def load_session_data(namespace):
    session_path = os.path.join(config.SESSIONS_DIR, namespace)
    if os.path.exists(session_path):
        session_data = json.load(open(session_path, 'r'))
        return session_data


def save_session_data(namespace, session_data):
    session_path = os.path.join(config.SESSIONS_DIR, namespace)
    json.dump(session_data, open(session_path, 'w'))
