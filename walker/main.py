#!/usr/bin/env python
# vim: set fileencoding=utf8 :

import sys
import pygame
import pygame.locals
import pymunk
import pymunk.pygame_util

from body import Body

FPS = 40
ITERATIONS_PER_FRAME = 10
GRAVITY = (0., -98.1)
SCREEN_SIZE = (400, 400)


def main():
    pygame.init()
    pygame.display.set_caption("Walker")

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    space = pymunk.Space()
    space.gravity = GRAVITY

    body = Body(200, 200, leg_mass=20., leg_width=3., leg_length=100., leg_angle=30)
    space.add(*body.get_objects())

    space.add(create_floor())

    dt = 1. / FPS / ITERATIONS_PER_FRAME
    running = True
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.locals.KEYDOWN and
                     event.key == pygame.locals.K_ESCAPE):
                running = False
        screen.fill(pygame.color.THECOLORS['white'])
        space.debug_draw(draw_options)
        for _ in range(ITERATIONS_PER_FRAME):
            space.step(dt)
        pygame.display.flip()
        clock.tick(FPS)


def create_floor():
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 4)
    floor = pymunk.Segment(body, (-SCREEN_SIZE[0] / 2., 0), (SCREEN_SIZE[0] / 2., 0), SCREEN_SIZE[1] / 100.)
    floor.friction = 0.62
    return floor


if __name__ == "__main__":
    sys.exit(main())
