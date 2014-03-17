#!/usr/bin/env python
"""
Initial menu view
"""

import cocos
from cocos.menu import *
from cocos.menu import ImageMenuItem
import pyglet

#from controller import Controller 

class MainMenu(cocos.menu.Menu):
    'Menu implementation has to be subclassed according to cocos2d docs'

    def __init__(self, controller):
        super( MainMenu, self ).__init__()
        
        # Set the controller to be used by the play method
        self.controller = controller
      
        # Set the items in the menut
        items = [
            ImageMenuItem('levels/play_menu.png', self.play),
            ImageMenuItem('levels/quit_menu.png', pyglet.app.exit),
        ]

        self.scale = 2.5
        self.position = (-200, -330)
        
        self.create_menu( items, shake(), shake_back() )

    def play(self):
        self.controller.run_level(1)


class MenuLayer(cocos.layer.Layer):

    def __init__(self, controller):
        super( MenuLayer, self ).__init__()
        
        # Add the background to the layer
        background_sprite = cocos.sprite.Sprite("levels/title.png")
        xwin, ywin = cocos.director.director.get_window_size()
        background_sprite.x = xwin/2
        background_sprite.y = ywin/2
        self.add(background_sprite, z=0)
        
        self.add(MainMenu(controller), z=1)
