#!/usr/bin/env python

import cocos

from cocos.actions import *

from game_layer import *
from event_layer import *
from bg_layer import *
from controller import Controller
import constants

if __name__ == "__main__":
    
    director = cocos.director.director
    director.init(width=1280, height=800, resizable=True)
    #xwin, ywin = director.get_window_size()
    # 

    #pyglet.font.add_directory('.')


    #bg = cocos.sprite.Sprite("levels/title.png")
    #xwin, ywin = director.get_window_size()
    #bg.x = xwin/2
    #bg.y = ywin/2
    #    
    #director.run( cocos.scene.Scene(MainMenu() ) )

    controller = Controller(0)
    controller.run_level(0)
