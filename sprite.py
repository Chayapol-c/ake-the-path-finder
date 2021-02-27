import pygame
import os

from vector import *

class Sprite:
    __image = 0
    __path = 0

    def __init__(self, path):
        self.__path = path
        self.__image = pygame.image.load(os.path.join(path))

    def set_scale(self, dimension):
        self.__image = pygame.transform.scale(self.__image, (dimension.get_x(), dimension.get_y()))
    
    def get_image(self):
        return self.__image
    def set_image(self, image):
        self.__image = image

class Sprite_sheet:
    __path = 0
    __image = 0
    __dimension = Vector()
    __count = 0
    
    __timer = 0
    __current_index = 0
    __interval = 0
    
    def __init__(self, path, dimension, count, interval):
        self.__path = path
        self.__image = pygame.image.load(os.path.join(path))
        self.__dimension = dimension
        self.__count = count
        
        self.__interval = interval

    def set_scale(self, scale=Vector()):
        self.__image = pygame.transform.scale(self.__image, (scale.get_x() * self.__count,
                                                             scale.get_x()))
        self.__dimension = scale
    
    def update(self, speed):
        self.__timer += speed / 5

        if self.__timer >= self.__interval:
            self.__current_index += 1
            self.__timer = 0

        if self.__current_index >= self.__count:
            self.__current_index = 0

    def render(self, surface, position=Vector()):
        surface.blit(self.__image, position.get_tuple(), (self.__current_index * self.__dimension.get_x(),
                                                          0,
                                                          self.__dimension.get_x(),
                                                          self.__dimension.get_y()
                                                          ))
    def get_image(self):
        return self.__image
    def set_image(self, image):
        self.__image = image

    def get_current_index(self):
        return self.__current_index
    def set_current_index(self, index):
        self.__current_index = index
