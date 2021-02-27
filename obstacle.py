import pygame

from vector import *
from sprite import *


class Obstacle:
    __sprite_sheet = 0
    
    __position = Vector()
    __dimension = Vector()
    
    __collider = 0

    __on_collide = 0
    
    def __init__(self, sprite_sheet, position, dimension, collider, on_collide):
        self.__sprite_sheet = sprite_sheet
        
        self.__position = position
        self.__dimension = dimension
        
        self.__collider = collider

        self.__on_collide = on_collide
    
    def render(self, surface, offset=Vector()):
        self.__sprite_sheet.update(2)
        self.__sprite_sheet.render(surface,
                                   Vector(self.__position.get_x() - offset.get_x(),
                                          self.__position.get_y() - offset.get_y()))

    def get_collider(self):
        return self.__collider

    def get_on_collide(self):
        return self.__on_collide

    def get_sprite_sheet(self):
        return self.__sprite_sheet
