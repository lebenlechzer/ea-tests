#!/usr/bin/env python
# vim: set fileencoding=utf8 :
import math
import sys
import copy

import pygame
import pygame.locals
import pymunk
import pymunk.vec2d
import pymunk.pygame_util

from body import Body

FPS = 40
ITERATIONS_PER_FRAME = 10
GRAVITY = (0., -1000)
SCREEN_SIZE = (1000, 400)
MOVE_FORCE_SIDE = pymunk.Vec2d(1e5, 0.)
MOVE_FORCE_UP = pymunk.Vec2d(0., 2e5)


def main():
    pygame.init()
    pygame.display.set_caption("Walker")

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    space = pymunk.Space()
    space.gravity = GRAVITY

    floor = create_floor()
    space.add(floor)
    space.add(create_walls())

    walker = Body(floor, leg_mass=1., leg_width=3., leg_length=100., init_leg_angle=30)
    walker.add_to_space(space)

    dt = 1. / FPS / ITERATIONS_PER_FRAME
    running = True
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.locals.KEYDOWN and
                     event.key == pygame.locals.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                walker.leg1.body.apply_force_at_local_point(MOVE_FORCE_SIDE, -walker.joint_pos_l1)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                walker.leg1.body.apply_force_at_local_point(-MOVE_FORCE_SIDE, -walker.joint_pos_l1)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                walker.leg2.body.apply_force_at_local_point(MOVE_FORCE_SIDE, -walker.joint_pos_l2)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                walker.leg2.body.apply_force_at_local_point(-MOVE_FORCE_SIDE, -walker.joint_pos_l2)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                walker.leg1_floor_motor.rate = 1.
                if walker.leg1_floor_motor not in space.constraints:
                    space.add(walker.leg1_floor_motor)
            elif event.type == pygame.KEYUP and event.key == pygame.K_x:
                if walker.leg1_floor_motor in space.constraints:
                    space.remove(walker.leg1_floor_motor)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                walker.leg1_floor_motor.rate = -1.
                if walker.leg1_floor_motor not in space.constraints:
                    space.add(walker.leg1_floor_motor)
            elif event.type == pygame.KEYUP and event.key == pygame.K_c:
                if walker.leg1_floor_motor in space.constraints:
                    space.remove(walker.leg1_floor_motor)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                walker.leg2_floor_motor.rate = 1.
                if walker.leg2_floor_motor not in space.constraints:
                    space.add(walker.leg2_floor_motor)
            elif event.type == pygame.KEYUP and event.key == pygame.K_n:
                if walker.leg2_floor_motor in space.constraints:
                    space.remove(walker.leg2_floor_motor)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                walker.leg2_floor_motor.rate = -1.
                if walker.leg2_floor_motor not in space.constraints:
                    space.add(walker.leg2_floor_motor)
            elif event.type == pygame.KEYUP and event.key == pygame.K_m:
                if walker.leg2_floor_motor in space.constraints:
                    space.remove(walker.leg2_floor_motor)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                local_force = copy.copy(MOVE_FORCE_UP)
                local_force.rotate(-walker.leg1.body.angle)
                walker.leg1.body.apply_force_at_local_point(local_force, walker.joint_pos_l1)

        screen.fill(pygame.color.THECOLORS['white'])
        space.debug_draw(draw_options)
        for _ in range(ITERATIONS_PER_FRAME):
            space.step(dt)
        pygame.display.flip()
        clock.tick(FPS)


def create_floor(friction=0.62):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 4)
    floor = pymunk.Segment(body, (-SCREEN_SIZE[0] / 2., 0), (SCREEN_SIZE[0] / 2., 0), SCREEN_SIZE[1] / 100.)
    floor.friction = friction
    return floor


def create_walls(friction=0.62):
    def create_wall(pos, from_pos, to_pos, width):
        wall_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        wall_body.position = pos
        wall = pymunk.Segment(wall_body, from_pos, to_pos, width)
        wall.friction = friction
        return wall

    left_wall = create_wall(pos=(0., SCREEN_SIZE[1] / 2.), from_pos=(0., -SCREEN_SIZE[1] / 2.),
                            to_pos=(0., SCREEN_SIZE[1] / 2.), width=SCREEN_SIZE[1] / 100.)
    right_wall = create_wall(pos=(SCREEN_SIZE[0], SCREEN_SIZE[1] / 2.), from_pos=(0., -SCREEN_SIZE[1] / 2.),
                             to_pos=(0., SCREEN_SIZE[1] / 2.), width=SCREEN_SIZE[1] / 100.)
    return left_wall, right_wall


if __name__ == "__main__":
    sys.exit(main())
