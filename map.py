import numpy as np
import random

# Tile size
from settings import *


min_room_size = 8

class Tile:
    def __init__(self, blocked, visible=None):
        self.blocked = blocked
        if visible is None:
            visible = blocked
        self.visible = False
        self.explored= False

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = self.initialize_map()

    def initialize_map(self):
        return np.array([[Tile(True) for _ in range(self.width)] for _ in range(self.height)])
    def random_initialize_map(self):
        # Rastgele bir harita oluştur (1 = engel, 0 = boş alan)
        return np.array([[Tile(random.choice([True, False])) for _ in range(self.width)] for _ in range(self.height)])
    

    def is_blocked(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return True
        return self.map[y][x].blocked  # type: ignore
    
    def set_block(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.map[y][x].blocked = True # type: ignore

    def set_unblock(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.map[y][x].blocked = False # type: ignore



    # def create_room(self, room):
    #     for y in range(room.top, room.bottom):
    #         for x in range(room.left, room.right):
    #             if x < self.width and y < self.height:  # Ensure within bounds
    #                 self.map[y][x].blocked = False
    #                 self.map[y][x].visible = False

        



    # Temporary create_room for creating FOV
    def create_room(self, room, wall_probability=0.2):
        for y in range(room.top, room.bottom):
            for x in range(room.left, room.right):
                if x < self.width and y < self.height:  # Ensure within bounds
                    if random.random() < wall_probability:
                        self.map[y][x].blocked = True
                        self.map[y][x].visible = True
                    else:
                        self.map[y][x].blocked = False
                        self.map[y][x].visible = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if x < self.width and y < self.height:  # Ensure within bounds
                lst_tmp = []
                lst_tmp.append(x)
                new_x = int(random.choice(lst_tmp))
                self.map[y][new_x].blocked = False
                self.map[y][new_x].visible = False
    
    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if x < self.width and y < self.height:  # Ensure within bounds
                lst_tmp = []
                lst_tmp.append(y)
                new_y = int(random.choice(lst_tmp))
                self.map[new_y][x].blocked = False
                self.map[new_y][x].visible = False

class Room:
    def __init__(self, x, y, width, height):
        self.left = x
        self.right = x + width
        self.top = y
        self.bottom = y + height

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top
    
    @property
    def center(self):
        center_x = (self.left + self.right) // 2
        center_y = (self.top + self.bottom) // 2
        return center_x, center_y

    def split(self):
        if self.width <= min_room_size * 2 and self.height <= min_room_size * 2:
            return None, None
        
        if self.width > self.height:
            split_direction = 'vertical'
        elif self.height > self.width:
            split_direction = 'horizontal'
        else:
            split_direction = random.choice(['horizontal', 'vertical'])
        if split_direction == 'horizontal':
            split_point = random.randint(self.top + min_room_size, self.bottom - min_room_size)
            left_room = Room(self.left, self.top, self.width, split_point - self.top)
            right_room = Room(self.left, split_point, self.width, self.bottom - split_point)
        else:
            split_point = random.randint(self.left + min_room_size, self.right - min_room_size)
            left_room = Room(self.left, self.top, split_point - self.left, self.height)
            right_room = Room(split_point, self.top, self.right - split_point, self.height)

        return left_room, right_room

class BSPNode:
    def __init__(self, room):
        self.room = room
        self.left = None
        self.right = None

    def is_leaf(self):
        return self.left is None and self.right is None
    
    def build_tree(self, min_size=min_room_size):
        if self.room.width > min_size * 2 and self.room.height > min_size * 2:
            left_room, right_room = self.room.split()
            if left_room and right_room:
                self.left = BSPNode(left_room)
                self.right = BSPNode(right_room)
                self.left.build_tree(min_size)
                self.right.build_tree(min_size)

    def create_blocks(self, node, map):
        room_width = random.randint(min_room_size, node.room.width)
        room_height = random.randint(min_room_size, node.room.height)
        room_x = random.randint(node.room.left, node.room.left + node.room.width - room_width)
        room_y = random.randint(node.room.top, node.room.top + node.room.height - room_height)
        room_temp = Room(room_x, room_y, room_width, room_height)
        map.create_room(room_temp)

    def create_dungeon(self, map):
        if self.is_leaf():
            new_room = Room(self.room.left +1, self.room.top+1, self.room.width- random.randint(1,4) , self.room.height-random.randint(1,4))
            map.create_room(new_room)
        else:
            if self.left:
                self.left.create_dungeon(map)
            if self.right:
                self.right.create_dungeon(map)
            if self.left and self.right:
                self.connect_rooms(map, self.left.room.center, self.right.room.center)


    def connect_rooms(self, map, left_center, right_center):
        x1, y1 = left_center
        x2, y2 = right_center

        if random.random() < 0.5:
            # First move horizontally, then vertically
            map.create_h_tunnel(x1, x2, y1)
            map.create_v_tunnel(y1, y2, x2)
        else:
            # First move vertically, then horizontally
            map.create_v_tunnel(y1, y2, x1)
            map.create_h_tunnel(x1, x2, y2)