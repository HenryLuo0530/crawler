import os
import logging
from logging.handlers import RotatingFileHandler

def log_setup():
    if os.path.exists("./log.log"):
        os.replace("log.log", "last_log.log")
    
    handler = RotatingFileHandler(
        filename="log.log",
        mode='a',
        maxBytes=1024 * 2,
        backupCount=0,
        encoding='utf-8',
        delay=False
    )
    handler.setLevel(logging.INFO)
    logging.basicConfig(
        format="%(name)s %(asctime)s %(levelname)s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[handler]
    )
    return

def check_shutdown(logger: logging.Logger) -> bool:
    is_normal_shutdown: bool
    if os.path.exists("./last_log.log"):
        with open("./last_log.log", "r", encoding="utf-8") as log_file:
            for line in log_file:
                pass
            last_log = line
            if "[I] Bot has been shutted down" in last_log:
                is_normal_shutdown = True
            else:
                is_normal_shutdown = False
    else:
        logger.warning("[W] last_log not found")
        is_normal_shutdown = True
    return is_normal_shutdown