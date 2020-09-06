import time
import random
from pprint import pprint
from scipy import spatial

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

#pprint(testblock.__dict__)

def detect_collision(block: FormData, otherblock: FormData):
    # southeast
    if (block.pos.x >= otherblock.pos.x and 
        block.pos.x <= otherblock.pos.x + otherblock.size.width -1):

        if block.posbef.x >= otherblock.pos.x + otherblock.size.width:
            #print("Opax")
            block.pos.x = otherblock.pos.x + otherblock.size.width
        
        if block.posbef.x + block.size.width <= otherblock.pos.x:
            #print("Opax")
            block.pos.x = otherblock.pos.x - otherblock.size.width

        if (block.pos.y >= otherblock.pos.y and 
            block.pos.y <= otherblock.pos.y + otherblock.size.height -1):
            
            if block.posbef.y >= otherblock.pos.y + otherblock.size.height:
                #print("Opay")
                block.pos.y = otherblock.pos.y + otherblock.size.height

        if (block.pos.y + block.size.height >= otherblock.pos.y +1 and 
            block.pos.y <= otherblock.pos.y):

            if block.posbef.y + block.size.height <= otherblock.pos.y + block.poschange.y + 1:
                #print("Opay")
                block.pos.y = otherblock.pos.y - block.size.height
                block.is_free_falling = False

    # southwest
    if (block.pos.x <= otherblock.pos.x and 
        block.pos.x + block.size.width >= otherblock.pos.x +1):

        if block.posbef.x + block.size.width <= otherblock.pos.x:
            #print("Opax")
            block.pos.x = otherblock.pos.x - otherblock.size.width
        
        if block.posbef.x + block.size.width <= otherblock.pos.x:
            #print("Opax")
            block.pos.x = otherblock.pos.x - otherblock.size.width

        if (block.pos.y >= otherblock.pos.y and 
            block.pos.y <= otherblock.pos.y + otherblock.size.height -1):
        
            if block.posbef.y >= otherblock.pos.y + otherblock.size.height:
                #print("Opay")
                block.pos.y = otherblock.pos.y + otherblock.size.height

        if (block.pos.y + block.size.height >= otherblock.pos.y +1 and 
            block.pos.y <= otherblock.pos.y):

            if block.posbef.y + block.size.height <= otherblock.pos.y + block.poschange.y + 1:
                #print("Opay")
                block.pos.y = otherblock.pos.y - block.size.height
                block.is_free_falling = False


A = [[451,222], [876,123], [1002,600], [222,451]]
tree = spatial.KDTree(A)
print(tree.__dict__)
print(tree.query([400,200], 2))