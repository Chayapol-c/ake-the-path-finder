import pygame

class Vector:
    __x = 0
    __y = 0

    def __init__(self, x=0, y=0):
        self.__x = x
        self.__y = y

    def add(self, other):
        self.__x += other.get_x()
        self.__y += other.get_y()

    def add_x(self, magnitude):
        self.__x += magnitude

    def add_y(self, magnitude):
        self.__y += magnitude
    
    def multiply(self, magnitude):
        self.__x *= magnitude
        self.__y *= magnitude

    def multiply_x(self, magnitude):
        self.__x *= magnitude

    def multiply_y(self, magnitude):
        self.__y *= magnitude
    
    def get_magnitude(self):
        return ((self.__x ** 2) + (self.__y ** 2)) ** 0.5
    
    def normalize(self):
        magnitude = self.get_magnitude()
        if magnitude != 0:
            self.__x /= magnitude
            self.__y /= magnitude
        else:
            self.__x = 0
            self.__y = -1

    def set_magnitude(self, magnitude):
        self.normalize()
        self.multiply(magnitude)
    
    def limit_magnitude(self, magnitude):
        if self.get_magnitude() > magnitude:
            self.set_magnitude(magnitude)

    def limit_x(self, magnitude):
        sign = 1
        if self.__x < 0:
            sign = -1
        if abs(self.__x) > magnitude:
            self.__x = magnitude * sign

    def limit_y(self, magnitude):
        sign = 1
        if self.__y < 0:
            sign = -1
        if abs(self.__y) > magnitude:
            self.__y = magnitude * sign
    
    def get_tuple(self):
        return (int(self.__x), int(self.__y))

    def set_x(self, x):
        self.__x = x
    
    def get_x(self):
        return self.__x

    def set_y(self, y):
        self.__y = y

    def get_y(self):
        return self.__y
