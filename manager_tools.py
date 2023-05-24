import logging
import os

def logs_autoclear():
    try:
        sz = os.path.getsize("logs.log")
        if int(sz) > 1024 * 1024 * 10: # 10 MB
            os.remove("logs.log")
    except FileNotFoundError:
        pass


class Logger:
    
    def __init__(self, name) -> None:
        file = 'logs.log'
        logging.basicConfig(
            filename=file,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filemode='a'
        )
        self.logger = logging.getLogger(name=name)
        self.logger.setLevel(logging.DEBUG)
    
    def get_logger(self):
        return self.logger