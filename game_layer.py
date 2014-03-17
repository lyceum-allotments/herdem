#!/usr/bin/env python

import cocos
import sheep
from cocos.actions import *
import c_handlers
import pyglet
import pymunk as pm
from pymunk import Vec2d
import math, sys, random
from bg_layer import *
from cocos.menu import *
from cocos.scene import *
from cocos.scenes import *
from cocos.layer import *


#sheep_speed = 80   
class GameLayer(cocos.layer.Layer):
    
    #remove space default value
    def __init__(self, controller, space = ""):
        super(GameLayer, self).__init__()
        director = cocos.director.director
        xwin, ywin = director.get_window_size()
        
        self.controller = controller 
        self.total_sheep = 5 + controller.number

        self.saved_sheeps = 0
        self.lost_sheeps = 0
        self.setup_labels()

        self.space = controller.space
        static_body = pm.Body()
        static_lines = [pm.Segment(static_body, (xwin*0, ywin*0), (xwin*0, ywin*1), 0.0)
                        ,pm.Segment(static_body, (xwin*0, ywin*1), (xwin*1, ywin*1), 0.0)
                        ,pm.Segment(static_body, (xwin*1, ywin*1), (xwin*1, ywin*0), 0.0)
                        ,pm.Segment(static_body, (xwin*1, ywin*0), (xwin*0, ywin*0), 0.0)
                        ] 

        for line in static_lines:
            line.elasticity = 0.95
        #self.space.add(static_lines)


    def setup_labels(self):
        director = cocos.director.director
        xwin, ywin = director.get_window_size()
        
        label_string = "Sheeps saved: %i / %i" % (self.controller.saved_sheeps,self.controller.total_sheep)
        self.saved_label = cocos.text.Label(label_string,
                                  font_name = 'fonts/LithosPro-Bold.otf',
                                  font_size = 32,
                                  anchor_x='left', anchor_y ='top')
        

        self.saved_label.position = 0,ywin
        self.saved_label.element.color = (0,0,0,255)
        self.add(self.saved_label, z= 2)


        lost_string = "Sheeps eaten: %i / %i" % (self.controller.lost_sheeps,self.controller.total_sheep)
        self.lost_label = cocos.text.Label(lost_string,
                                  font_name = 'fonts/LithosPro-Bold.otf',
                                  font_size = 32,
                                  anchor_x='right', anchor_y ='top')
        

        self.lost_label.position = xwin,ywin #ywin-32
        self.lost_label.element.color = (0,0,0,255)
        self.add(self.lost_label, z= 2)
        
    def reset(self):
        self.saved_label.element.text = "Sheeps saved: 0 / 0"
        self.lost_label.element.text = "Sheeps eaten: 0 / 0"
