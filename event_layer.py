#!/usr/bin/env python

import cocos
import pyglet

from cocos.actions import *

class EventLayer(cocos.layer.Layer):
    
    is_event_handler = True

    def __init__(self, controller):
        super(EventLayer, self).__init__()
        #should be removed
        self.controller = controller 
        self.keys_pressed = set()
        self.key_bindings = [{'UP' : 'UP', 'DOWN' : 'DOWN', 'LEFT' : 'LEFT', 'RIGHT' : 'RIGHT'},
                             {'UP' : 'W', 'DOWN' : 'S', 'LEFT' : 'A', 'RIGHT' : 'D'}]

    def player(self,key):
        if key == 'DOWN' or key == 'UP' or key == 'RIGHT' or key == 'LEFT':
            return 1
        if key == 'A' or key == 'W' or key == 'D' or 'S':
            return 2

    def player2_key(self,key):
        dir = ''
        if key == 'W': 
            dir = 'UP'
        if key == 'A':
            dir = 'LEFT'
        if key == 'D':
            dir = 'RIGHT'
        if key == 'S':
          dir = 'DOWN'
        return dir


    def update_direction(self, player_no):
        direction = [0, 0]
        i = player_no

        allowed_directions = self.controller.dog[i].get_allowed_directions()
        if self.key_bindings[i]['UP'] in self.keys_pressed and allowed_directions['UP']:
            direction[1] = 1
        elif self.key_bindings[i]['DOWN'] in self.keys_pressed and allowed_directions['DOWN']:
            direction[1] = -1
        if self.key_bindings[i]['RIGHT'] in self.keys_pressed and allowed_directions['RIGHT']:
            direction[0] = 1
        elif self.key_bindings[i]['LEFT'] in self.keys_pressed and allowed_directions['LEFT']:
            direction[0] = -1
        return direction


    def on_key_press(self,key, modifiers):
        
        key = pyglet.window.key.symbol_string(key)
        # Sometimes the key detector freaks out and repeatedly detects key presses
        # this stops this from affecting anything further down the line
        if key in self.keys_pressed:
            return

        if key == 'P':
            self.controller.pause_game()


        self.keys_pressed.add(key)

        for i in range(len(self.controller.dog)):
            if key in self.key_bindings[i].values():
                direction = self.update_direction(i)

                allowed_directions = self.controller.dog[i].get_allowed_directions()

                if self.key_bindings[i]['UP'] == key and allowed_directions['UP']:
                    direction[1] = 1
                elif self.key_bindings[i]['DOWN'] == key and allowed_directions['DOWN']:
                    direction[1] = -1
                if self.key_bindings[i]['RIGHT'] == key and allowed_directions['RIGHT']:
                    direction[0] = 1
                elif self.key_bindings[i]['LEFT'] == key and allowed_directions['LEFT']:
                    direction[0] = -1

                self.controller.move_dog(i, direction)

        
    def on_key_release(self, key, modifiers):
        key = pyglet.window.key.symbol_string(key)
        
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
        else:
            return
        for i in range(len(self.controller.dog)):
            if key in self.key_bindings[i].values():
                self.controller.move_dog(i, self.update_direction(i))
