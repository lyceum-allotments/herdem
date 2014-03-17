#!/usr/bin/env python

import cocos
from cocos.actions import *
import cocos.collision_model as cmodel
from time import gmtime, strftime
import pymunk as pm
import math
import random
import sheep
import constants
import time
from threading import Timer
import utils

def add_collision_handlers(controller):
    # Adding the various collision handlers

    space = controller.space

    space.add_collision_handler(constants.coll_types["dog"],
                                constants.coll_types["sheep"],
                                begin = halt_first,
                                separate = go)


    space.add_collision_handler(constants.coll_types["dog"],
                                constants.coll_types["dog"],
                                pre_solve = halt_both,
                                separate = go)

    space.add_collision_handler(constants.coll_types["dog"],
                                constants.coll_types["bone_influence"],
                                pre_solve = dog_is_near_bone)

    space.add_collision_handler(constants.coll_types["dog"],
                                constants.coll_types["bone"],
                                begin = dog_is_eating_bone)

    space.add_collision_handler(constants.coll_types["dog"],
                                constants.coll_types["wall"],
                                begin = wall_collide_b,
                                separate = wall_collide_s)

    space.add_collision_handler(constants.coll_types["dog_influence"],
                                constants.coll_types["sheep"],
                                begin = dog_sheep_b,
                                pre_solve = repel,
                                separate = dog_sheep_s)

    space.add_collision_handler(constants.coll_types['sheep'],
                                constants.coll_types['wolf'],
                                post_solve=remove_sheep)

    space.add_collision_handler(constants.coll_types['sheep'],
                                constants.coll_types['exit'],
                                begin = sheep_exit)

    space.add_collision_handler(constants.coll_types['dog'],
                                constants.coll_types['exit'],
                                begin = wall_collide_b,
                                separate = wall_collide_s)


def dog_is_near_bone(space, arbiter):
    #print "dog_bone_collision"
    # Get collision shapes and sprites
    dog_shape = arbiter.shapes[0]
    bone_shape = arbiter.shapes[1]
    dog = dog_shape.parent
    bone = bone_shape.parent
    
    # Lock the bone from being eaten by both dogs
    if not bone.being_eaten:
        # Make the dog run towards the bone
        x = bone.position[0] - dog.position[0]
        y = bone.position[1] - dog.position[1]
        angle = math.atan2(y, x) * 180 / math.pi
        dog.move_dog(angle)

        # Prevent user from controlling the dog
        dog.controllable = False
    
    return False


def dog_is_eating_bone(space, arbiter):
    print 'dog is eating'
    dog_shape = arbiter.shapes[0]
    bone_shape = arbiter.shapes[1]
    dog = dog_shape.parent
    bone = bone_shape.parent

    # Lock the bone from being eaten by both dogs
    if not bone.being_eaten:
        bone.being_eaten = True
        dog.eating_bone = True

        dog.stop_move()

        eating_time = 2
            
        # Remove bone after bone is eaten
        bone_timer = Timer(eating_time, bone.remove_bone)
        bone_timer.start()

        # Return control of the dog to the user
        dog_timer = Timer(eating_time, dog.finished_eating_bone)
        dog_timer.start()

    return False

def dog_sheep_b(space, arbiter):
    sheep =  arbiter.shapes[1].parent
    sheep.body.velocity_limit = sheep.panic_speed
    return True

def dog_sheep_s(space, arbiter):
    
    sheep = arbiter.shapes[1].parent
    sheep.controller.game_layer.schedule_interval(unpanic, 0.5, sheep)
    return True

def unpanic(dt, sheep):
    sheep.panic -= 10

    if sheep.panic < sheep.speed:
        sheep.body.velocity_limit = sheep.speed
        sheep.controller.game_layer.unschedule(unpanic)
    else:
        sheep.body.velocity = sheep.body.velocity.normalized() * sheep.panic
    return

def halt_first(space,arbiter):
    first = arbiter.shapes[0]
    
    first.body.velocity = pm.Vec2d((0,0))
    return True

