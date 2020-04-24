import time
import random
from pprint import pprint

class FormDataPosition:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
class FormDataSize:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

class FormData:
    def __init__(self, name: str, pos: FormDataPosition, size: FormDataSize, center: FormDataPosition, color: tuple):
        self.name = name
        self.pos = pos
        self.size = size
        self.center = center
        self.color = color
  

testblock = FormData("Xunda", FormDataPosition(100, 100), FormDataSize(100, 100), FormDataPosition(100, 100), (0,0,0))

pprint(testblock.__dict__)