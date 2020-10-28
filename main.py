import pygame
import image
import glob
from random import choice

def find_images():
    return glob.glob('*.png') + glob.glob('*.jpg')

def main():
    paths = find_images()
    height = 600
    width = 600
    window = pygame.display.set_mode((width, height))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        img = image.image(choice(paths))
        img.scale(width, height)
        img.random_filter()()
        window.fill((255, 255, 255))
        window.blit(img.get_surface(), (0, 0))
        pygame.display.update()
        pygame.time.wait(2000)

if __name__ == '__main__':
    main()
