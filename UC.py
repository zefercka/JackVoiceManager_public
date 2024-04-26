import configparser
import os
import re


class CommandFile:
    def __init__(self):
        self.command = configparser.ConfigParser()
        if not os.path.exists("command.ini"):
            # import winapps
            self.command.add_section("UserCommand")

            # co = {
            #     "Google Chrome": ("открой chrome", ""),
            #     "Adobe Photoshop": ("открой photoshop"),
            #     "Steam": ("открой steam"),
            #     "Epic Games Launcher": ("открой epic games"),
            #     "Adobe Audition": ("открой audition"),
            #     "Audacity": ("открой audacity"),
            #     "Adobe After Effects": ("открой after effects"),
            #     "AnyDesk": ("открой anydesk"),
            #     "Wallpaper Engine": ("открой wallpaper engine"),
            #     "Mozilla Firefox": ("открой firefox"),
            #     "Movavi Video Suite": ("открой movavi"),
            # }
            #
            # for app in winapps.list_installed():
            #     n = re.sub(r'\([^()]*\)', '', app.name)
            #     n = re.sub(r'[^\w\s]+|[\d]+', '', n).strip()
            #
            #     if n in co:
            #         print(app)
            #         self.command.set("UserCommand", co[n], app.modify_path)

            with open("command.ini", "w") as cf:
                self.command.write(cf)
                cf.close()

        else:
            with open("command.ini", "r") as cf:

                self.command.read_file(cf)
                try:
                    commands_file = self.command.items("UserCommand")
                    for item in commands_file:
                        try:
                            commands[item[0]] = item[1]
                        except:
                            continue
                    cf.close()
                except:
                    self.command.add_section("UserCommand")
                    cf.close()

    def save(self):
        self.command = configparser.ConfigParser()
        self.command.add_section("UserCommand")

        for item in commands.items():
            self.command.set("UserCommand", item[0], item[1])

        with open("command.ini", "w") as cf:
            self.command.write(cf)
            cf.close()


commands = dict()
command_file = None
