#!/usr/bin/env python
# vim: set fileencoding=utf8 :

import sys
import pygame
import pygame.locals
import pymunk

def main():
    pygame.init()
    pygame.display.set_caption("Walker")

    screen = pygame.display.set_mode((240,180))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
              (event.type == pygame.locals.KEYDOWN and
               event.key == pygame.locals.K_ESCAPE):
                running = False


if __name__ == "__main__":
    sys.exit(main())
