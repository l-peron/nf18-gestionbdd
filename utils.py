import json
from typing import Dict
from datetime import datetime as dt


class Utils:
    def __init__(self):
        self.logs = open("logs.log", "a")
        pass

    def loadDatas(self) -> Dict[str, str]:
        with open("db_config.json", "r") as json_file:
            return json.loads(json_file.read())

    def writeLogs(self, message: str):
        log = f"[{dt.now()}] {message} \n"
        print(log)
        self.logs.write(log)

    def close(self):
        self.logs.close()
