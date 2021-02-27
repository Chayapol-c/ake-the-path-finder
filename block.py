import pygame

from vector import *
from sprite import *

class Block:
    __sprite = 0
    __position = Vector()
    __dimension = Vector()
    __collider = 0

    __on_collide = 0
    
    def __init__(self, sprite, position, dimension, on_collide):
        self.__sprite = sprite.get_image()
        self.__sprite = pygame.transform.scale(self.__sprite, (dimension.get_x(), dimension.get_y()))
        
        self.__position = position
        self.__dimension = dimension

        self.__collider = pygame.Rect(position.get_x(), position.get_y(), dimension.get_x(), dimension.get_y())

        self.__on_collide = on_collide
    
    def render(self, surface, offset=Vector()):
        surface.blit(self.__sprite, (self.__position.get_x() - offset.get_x(), self.__position.get_y() - offset.get_y()))

    def set_position(self, position):
        self.__position = position

    def get_collider(self):
        return self.__collider

    def get_on_collide(self):
        return self.__on_collide
