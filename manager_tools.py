
import os

def logs_autoclear():
    try:
        sz = os.path.getsize("logs.log")
        if int(sz) > 1024 * 1024 * 10: # 10 MB
            os.remove("logs.log")
    except FileNotFoundError:
        pass
