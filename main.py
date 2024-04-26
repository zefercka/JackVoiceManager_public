# -*- coding: utf8 -*-

import config
import design
import logger
from execute_command import set_logger, set_calendar, ntn

if __name__ == "__main__":
    try:
        logger.log = logger.Logger()
        set_logger(logger.log)

        config.configfile = config.ConfigFile()
        # UC.command_file = UC.CommandFile()
        # set_calendar()
        design.start()

    except Exception as err:
        print(err)
    finally:
        config.configfile.save()
        logger.log.close()
        ntn.stopped = 1
        # UC.command_file.save()