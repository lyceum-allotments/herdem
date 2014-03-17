#!/usr/bin/env python

import cocos
from cocos.actions import *
import cocos.collision_model as cm

import pymunk as pm
from pymunk import Vec2d
import math, sys, random
from constants import *
import constants
import herdem_move as hm
import pyglet
import animated_sprite as asp

wolf_speed = 40
class WolfSprite(asp.AnimatedSprite):

    def __init__(self, controller):
        image_file = {"still" : pyglet.image.load("images/wolf.png"),
                      "go"    : pyglet.image.load("images/wolf.png")}

        super(WolfSprite, self).__init__(image_file)
        self.space = controller.space

        director = cocos.director.director
        xwin, ywin = director.get_window_size()
        self.speed = wolf_speed
        self.position = cocos.euclid.Vector2(random.uniform(xwin*0.1,xwin*0.2),random.uniform(ywin*0.8,ywin*0.85))
        self.old_position = self.position 
        
        # Set chipmunk body and shape properties
        mass = 10
        radius = 40
        inertia = pm.moment_for_circle(mass, 0, radius, (0,0))
        
        self.body = pm.Body(mass, inertia)
        self.body.position = self.position
       
        velx = random.uniform(0,wolf_speed)*random.choice([-1,1])
        vely = random.uniform(0,wolf_speed)*random.choice([-1,1])
        self.velocity = (0,0)
        
        self.body.velocity = (velx,vely)
        self.shape = pm.Circle(self.body, 40, (0,0))
        self.shape.elasticity = 0.95
        self.shape.collision_type = coll_types['wolf']
        
        #Add the wolf to the chipmunk space
        self.space.add(self.body, self.shape)

        #Random move of wolf
        self.do(hm.HerdemMove())
        self.do(hm.HerdemRotate())
        self.controller = controller
