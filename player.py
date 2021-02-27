import pygame

from vector import *
from sprite import *

class Player:
    __position = Vector()
    __velocity = Vector()
    __acceleration = Vector()


    __movement_state = 0
    __sprite_sheet_dict = {}
    __dimension = 0

    __collider = 0
    
    __collider_top = 0
    __collider_buttom = 0
    __collider_left = 0
    __collider_right = 0

    __walking_force = 1
    __max_speed = 9
    __friction = 0.7

    __jumping_force = 30
    __is_on_ground = False
    
    __is_walking = False

    __won = False
    __dead = False
    
    def __init__(self, sprite_sheet_dict, position=Vector(), dimension=Vector()):
        self.__sprite_sheet_dict = sprite_sheet_dict
        self.__dimension = dimension
        self.__position = position

        self.update_collider()

    def apply_force(self, force=Vector()):
        self.__acceleration.add(force)
    
    def update_collider(self):
        self.__collider = pygame.Rect(self.__position.get_x(), self.__position.get_y(),
                                      self.__dimension.get_x(), self.__dimension.get_y())
        self.__collider_top = pygame.Rect(self.__position.get_x() + 10, self.__position.get_y(),
                                          self.__dimension.get_x() - 20, 10)
        self.__collider_buttom = pygame.Rect(self.__position.get_x() + 10, self.__position.get_y() + self.__dimension.get_y() - 10,
                                             self.__dimension.get_x() - 20, 10)
        self.__collider_left = pygame.Rect(self.__position.get_x(), self.__position.get_y() + 10,
                                           10, self.__dimension.get_y() - 20)
        self.__collider_right = pygame.Rect(self.__position.get_x() + self.__dimension.get_x() - 10, self.__position.get_y() + 10,
                                            10, self.__dimension.get_y() - 20)
    
    def collide(self, map_list):
        for row in range(0, len(map_list)):
            for column in range(0, len(map_list[row])):
                if map_list[row][column] != 0:
                    if map_list[row][column].get_on_collide() == "COLLIDE":
                        # collide ground
                        while self.__collider_buttom.colliderect(map_list[row][column].get_collider()):
                            self.__position.add(Vector(0, -1))
                            self.update_collider()
                            self.__velocity.set_y(0)
                            self.__is_on_ground = True
                        # collide top
                        while self.__collider_top.colliderect(map_list[row][column].get_collider()):
                            self.__position.add(Vector(0, 1))
                            self.update_collider()
                            self.__velocity.set_y(0)
                        # collide left
                        while self.__collider_left.colliderect(map_list[row][column].get_collider()):
                            self.__position.add(Vector(1, 0))
                            self.update_collider()
                            self.__velocity.set_x(0)
                        # collide right
                        while self.__collider_right.colliderect(map_list[row][column].get_collider()):
                            self.__position.add(Vector(-1, 0))
                            self.update_collider()
                            self.__velocity.set_x(0)
                    elif map_list[row][column].get_on_collide() == "GAME OVER":
                        if self.__collider.colliderect(map_list[row][column].get_collider()):
                            self.__dead = True
                    elif map_list[row][column].get_on_collide() == "WIN":
                        if self.__collider.colliderect(map_list[row][column].get_collider()):
                            self.__won = True
    
    def update(self, input_dict):
        self.apply_force(Vector(0, 2))

        # walk
        if input_dict["LEFT"]:
            self.apply_force(Vector(-self.__walking_force, 0))
            self.__is_walking = True
        if input_dict["RIGHT"]:
            self.apply_force(Vector(self.__walking_force, 0))
            self.__is_walking = True
        # jump
        if input_dict["UP"] and self.__is_on_ground:
            self.__velocity.add_y(-self.__jumping_force)

        # friction
        if not self.__is_walking:
            self.__velocity.multiply_x(self.__friction)
        if self.__velocity.get_magnitude() < 0.02:
            self.__velocity.set_magnitude(0)
        self.__is_walking = False

        # update position
        self.__velocity.add(self.__acceleration)
        self.__velocity.limit_x(self.__max_speed)
        self.__position.add(self.__velocity)
        
        self.update_collider()

        # update walking direction
        if abs(self.__velocity.get_x()) < 0.1 and self.__is_on_ground:
            self.__movement_state = "IDLE"
        elif self.__velocity.get_x() >= 0 and self.__is_on_ground:
            self.__movement_state = "WALKING RIGHT"
        elif self.__velocity.get_x() < 0 and self.__is_on_ground:
            self.__movement_state = "WALKING LEFT"
        elif abs(self.__velocity.get_x()) < 0.1:
            self.__movement_state = "JUMPING FRONT"
        elif self.__velocity.get_x() >= 0:
            self.__movement_state = "JUMPING RIGHT"
        else:
            self.__movement_state = "JUMPING LEFT"
        self.__is_on_ground = False
        
        self.__acceleration.set_magnitude(0)

    def render(self, surface, offset=Vector()):
        if self.__movement_state != 0:
            self.__sprite_sheet_dict[self.__movement_state].update(abs(self.__velocity.get_x()))
            self.__sprite_sheet_dict[self.__movement_state].render(surface, Vector(self.__position.get_x() - offset.get_x(), self.__position.get_y() - offset.get_y()))
        
    def get_position(self):
        return self.__position

    def get_velocity(self):
        return self.__velocity
    def set_velocity(self, velocity):
        self.__velocity = velocity

    def get_dead(self):
        return self.__dead

    def get_won(self):
        return self.__won
