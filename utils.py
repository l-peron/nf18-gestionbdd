import json
from typing import Dict

class Utils:
    def __init__(self):
        pass

    def loadDatas(self) -> Dict[str, str]:
        with open("db_config.json", "r") as json_file:
            return json.loads(json_file.read())
