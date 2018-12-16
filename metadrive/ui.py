import os
import imp
import npyscreen

INSTALLED = imp.find_module('metadrive')[1]

class ReactJS:

    def __init__(self):
        self.path = os.path.join(INSTALLED, '_react')

        if self.path == 'metadrive':
            self.path = os.getcwd()

    def build():

        if 'node_modules' in os.listdir(path):
            os.system('rm -rf {path}/node_modules && yarn install'.format(self.path))
        else:
            os.system('cd {path} && yarn install'.format(path=self.path))

    def start():

        if 'node_modules' in os.listdir(path):
            os.system('cd {path} && yarn start'.format(path=self.path))
        else:
            build()
            os.system('cd {path} && yarn start'.format(path=self.path))



class NCurses(npyscreen.NPSApp):

    def main(self):
        F  = npyscreen.Form(name = "Welcome to Npyscreen",)
        t  = F.add(npyscreen.TitleText, name = "Text:",)
        fn = F.add(npyscreen.TitleFilename, name = "Filename:")
        fn2 = F.add(npyscreen.TitleFilenameCombo, name="Filename2:")
        dt = F.add(npyscreen.TitleDateCombo, name = "Date:")
        s  = F.add(npyscreen.TitleSlider, out_of=12, name = "Slider")
        ml = F.add(npyscreen.MultiLineEdit,
               value = """try typing here!\nMutiline text, press ^R to reformat.\n""",
               max_height=5, rely=9)
        ms = F.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Pick One",
                values = ["Option1","Option2","Option3"], scroll_exit=True)
        ms2= F.add(npyscreen.TitleMultiSelect, max_height =-2, value = [1,], name="Pick Several",
                values = ["Option1","Option2","Option3"], scroll_exit=True)

        # This lets the user interact with the Form.
        F.edit()

        print(ms.get_selected_objects())
