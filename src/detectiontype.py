from enum import Enum


class DetectionType(Enum):
    DISPLAY = "Display"
    TEXT = "Text"

class DetectionPreference:
    def __init__(self, type: str, value: str):
        self.type = type
        self.value = value