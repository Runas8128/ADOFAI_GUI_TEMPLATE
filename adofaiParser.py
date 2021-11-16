from typing import Callable

import json
from parseHelper import *

def run(
    fileName: str,
    # Your needed arguments...
    logger: Callable[[str], None]):

    logger("Loading Map file")
    
    with open(fileName, 'r', encoding='utf-8-sig') as adofaiFile:
        rawString = adofaiFile.read()\
                .replace(',\n}\n', '\n}\n')\
                .replace(',\n}', '\n}')\
                .replace(', }', '}')\
                .replace(',,', ',')
        Map: MapType = json.loads(rawString)
    
    logger("Your Runner step")

    # TODO: build your steps
    
    logger("Make and Dump new map")
    
    newMap = Map
    with open(fileName[:-7] + '_Filtered.adofai', 'w', encoding='utf-8-sig') as newFile:
        json.dump(newMap, newFile, indent=4)
