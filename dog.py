#!/usr/bin/env python

import cocos
import utils
import cocos.actions
import pymunk as pm
from pymunk import Vec2d
import math, sys, random
from constants import *
import animated_sprite as asp
import pyglet


class DogSprite(asp.AnimatedSprite):

    def __init__(self, controller, pos = -1, image_file = "dog"):
        self.velocity = (0,0)
        spf = 0.12  # seconds per frame
        # image_file = {"still" : pyglet.image.load("images/%s/0.png"%image),
        #               "go"    : pyglet.image.load("images/%s/0.png"%image)}
        image_file = {"still" : pyglet.image.load("images/dog/0.png"),
                      "go"    : pyglet.image.Animation(
   [pyglet.image.AnimationFrame(pyglet.image.load('images/dog/1.png'), spf),
    pyglet.image.AnimationFrame(pyglet.image.load('images/dog/2.png'), spf),
    pyglet.image.AnimationFrame(pyglet.image.load('images/dog/3.png'), spf),
    pyglet.image.AnimationFrame(pyglet.image.load('images/dog/4.png'), spf)])}

        super(DogSprite, self).__init__(image_file)
        
        director = cocos.director.director
        xpos, ypos = director.get_window_size()
        
        self.speed = 200
        self.controller = controller
    
        self.space = controller.space
        if pos == -1:
            pos = [random.uniform(xpos*0.15,xpos*0.85),
                   random.uniform(ypos*0.15,ypos*0.85)]


        self.position = pos
        radius = 50 

        # Add pymunk body
        self.body = pm.Body(1, pm.inf)
        self.body.position = pm.Vec2d(pos)
        self.body.velocity = (0,0)
        self.shape = pm.Circle(self.body, 25)
        # self.shape = pm.Poly(self.body, [(-29.5, 22.8), (40.5, 22.8), (40.5, -24.2), (-29.5, -24.2)]) 
        self.shape.elasticity = 0.0
        self.shape.collision_type = coll_types['dog']
        self.shape.parent = self

        self.turn = True

        # Add dog's 'sphere of influence'
        infl_radius = 100
        self.influence_circle =pm.Circle(self.body, infl_radius)
        self.influence_circle.collision_type = coll_types['dog_influence']
        self.influence_circle.sensor = True
        self.influence_circle.parent = self

        self.space.add(self.body, self.shape, self.influence_circle)

        self.do(DogMove())
        
        self.eating_bone = False

        # User can control the dog
        self.controllable = True
    
    def move_dog(self, angle):
        
        # From direction angle calcuate direction vector 
        angle_rad = angle / 180.0 * math.pi
        x = math.cos(angle_rad)
        y = math.sin(angle_rad)
        direction = cocos.euclid.Vector2(x, y).normalize()

        # Calculate velocity
        self.body.velocity = pm.Vec2d(direction) * self.speed 
        self.do(cocos.actions.RotateTo(-angle, 0.1))


    def finished_eating_bone(self):
        self.body.position = self.position
        self.do(DogMove())
        self.eating_bone = False
        self.controllable = True


    def stop_move(self):

        self.body.velocity = (0,0)

    def get_allowed_directions(self):
        space = self.space
        allowed_directions = {'UP' : True,
                              'DOWN' : True,
                              'LEFT' : True,
                              'RIGHT': True}

        # print space.shape_query(self.shape)
        for s in space.shape_query(self.shape):
            if s.collision_type in [coll_types['wall'], coll_types['exit']]:
                c = pm.Vec2d(s.parent.x + s.parent.width /2, s.parent.y + s.parent.height /2)
                theta = (pm.Vec2d(self.position) - c).angle_degrees % 360
                allowed_directions = utils.allowed_directions(theta, allowed_directions)
            if s.collision_type == coll_types['dog']:
                c = pm.Vec2d(s.parent.x, s.parent.y)
                theta = (pm.Vec2d(self.position) - c).angle_degrees % 360
                allowed_directions = utils.allowed_directions(theta, allowed_directions)

        return allowed_directions
                
class DogMove(cocos.actions.Move):
    def step(self, dt):
        #Update sprite position from pymunk body
        self.target.position = self.target.body.position
        
        # Get the magnitude of the body velocity
        velocity =  self.target.body.velocity.get_length()

        # Animate the dog only while it is moving
        if velocity > 0:
            self.target.set_animation()
        else:
            self.target.set_image("still")
      
        
