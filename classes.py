import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Block:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id

    