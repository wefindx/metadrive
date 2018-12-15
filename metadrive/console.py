import requests
import IPython
from traitlets.config import Config


def repl(host=None, port=None):

    def get(url):
        response = requests.get(
            'http://{host}:{port}/address'.format(host=host, port=port),
            params={'url': url}
        )
        if response.ok:
            return response.json()

    def list(url):
        response = requests.get(
            'http://{host}:{port}/sites'.format(host=host, port=port)
        )
        if response.ok:
            return response.json()
        else:
            return []

    def update(url):
        response = requests.get(
            'http://{host}:{port}/index'.format(host=host, port=port)
        )
        if response.ok:
            return response.json()
        else:
            return []

    IPython.embed(
        banner1="[http://{}:{}] Welcome to MetaDrive - A Web Driver.\n".format(host, port),
        banner2=":get('https://example.com')   -- retrieves website\n:list()                       -- lists available websites\n:update()                     -- refreshes the list of available websites\n",
        exit_msg="Bye~",
        config = Config({
            'TerminalIPythonApp': {'display_banner': False},
            'InteractiveShellApp': {'log_level': 20},
            'InteractiveShell': {
                'autoindent': True,
                'colors': 'LightBG',
                'confirm_exit': False,
                'deep_reload': True,
                'editor': 'vi',
                'xmode': 'Context'},
            'PrefilterManager': {'multi_line_specials': True},
            'AliasManager': {'user_aliases': [('la', 'ls -al')]}
        })
    )

if __name__ == "__main__":
    repl(host='0.0.0.0', port=8000)
