#!/usr/bin/env python

#cocos2d stuff
import cocos
from cocos.scene import *
from cocos.scenes import *

#pyglet and pymunk
import pyglet
import pymunk as pm

#game files
import game_layer
from game_layer import GameLayer
from bg_layer import BGLayer
from event_layer import EventLayer
import c_handlers
from constants import coll_types
from menu_layer import MenuLayer
import high_score as hs

#sprites
from dog import DogSprite
from wolf import WolfSprite
from sheep import SheepSprite
import herdem_level as hl

import time

import bone
import math


class Controller(cocos.scene.Scene):
    
    def __init__(self, levelNum = 0):
        super(Controller, self).__init__()

        # game state information, should be moved to a separate file
        # if it gets too big.
        self.number = levelNum
        self.space = pm.Space()

        c_handlers.add_collision_handlers(self)

        # Setup pause sprite
        self.game_paused = False
        self.pause_sprite = cocos.sprite.Sprite("levels/paused.png")
        xwin, ywin = cocos.director.director.get_window_size()
        self.pause_sprite.x = xwin/2
        self.pause_sprite.y = ywin/2


        self.multiplayer = True 

        self.sheeps = []
        self.dog = []

        self.saved_sheeps = 0
        self.lost_sheeps = 0
        self.testStr = "STRING FROM CONTROLLER.PY"

        self.level_list = [None, hl.Level1,hl.Level2] 
  
    def setup_level(self, level):
        
        #reset state info for new level
        self.total_sheep = 5 + self.number
        # self.total_sheep = 1

        self.saved_sheeps = 0
        self.lost_sheeps = 0
         
        #create a new scene in which all layers will be added
        self.scene = cocos.scene.Scene() 

        if level == 0:
            # Use menu layer for initial game startup
            self.scene.add(MenuLayer(self))
        else:
            if level == 1:
                self.game_layer = GameLayer(self, self.space)
                self.event_layer = EventLayer(self)


            self.game_layer.reset()
            self.start_time = time.time()
            for o in self.space.shapes + self.space.bodies:
                self.space.remove(o)
            # from pympler import summary
            # from pympler import muppy
            # sum1 = summary.summarize(muppy.get_objects())
            # summary.print_(sum1)


            # When the end of the game is reached just replay the
            # last level
            if level > len(self.level_list) - 1:
                level = -1
            self.level = self.level_list[level](self)
            self.level.create()

            self.game_layer.event_layer = self.event_layer
            
            self.scene.add(self.game_layer)
            self.scene.add(self.game_layer.event_layer)

            
            #adding sprites (model)
            # self.sheeps = []
            # for i in range(self.total_sheep):
            #     s = SheepSprite(self)
            #     self.sheeps.append(s)
            #     self.scene.add(s)
         
            # self.dog = []
            # self.dog.append(DogSprite(self, "dog"))
            # self.dog[0].player_number = 0
            # self.scene.add(self.dog[0])

            # #if multiplayer create two dogs
            # if self.multiplayer:
            #     self.dog.append(DogSprite(self, "brown_dog"))
            #     self.dog[1].player_number = 1
            #     self.scene.add(self.dog[1])
     
            # self.wolf = WolfSprite(self)
            #self.sheeps.append(self.wolf)
            # self.scene.add(self.wolf)
            self.scene.add(bone.BoneSprite(self))

            self.scene.schedule(self.update_pos)
     
    def run_level(self, num):

        self.director = cocos.director.director
        pyglet.font.add_directory('.')
        
        self.number = num
        print "num is: "+str(num)
        self.setup_level(num)
        
        if self.number != 0:
            self.director.push(FlipX3DTransition( self.scene, duration=1 ) ) 
        else:
            self.director.run(self.scene)

    def pause_game(self):
        # Add or remove pause sprite for pause/unpause
        # Could be changed to a layer if more options are required
        if not self.game_paused:
            self.scene.add(self.pause_sprite)
            self.scene.pause_scheduler()
            self.game_paused = True
        else:
            self.scene.remove(self.pause_sprite)
            self.scene.resume_scheduler()
            self.game_paused = False

    def lost(self):
        xwin, ywin = cocos.director.director.get_window_size()
        
        lost_sprite = cocos.sprite.Sprite("levels/lose_screen.png")
        lost_sprite.position = (xwin/2, ywin/2)
        self.scene.add(lost_sprite)
        self.scene.schedule_interval(self.gotomenu, 2)
    
    def gotomenu(self,dt):
        self.unschedule(self.gotomenu)
        #load main menu
        self.run_level(0);
        

    def won(self):
        xwin, ywin = cocos.director.director.get_window_size()
        
        lost_sprite = cocos.sprite.Sprite("levels/win_screen.png")
        lost_sprite.position = (xwin/2, ywin/2)
        self.scene.add(lost_sprite)
        # self.scene.schedule_interval(self.nextlevel, 2)
        self.finish_time = time.time()
        self.scene.schedule_interval(self.goto_hiscore, 2)

    def goto_hiscore(self, dt):
        self.scene.unschedule(self.goto_hiscore)
        self.scene.unschedule(self.update_pos)
        self.scene.add(hs.HighScore(self), z = 10)

    def nextlevel(self,dt):
        self.scene.unschedule(self.nextlevel)
        self.number += 1
        self.run_level(2);

        #self.game_layer = GameLayer(self, self.space)
        #bg_layer = BGLayer(self.number-1, self )
        #self.game_layer.event_layer = EventLayer(self)
        #game_scene = cocos.scene.Scene(bg_layer, game_layer, self.game_layer.event_layer)
        #print "LINE 145"    
        #cocos.director.director.push(FlipX3DTransition( game_scene, duration=1 ) ) 
    
    def move_dog(self, i, dir):
        
        # Stop the dog on key release or if dog is not controllable
        if (dir[1] == 0 and dir[0] == 0) or not self.dog[i].controllable:
            self.dog[i].stop_move()
        else:
            angle = math.atan2(dir[1], dir[0]) * 180.0 / math.pi
            self.dog[i].move_dog(angle)
        
    def update_pos(self,dt):
        
        self.space.step(dt)
              
        if self.level.lost() :
            self.lost()

        if self.level.won():
            self.won()
