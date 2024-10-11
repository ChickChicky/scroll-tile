from math import *
from subprocess import Popen, PIPE
from sys import argv

_program = argv.pop(0)

import pygame

IMAGE = argv.pop(0)
IMAGE_SCALE = .15
IMAGE_ROT = 15
IMAGE_SPACING = 100, 100

RENDER_WIDTH, RENDER_HEIGHT = 680, 240
RENDER_FILE = argv.pop(0)

ANIMATION_TIME = 2
ANIMATION_FPS = 50

FLIP_ANGLE = 15
FLIP_TIME = 1

SCROLL_ANGLE = 45
SCROLL_SPEED = 1

BACKGROUND = (0,0,0)

pygame.init()

screen = pygame.display.set_mode((RENDER_WIDTH, RENDER_HEIGHT))
pygame.display.set_caption('Scrolling tile render')

base_img = pygame.transform.rotate(pygame.transform.scale_by(pygame.image.load(IMAGE),IMAGE_SCALE),IMAGE_ROT)

a = radians(SCROLL_ANGLE)
dx, dy = cos(a), sin(a)
b = radians(FLIP_ANGLE)
w, h = IMAGE_SPACING[0], IMAGE_SPACING[1]
k = (w**2+h**2)**.5

ffmpeg = Popen(
    args = [
        'ffmpeg',
        '-y',
        '-f', 'rawvideo',
        '-video_size', str(RENDER_WIDTH)+'x'+str(RENDER_HEIGHT),
        '-pix_fmt', 'rgb24',
        '-r', str(ANIMATION_FPS), 
        '-i', 'pipe:0',
        RENDER_FILE,
    ],
    stdin =  PIPE
)

f = 0
while f < ANIMATION_TIME*ANIMATION_FPS:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
            
    screen.fill(BACKGROUND)
    
    f += 1
    t = (f/ANIMATION_FPS) % ANIMATION_TIME
    d = t * k * SCROLL_SPEED
    ox, oy = dx * d, dy *d
    p = (t % (2*FLIP_TIME)) > FLIP_TIME
    
    img = pygame.transform.flip(base_img,p,False)
    
    ww = RENDER_WIDTH/w*1.5
    hh = RENDER_HEIGHT/h*1.5
    for yy in range(floor(-hh),ceil(hh)):
        for xx in range(floor(-ww),ceil(ww)):
            screen.blit(img, (ox+xx*w,oy+yy*h))
            
    arr = pygame.PixelArray(screen)
    ffmpeg.stdin.write(bytes(c for y in range(RENDER_HEIGHT) for x in range(RENDER_WIDTH) for c in (*screen.unmap_rgb(arr[x,y]),)[:3]))
    arr.close()

    pygame.display.flip()

pygame.quit()
