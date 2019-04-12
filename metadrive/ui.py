import os
import imp

from metadrive.config import (
    INSTALLED,
    CONSOLE_HOST,
    CONSOLE_PORT,
)

class NCurses:

    def run(self):

        import npyscreen

        class NCurse(npyscreen.NPSApp):

            def main(self):

                F  = npyscreen.Form(name = "Welcome to MetaDrive!",)
                t  = F.add(npyscreen.TitleText, name = "URL:",)
                ml = F.add(npyscreen.MultiLineEdit,
                       value = """data output goes here...\n""",
                       max_height=45, rely=9)

                # This lets the user interact with the Form.
                F.edit()

        NCurse().run()


class ReactJS:

    def __init__(self):
        self.path = os.path.join(INSTALLED, '_ui_scripts')

        if self.path == 'metadrive':
            self.path = os.getcwd()

    def build(self):

        if not os.path.exists('{path}/.env'.format(path=self.path)):
            with open('{path}/.env'.format(path=self.path), 'w') as f:
                f.write(
                    'REACT_APP_API_SERVER=http://{host}:{port}'.format(
                        host=CONSOLE_HOST,
                        port=CONSOLE_PORT
                    )
                )


        if 'node_modules' in os.listdir(self.path):
            os.system('rm -rf {path}/node_modules && yarn install'.format(self.path))
        else:
            os.system('cd {path} && yarn install'.format(path=self.path))

    def start(self):

        if 'node_modules' in os.listdir(self.path):
            os.system('cd {path} && yarn start'.format(path=self.path))
        else:
            self.build()
            os.system('cd {path} && yarn start'.format(path=self.path))