def halt_both(space, arbiter):
    first = arbiter.shapes[0]
    second = arbiter.shapes[1]

    first.body.velocity = pm.Vec2d((0, 0))
    second.body.velocity = pm.Vec2d((0, 0))
    return False


def go(space, arbiter):
    
    global controller

    sprite = arbiter.shapes[0].parent
    p_no = sprite.player_number
    #sprite.move(sprite.controller.event_layer.update_direction(p_no))

    return True


def update_dn(sprite, space):
    p_no = sprite.player_number
    event_layer = sprite.controller.event_layer
    dn = event_layer.update_direction(p_no)
    #sprite.move(dn)
    #sprite.stop_move()

    return True



def wall_collide_b(space,arbiter):

    sprite = arbiter.shapes[0].parent
    space.add_post_step_callback(update_dn,sprite,space)
    return True


def wall_collide_s(space,arbiter):

    sprite = arbiter.shapes[0].parent
    space.add_post_step_callback(update_dn,sprite,space)

    return False

def override(space, arbiter):
    return False

def flee(sheep, space):
    flee_vecs = []

    allowed_directions = sheep.get_allowed_directions()

    for s in space.shape_query(sheep.shape):
        if s.collision_type == constants.coll_types['dog_influence']:
            flee_vecs.append(sheep.calc_flee_vec(s.parent, allowed_directions))
    total_flee_vec = flee_vecs[0]
    for f in flee_vecs[1:]:
        total_flee_vec += flee_vecs[0]
    new_panic = total_flee_vec.length


    if sheep.body.velocity.length < new_panic:
        sheep.panic = new_panic
        sheep.body.velocity = total_flee_vec.normalized() * new_panic
    else:
        sheep.body.velocity = total_flee_vec.normalized() * sheep.body.velocity.length



def repel(space, arbiter):
    sheep = arbiter.shapes[1].parent
    flee_vecs = []

    allowed_directions = sheep.get_allowed_directions()

    for s in space.shape_query(sheep.shape):
        if s.collision_type == constants.coll_types['dog_influence']:
            flee_vecs.append(sheep.calc_flee_vec(s.parent, allowed_directions))
    total_flee_vec = flee_vecs[0]
    for f in flee_vecs[1:]:
        total_flee_vec += flee_vecs[0]
    new_panic = total_flee_vec.length


    if sheep.body.velocity.length < new_panic:
        sheep.panic = new_panic
        sheep.body.velocity = total_flee_vec.normalized() * new_panic
    else:
        sheep.body.velocity = total_flee_vec.normalized() * sheep.body.velocity.length



    # space.add_post_step_callback(flee,sheep,space)
    return True

def remove_sheep(space, arbiter):

    print "REMOVING SHEEP"

    a,b = arbiter.shapes

    sheep = a.parent
    controller = sheep.controller
 
    if sheep in sheep.controller.sheeps:
 
        #remove sheep from the sheeps array
        controller.sheeps.remove(sheep)
        #remove the sheep from the scene
        controller.scene.remove(sheep)
        controller.lost_sheeps = controller.lost_sheeps + 1
        label_string = "Sheeps eaten: %i / %i" % (controller.lost_sheeps,controller.total_sheep)
        
        #update the number of sheeps lost label
        controller.game_layer.lost_label.element.text = label_string
    return True

def sheep_exit(space, arbiter):
    a, b = arbiter.shapes
    sheep = a.parent
    controller = sheep.controller

    space.add_post_step_callback(sheep_saved, sheep)
    return False

def sheep_saved(sheep):
    controller = sheep.controller

    colliding_with = [s.collision_type for s in
                  controller.space.shape_query(sheep.shape)]

    wall = constants.coll_types['wall']

    if sheep in sheep.controller.sheeps and wall not in colliding_with:
        sheep.body.velocity = pm.Vec2d([80, 0])
        controller.saved_sheeps += 1
        sheep.shape.sensor = True
        sheep.shape.collision_type = constants.coll_types['none']
        sheep.schedule(sheep.check_for_removal)
        label_string = "Sheeps saved: %i / %i" % (controller.saved_sheeps,controller.total_sheep)
        controller.game_layer.saved_label.element.text = label_string

    return True
