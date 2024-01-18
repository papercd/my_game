
import pygame
import random
import sys 
from scripts.tilemap import Tilemap
from scripts.utils import load_image,load_images,Animation
from scripts.entities import PhysicsEntity,PlayerEntity
from scripts.clouds import Clouds
from scripts.particles import Particle
#now we need to add in the we have the player, now we need to add in the tiles. Now this is where things get a lot more difficult to follow. 

class myGame:
    def __init__(self):
        pygame.init() 
        pygame.display.set_caption('myGame')
        self.screen = pygame.display.set_mode((640,480))
        self.clock = pygame.Clock()
        self.display = pygame.Surface((320,240))

        #so coming back to here, we will define an assets dictionary that contains all of the assets
        #(sprites) that we are going to use to create our game. 

        #Now that we have our load_image function defined, let's load the background into our assets 
        #and have that blitted onto our screen rather than just a gray screen. 
        self.assets = {
            'decor' : load_images('tiles/decor'),
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
            'player' : load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle' : Animation(load_images('entities/player/idle'), img_dur =6),
            'player/run' : Animation(load_images('entities/player/run'), img_dur =4),
            'player/jump' : Animation(load_images('entities/player/jump'), img_dur =5),
            'player/slide' : Animation(load_images('entities/player/slide'), img_dur =5),
            'player/wall_slide' : Animation(load_images('entities/player/idle'), img_dur =4),
            'particle/leaf':Animation(load_images('particles/leaf'),img_dur =20,loop=False)
        } 

        self.clouds = Clouds(self.assets['clouds'],count = 10, direction ='right')
        self.opp_clouds = Clouds(self.assets['clouds'],count = 6, direction ='left')
    

        self.Tilemap = Tilemap(self,tile_size=16)
        self.Tilemap.load('map.json')

        #adding leaf shedding particle effects by locating where the trees are in the tilemap and spawning leaves in a certain location with regards to 
        #that tree location. 

        self.leaf_spawners = []
        for tree in self.Tilemap.extract([('large_decor',2)],keep = True):
            self.leaf_spawners.append(pygame.Rect(4+tree.pos[0], 4+tree.pos[1],23,13))
        
        self.particles = []


        self.player = PlayerEntity(self,(50,50),(8,15))
        self.player_movement = [False,False]
        self.scroll = [0,0]
        
    
        #alright, now I am going to add a physics engine to make the player 
        #be able to jump, and collide into things. First, I am going to make 
        # a physics entity class from which we can create objects to apply physics onto, 
        #then create the player entity from that class.
    

    def run(self):
        while True: 
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() /2 - self.scroll[0])/30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() /2 - self.scroll[1])/30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 399999 < rect.width * rect.height: 
                    pos = (rect.x +random.random()* rect.width,rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self,'leaf',pos,velocity=[random.randrange(-100,100)/1000,0.3], frame = random.randint(0,20)))

            self.display.blit(self.assets['background'],[0,0])


            self.clouds.update()
            self.clouds.render(self.display,render_scroll)

            self.opp_clouds.update()
            self.opp_clouds.render(self.display,render_scroll)
            

            #Now that you've defined the update and render functions internally in the playerEntity class, 
            #We don't need the code here. 
            self.Tilemap.render(self.display,render_scroll)
            self.player.update_pos(self.Tilemap,(self.player_movement[1]-self.player_movement[0],0))
            self.player.render(self.display,render_scroll)

            for particle in self.particles.copy():
                kill =particle.update()
                particle.render(self.display,offset = render_scroll)
                if kill: 
                    self.particles.remove(particle)

            for event in pygame.event.get():
                #We need to define when the close button is pressed on the window. 
                if event.type == pygame.QUIT: 
                    #then pygame is closed, and the system is closed. 
                    pygame.quit() 
                    sys.exit() 

                #define when the right or left arrow keys are pressed, the corresponding player's movement variable varlues are changed. 
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_LEFT: 
                        self.player_movement[0] = True
                    if event.key == pygame.K_RIGHT: 
                        self.player_movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.player_jump() 

                        
                #define when the right or left arrow keys are then lifted, the corresponding player's movement variable values are changed back to false.
                if event.type == pygame.KEYUP: 
                    if event.key == pygame.K_LEFT: 
                        self.player_movement[0] = False
                    if event.key == pygame.K_RIGHT: 
                        self.player_movement[1] = False 
        
            #pygame.display.update() updates the screen, and the clock.tick() adds the sleep in between every frame. 
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))
            pygame.display.update()
            self.clock.tick(60)

myGame().run()