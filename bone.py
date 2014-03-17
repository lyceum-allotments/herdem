import cocos
import random
import pymunk
from constants import *

class BoneSprite(cocos.sprite.Sprite):
    def __init__(self, controller):
        super(BoneSprite, self).__init__("images/bones/cartoon_bone.png")
       
        # Set a ramdom position of the bone
        director = cocos.director.director
        xpos, ypos = director.get_window_size()
        pos = [random.uniform(xpos*0.15,xpos*0.85),
               random.uniform(ypos*0.15,ypos*0.85)]
        self.position = pos
        
        # Set pymunk body and shape and add to the space
        self.body = pymunk.Body()
        self.body.position = self.position
       
        # Dog would eat the bone when it gets this close
        self.shape = pymunk.Circle(self.body, 20)
        self.shape.collision_type = coll_types['bone']
        self.space = controller.space
        self.space.add(self.shape)

        # Add bone's 'sphere of influence'
        # The dog would run if it get close enough
        self.influence_circle = pymunk.Circle(self.body, 200)
        self.influence_circle.collision_type = coll_types['bone_influence']
        self.influence_circle.sensor = True
        self.influence_circle.parent = self
        self.space.add(self.influence_circle)

        # Keep a link from the shape to the sprite
        self.shape.parent = self

        self.controller = controller

        self.being_eaten = False

    def remove_bone(self):
        
        # Remove bone from space and scene
        self.space.remove(self.shape)
        self.space.remove(self.influence_circle)
        self.controller.scene.remove(self)