#!/usr/bin/env python
# vim: set fileencoding=utf8 :

import math
import copy

import pymunk


class Body(object):
    def __init__(self, x, y, leg_mass=5., leg_width=2., leg_length=40., leg_angle=30):
        self.leg_length = leg_length
        self.leg_mass = leg_mass
        self.leg_width = leg_width
        self.leg_angle = leg_angle

        self.leg1, self.joint_pos_l1, joint_pos_l1_ext = self.create_leg(self.leg_mass, self.leg_length, self.leg_width,
                                                                         math.radians(-self.leg_angle))
        self.leg2, self.joint_pos_l2, joint_pos_l2_ext = self.create_leg(self.leg_mass, self.leg_length, self.leg_width,
                                                                         math.radians(self.leg_angle))

        self.place_legs(x, y, joint_pos_l1_ext, joint_pos_l2_ext)

        self.rotation_center_legs_joint = pymunk.PinJoint(self.leg1.body, self.leg2.body,
                                                          self.joint_pos_l2, self.joint_pos_l1)
        self.rotation_center_legs_joint.collide_bodies = False

    def get_objects(self):
        return self.leg1, self.leg2, self.leg1.body, self.leg2.body, self.rotation_center_legs_joint

    def place_legs(self, x, y, offset_1, offset_2):
        self.leg1.body.position = (x + offset_1.x, y + offset_1.y)
        self.leg2.body.position = (x + offset_2.x, y + offset_2.y)

    @staticmethod
    def create_leg(leg_mass, leg_length, leg_width, angle):
        body = pymunk.Body(leg_mass, pymunk.moment_for_box(leg_mass, (leg_width, leg_length)))
        shape = pymunk.Poly.create_box(body, (leg_width, leg_length))
        vertices = shape.get_vertices()
        joint_position: pymunk.Vec2d = (vertices[1] + vertices[2]) / 2.
        # rotation = pymunk.transform.Transform(math.cos(angle), -math.sin(angle), math.sin(angle), math.cos(angle))
        # shape.unsafe_set_vertices(shape.get_vertices(), rotation)
        body.angle = -angle
        joint_position_ext = copy.copy(joint_position)
        joint_position_ext.rotate(angle)
        shape.friction = .4

        return shape, joint_position, joint_position_ext
