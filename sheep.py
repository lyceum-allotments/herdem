#!/usr/bin/env python

import cocos
import utils
from cocos.actions import *
import cocos.collision_model as cm

import pymunk as pm
from pymunk import Vec2d
import math, sys, random
from constants import *
import animated_sprite as asp
import herdem_move as hm
import pyglet
import random 

sheep_speed = 80
class SheepSprite(asp.AnimatedSprite):

    def __init__(self, controller, pos = -1, image_file = "sheep"):
        spf = 0.12
        image_root = "images/%s" % image_file
        image_file = {"still" : pyglet.image.load("%s/0.png" % image_root),
                      "go"    : pyglet.image.Animation(
        [pyglet.image.AnimationFrame(pyglet.image.load("%s/1.png"% image_root),spf),
         pyglet.image.AnimationFrame(pyglet.image.load("%s/2.png"% image_root),spf),
         pyglet.image.AnimationFrame(pyglet.image.load("%s/3.png"% image_root),spf),
         pyglet.image.AnimationFrame(pyglet.image.load("%s/4.png"% image_root),spf)])}

        super(SheepSprite, self).__init__(image_file)
        self.space = controller.space
        self.controller = controller
        director = cocos.director.director
        xwin, ywin = director.get_window_size()

        self.speed = sheep_speed
        # Max. speed sheep can have when panicked
        self.panic_speed = 200
        self.panic = 0
        if pos == -1:
            pos = [random.uniform(xwin*0.15,xwin*0.65),
                   random.uniform(ywin*0.15,ywin*0.65)]

        self.position = pos
        self.velocity = (0,0)
        self.old_position = self.position 
        mass = 1
        radius = 40

        # Add pymunk body
        self.body = pm.Body(mass, pm.inf)
        self.body.position = pm.Vec2d(pos)
        velx = random.uniform(0,sheep_speed)*random.choice([-1,1])
        vely = random.uniform(0,sheep_speed)*random.choice([-1,1])
        self.body.velocity = (velx,vely)
        self.body.velocity_limit = sheep_speed
        self.shape = pm.Circle(self.body, radius)
        self.shape.elasticity = 1.0
        self.shape.collision_type = coll_types['sheep']
        self.shape.parent = self
        
        
        self.space.add(self.body, self.shape)

        self.do(hm.HerdemMove())
        self.do(hm.HerdemRotate())

    def get_allowed_directions(self):
        space = self.space
        allowed_directions = {'UP' : True,
                              'DOWN' : True,
                              'LEFT' : True,
                              'RIGHT': True}

        # print space.shape_query(self.shape)
        for s in space.shape_query(self.shape):
            if s.collision_type == coll_types['wall']:
                c = pm.Vec2d(s.parent.x + s.parent.width /2, s.parent.y + s.parent.height /2)
                theta = (pm.Vec2d(self.position) - c).angle_degrees % 360
                allowed_directions = utils.allowed_directions(theta, allowed_directions)
        return allowed_directions

    def calc_flee_vec(self, dog, allowed_directions):

        flee_vec = (self.body.position - dog.body.position)
        panic = (1.5 * (dog.influence_circle.radius + self.shape.radius - flee_vec.length) + self.speed)

        flee_vec = flee_vec.normalized() * panic
        if flee_vec[0] > 0 and not allowed_directions['RIGHT']:
            flee_vec[0] = 0
        elif flee_vec[0] < 0 and not allowed_directions['LEFT']:
            flee_vec[0] = 0
        elif flee_vec[1] > 0 and not allowed_directions['UP']:
            flee_vec[1] = 0
        elif flee_vec[1] < 0 and not allowed_directions['DOWN']:
            flee_vec[1] = 0
        return flee_vec

    def check_for_removal(self, dt):
        xwin, ywin = cocos.director.director.get_window_size()
        if self.x > xwin or self.x < 0 or self.y > ywin or self.y < 0:
            self.controller.scene.remove(self)
            self.controller.sheeps.remove(self)
