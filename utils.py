import json
from typing import Dict
from datetime import datetime as dt

class Utils:
    def __init__(self):
        self.logs = open('logs.txt', 'w')
        pass

    def loadDatas(self) -> Dict[str, str]:
        with open("db_config.json", "r") as json_file:
            return json.loads(json_file.read())

    def writeLogs(self, message: str):
        self.logs.write(f"[{dt.now()}] {str} \n")
