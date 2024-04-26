from datetime import datetime


class Logger:
    def __init__(self):
        self.logger = open(f"logs/LOG-{datetime.now().strftime('%d-%m-%Y')}.log", "a")

    def write(self, file, func, status, err=None, type_=None, inf=None):
        if type_ is None:
            if status:
                self.logger.write(f"{datetime.now().strftime('%H:%M:%S')} - [INFO] {file}: {func} - Successful \n")
            else:
                self.logger.write(f"{datetime.now().strftime('%H:%M:%S')} - [ERROR] {file}: {func} - {err} \n")
        else:
            self.logger.write(f"{datetime.now().strftime('%H:%M:%S')} - [{type_}] {file}: {func} - {inf} \n")

    def close(self):
        self.logger.close()


log = None
