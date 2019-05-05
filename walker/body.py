#!/usr/bin/env python
# vim: set fileencoding=utf8 :

import math

import pymunk
import pygame


class Body(object):
    def __init__(self, floor, leg_mass=5., leg_width=2., leg_length=40., leg_friction=.4, init_leg_angle=30):
        self.leg_length = leg_length
        self.leg_mass = leg_mass
        self.leg_width = leg_width
        self.leg_friction = leg_friction
        self.legs_min_angle = 0.
        self.legs_max_angle = .9 * math.pi

        self.leg1, self.joint_pos_l1 = self.create_leg(self.leg_mass, self.leg_length, self.leg_width,
                                                       math.radians(init_leg_angle), leg_friction,
                                                       pygame.color.THECOLORS['red'])
        self.leg2, self.joint_pos_l2 = self.create_leg(self.leg_mass, self.leg_length, self.leg_width,
                                                       math.radians(-init_leg_angle), leg_friction,
                                                       pygame.color.THECOLORS['green'])

        leg_position_x = floor.body.position.x / 8.
        leg_position_y = floor.body.position.y
        self.place_leg(self.leg1, leg_position_x, leg_position_y, math.radians(init_leg_angle))
        self.place_leg(self.leg2, leg_position_x, leg_position_y, math.radians(-init_leg_angle))

        self.rotation_center_legs_joint = pymunk.PivotJoint(self.leg1.body, self.leg2.body,
                                                            self.joint_pos_l2, self.joint_pos_l1)
        self.rotation_center_legs_joint.collide_bodies = False

        self.leg1_floor_motor = pymunk.SimpleMotor(self.leg1.body, floor.body, 0.)
        self.leg2_floor_motor = pymunk.SimpleMotor(self.leg2.body, floor.body, 0.)

        self.legs_rotary_limit_joint = pymunk.RotaryLimitJoint(self.leg1.body, self.leg2.body,
                                                               self.legs_min_angle, self.legs_max_angle)

    def add_to_space(self, space: pymunk.Space):
        space.add(self.leg1, self.leg2, self.leg1.body, self.leg2.body, self.rotation_center_legs_joint,
                  self.legs_rotary_limit_joint)

    def place_leg(self, leg, x, y, angle):
        leg.body.position = (x - self.leg_length * math.sin(angle) / 2.,
                             y + self.leg_length * math.cos(angle) / 2.)

    @staticmethod
    def create_leg(mass, length, width, angle, friction, color):
        body = pymunk.Body(mass, pymunk.moment_for_box(mass, (width, length)))
        shape = pymunk.Poly.create_box(body, (width, length))
        vertices = shape.get_vertices()
        joint_position: pymunk.Vec2d = (vertices[1] + vertices[2]) / 2.
        body.angle = -angle
        shape.friction = friction
        shape.color = color
        return shape, joint_position
