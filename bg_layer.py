#!/usr/bin/env python

import cocos
from cocos.actions import *
import pymunk as pm
from pymunk import Vec2d
import math, sys, random
from constants import *

class BGLayer(cocos.layer.Layer):

    def __init__(self, levelNum, controller):
        super(BGLayer, self).__init__()
        self.max_levelNum = 1
        
        director = cocos.director.director
        xwin, ywin = director.get_window_size()

        if levelNum == "title":
            ttl = cocos.sprite.Sprite("levelNums/title.png")
            ttl.x = xwin / 2  
            ttl.y = ywin / 2
            self.add(ttl)
            return

        if levelNum >= self.max_levelNum:
            self.levelNum = self.max_levelNum
        else:
            self.levelNum = levelNum
        print "levelNum is .. %d" % levelNum
        self.controller = controller
        self.wall_list = ["wall_end_br", "wall_end_tr", "wall_bl",
                          "wall_b", "wall_br", "wall_end_bl", "wall_end_tl",
                          "wall_l", "wall_r", "wall_end_rb", "wall_end_lb",
                          "wall_tl", "wall_t", "wall_tr", "wall_end_rt",
                          "wall_end_lt"]


        

        self.level_paths = ["levels/level0.xml", "levels/level1.xml"]
        
        bg = cocos.tiles.load(self.level_paths[self.levelNum])['map0']

        map_tw = len(bg.cells)
        map_th = len(bg.cells[0])

        for i in range(map_tw): #bg.cells:
            for j in range(map_th):
                # Adding the fence tiles to the static collision manager
                if bg.cells[i][j].tile.id in self.wall_list:
                    add_ctile(bg.cells[i][j], coll_types["wall"], controller.space)

                                        
                    

        bg.set_view(0, 0, xwin, ywin) 
        self.add(bg)

        level_string = "Level: %i" % levelNum
        self.level_label = cocos.text.Label(level_string,
                                  font_name = 'fonts/LithosPro-Bold.otf',
                                  font_size = 32,
                                  anchor_x='left', anchor_y ='bottom')
        

        self.level_label.position = 0,0
        self.level_label.element.color = (0,0,0,255)
        self.add(self.level_label, z= 2)


def add_ctile(cell, coll_type, space):
    verts = [(cell.x, cell.y),
             (cell.x + cell.width, cell.y),
             (cell.x + cell.width, cell.y + cell.height),
             (cell.x, cell.y + cell.height)]
    
    body = pm.Body()
    shape = pm.Poly(body, verts, (0,0),auto_order_vertices=True) 
    
    shape.collision_type = coll_type 
    shape.elasticity = 1.0
    shape.parent = cell
    
    space.add(shape)
    return

