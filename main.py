'''Main file for the game. This is where the game loop will be.'''
# Importing built-in libraries
import math

# Importing third-party libraries
import pygame

# Importing local files

# Constants


# Messing around to test things
# Hex stuff
def axial_to_pixel(q, r, size):
    y = size * math.sqrt(3) * (r + q/2)
    x = size * 3/2 * q
    return (x, y)


def draw_hex(surface, center, size, color):
    points = [
        (center[0] + size * math.cos(math.radians(60 * i)),
         center[1] + size * math.sin(math.radians(60 * i)))
        for i in range(6)
    ]

    pygame.draw.polygon(surface, color, points, 2)


def axial_to_pixel_p(q, r, size):
    x = round(size * math.sqrt(3) * (q + r/2))
    y = round(size * 3/2 * r)
    return (x, y)


def draw_hex_p(surface, center, size, color):
    points = [
        (center[0] + size * math.cos(math.radians(60 * i - 30)),
         center[1] + size * math.sin(math.radians(60 * i - 30)))
        for i in range(6)
    ]

    pygame.draw.polygon(surface, color, points, 1)


# Check if the file is being run directly and not imported.
# If it is being run directly, run the game loop.
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Game')
    running = True
    size = 20
    event: pygame.event.Event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_KP_PLUS)

    thekey = event.key
    print(type(thekey))

    while running:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                running = False
            if (event.type == pygame.KEYDOWN and (event.key == pygame.K_KP_PLUS or
                                                  (event.key == pygame.K_EQUALS and
                                                   pygame.key.get_mods() & pygame.KMOD_SHIFT))):
                size += 5
                if size > 100:
                    size = 100
            if (event.type == pygame.KEYDOWN and (event.key == pygame.K_KP_MINUS or
                                                  (event.key == pygame.K_MINUS))):
                size -= 5
                if size < 5:
                    size = 5

        screen.fill((0, 0, 0))
        draw_hex_p(screen, axial_to_pixel_p(4, 4, size), size, (255, 255, 255))
        draw_hex_p(screen, axial_to_pixel_p(3, 4, size), size, (255, 255, 255))
        draw_hex_p(screen, axial_to_pixel_p(4, 3, size), size, (255, 255, 255))
        draw_hex_p(screen, axial_to_pixel_p(5, 4, size), size, (255, 255, 255))
        draw_hex_p(screen, axial_to_pixel_p(4, 5, size), size, (255, 255, 255))
        pygame.display.flip()

    pygame.quit()
