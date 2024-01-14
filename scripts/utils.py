import os 
import pygame 


#so in here we are going to define a function that creates pygame image objects
#and returns them, so that we can simplify our code when creating our assets 
#dictionary.The assets dictionary is going to contain lists as well, lists of sprite objects
#for our grass, stone, and clouds, etc.

BASE_PATH = 'data/images/'

def load_image(path):
    sprite = pygame.image.load(BASE_PATH + path).convert()
    sprite.set_colorkey((0,0,0))
    return sprite 


#now the this load_images function will get all the sprites within one directory and turn them into a list.

def load_images(path):
    sprites = []
    #the sorted() method will turn the list into an alphabetically-sorted list.
    for sprite_name in sorted(os.listdir(BASE_PATH + path)):
        sprites.append(load_image(path+ '/' + sprite_name))

    return sprites