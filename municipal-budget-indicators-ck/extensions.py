import dataclasses
import json
import os
import sys
from decimal import Decimal

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)

indicator_limits = {
    'VPCP': [0.9, 0.8],
    'RS': [0, -0],
    'CPBR': [0.0, -0.0, -0.0],
    'SBR': [0.25, 0, 0],
    'BUKBV': [4, 1],
    'BUKBP': [0.3, 0.08],
    'KVBP': [0, 1.0, 1.2],
    'URM': [1.2, 1.0, 0],
    'IA': [0.20, 0.10, 0],
    'KSKV': [0.98, 0.75, 0],
    'SKR': [0.0, -0.0, 0.0],
    'KPIT': [0.5, 0.25, 0],
    'KVSBR': [0.0, 0.0, 0.0],
    'CDSBR': [0, 3, 6],
    'DSSBR': [0, 0.4, 0.8],
    'PUSBR': [0, 0.04, 0.08],
    'DSC': [0.0, 0.2, 0.3],
    'KDS': [1.2, 1.0, 0.0],
    'CZCA': [0.0, 0.1, 0.25],
    'CZCA1': [0.0, 0.1, 0.25],
    'CL': [5, 1],
    'OL': [1.75, 1],
    'FZ': [0.5, 0.05],
}

# https://stackoverflow.com/questions/51060894/adding-a-data-file-in-pyinstaller-using-the-onefile-option
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path) 
