import json
from typing import Dict
from datetime import datetime as dt

class Utils:
    def __init__(self):
        pass

    def loadDatas(self) -> Dict[str, str]:
        with open("db_config.json", "r") as json_file:
            return json.loads(json_file.read())

    def hasAccount(self, id, datas):
        for raw in datas:
            if id in raw:
                return True
        return False
