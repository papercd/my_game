
import pygame
import random
import math
import sys 
from scripts.tilemap import Tilemap
from scripts.utils import load_image,load_images,Animation
from scripts.entities import PlayerEntity
from scripts.clouds import Clouds
from scripts.particles import Particle
from scripts.cursor import Cursor
from scripts.weapons import Weapon 



class myGame:
    def __init__(self):
        pygame.init() 
        pygame.display.set_caption('myGame')
        self.screen = pygame.display.set_mode((1040,652))
        self.clock = pygame.Clock()
        self.display = pygame.Surface((self.screen.get_width()//2,self.screen.get_height()//2))

        #so coming back to here, we will define an assets dictionary that contains all of the assets
        #(sprites) that we are going to use to create our game. 

        self.assets = {
            'decor' : load_images('tiles/decor'),
            'grass' : load_images('tiles/grass'),
            'large_decor' : load_images('tiles/large_decor'),
            'stone' : load_images('tiles/stone'),
            'player' : load_image('entities/player.png'),
            'background': load_image('background.png'),
            'test_background' : load_image('test_background.png'),

            'cursor/default' : load_image('cursor/default_cursor.png',background='black'),
            'crosshair' : load_image('cursor/crosshair.png'),


            'clouds': load_images('clouds/default'),
            'gray1_clouds' : load_images('clouds/gray1',background = 'transparent'),
            'gray2_clouds' : load_images('clouds/gray2',background = 'transparent'),
            
            'player/idle' : Animation(load_images('entities/player/holding_gun/idle',background='transparent'), img_dur =6),
            'player/run' : Animation(load_images('entities/player/holding_gun/run',background='transparent'), img_dur =4),

            'player/jump_up' : Animation(load_images('entities/player/holding_gun/jump/up',background='transparent'), img_dur =5),
            'player/jump_down' : Animation(load_images('entities/player/holding_gun/jump/down',background='transparent'), img_dur =5,halt=True),
           

            'player/slide' : Animation(load_images('entities/player/slide',background='transparent'), img_dur =5),
            'player/wall_slide' : Animation(load_images('entities/player/wall_slide',background='transparent'), img_dur =4),
            


            'particle/leaf':Animation(load_images('particles/leaf'),img_dur =20,loop=False),
            'particle/jump':Animation(load_images('particles/jump',background= 'black'),img_dur= 2, loop= False),
            'particle/dash_left' : Animation(load_images('particles/dash/left',background='black'),img_dur=1,loop =False),
            'particle/dash_right' : Animation(load_images('particles/dash/right',background='black'),img_dur=1,loop =False),

            'particle/ak_smoke' : Animation(load_images('particles/ak_smoke',background='black'),img_dur=2,loop=False)
        } 


        self.weapons = {
            'ak' : Weapon('rifle',load_image('weapons/ak_holding.png',background='transparent'), 10,15,(2,2))
        }

        
        self.bullets = {
            'rifle_small' : load_image('bullets/rifle/small.png',background='transparent'),
        }
        self.bullets_on_screen = []
        

        self.gray_clouds = Clouds(self.assets['gray1_clouds'],count = 8,direction='right')
        self.opp_gray_clouds = Clouds(self.assets['gray2_clouds'],count = 6, direction= 'left')

        self.Tilemap = Tilemap(self,tile_size=16)
        self.Tilemap.load('map.json')

        #adding leaf shedding particle effects by locating where the trees are in the tilemap and spawning leaves in a certain location with regards to 
        #that tree location. 

        self.leaf_spawners = []
        for tree in self.Tilemap.extract([('large_decor',2)],keep = True):
            self.leaf_spawners.append(pygame.Rect(4+tree.pos[0], 4+tree.pos[1],23,13))
        

        self.particles = []
        
        

        self.player = PlayerEntity(self,(50,50),(16,16))
        self.player_movement = [False,False]
        self.scroll = [0,0]
        
        #cursor object 
        pygame.mouse.set_visible(True)
        self.cursor = Cursor(self,(50,50),(4,4),'default')

        #weapon equip
        self.player.equip_weapon(self.weapons['ak'])
        self.frame_count = 0
        self.reset = True 
       

    def run(self):
        while True: 
            self.frame_count = (self.frame_count+1) % 60 
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() /2 - self.scroll[0])/30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() /2 - self.scroll[1])/30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 399999 < rect.width * rect.height: 
                    pos = (rect.x +random.random()* rect.width,rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self,'leaf',pos,velocity=[random.randrange(-100,100)/1000,0.3], frame = random.randint(0,20)))

           
            #you should now add a cap to how much the map can move in either dimension, which you are going to add later. 
            background = pygame.transform.scale(self.assets['test_background'],(self.display.get_width()*1.4,self.display.get_height()*1.4))
            self.display.blit(background, [0-(0.4*self.display.get_width())/2- (render_scroll[0]/350) ,0-(0.4*self.display.get_height())/2 - (render_scroll[1]/350)])

            self.gray_clouds.update()
            self.gray_clouds.render(self.display,render_scroll)

            self.opp_gray_clouds.update()
            self.opp_gray_clouds.render(self.display,render_scroll)


            #Now that you've defined the update and render functions internally in the playerEntity class, 
            #We don't need the code here. 
            self.Tilemap.render(self.display,render_scroll)

            PLAYER_DEFAULT_SPEED = 1.5


            self.player.update_pos(self.Tilemap,self.cursor.pos,((self.player_movement[1]-self.player_movement[0])*PLAYER_DEFAULT_SPEED,0))
            self.player.render(self.display,render_scroll)
            
            #rapid fire and single fire toggle 
            if pygame.mouse.get_pressed()[0]:
                if self.player.weapon_toggle_state():
                    #then you shoot. 
                    self.player.shoot_weapon(self.frame_count)
                else:
                    #you shoot, once. 
                    if self.reset == True: 
                        self.player.shoot_weapon(self.frame_count)
                        self.reset = False 
            elif pygame.mouse.get_pressed()[0] == False:
                self.reset = True 
             

            #code for the cursor 
            self.cursor.update()
            self.cursor.render(self.display)
            


            for particle in self.particles.copy():
                if particle == None: 
                    self.particles.remove(particle)
                else:
                    kill =particle.update()
                    particle.render(self.display,offset = render_scroll)
                    if particle.type =='leaf':
                        particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                    if kill: 
                        self.particles.remove(particle)
            
            for bullet in self.bullets_on_screen:
                if bullet == None: 
                    self.bullets_on_screen.remove(bullet)
                else: 
                    kill = bullet.update_pos(self.Tilemap)
                    bullet.render(self.display,offset = render_scroll)
                
                    if kill: 
                        self.bullets_on_screen.remove(bullet)
            

            for event in pygame.event.get():
                #We need to define when the close button is pressed on the window. 
                        
                if event.type == pygame.QUIT: 
                    #then pygame is closed, and the system is closed. 
                    pygame.quit() 
                    sys.exit() 
                
                #define when the right or left arrow keys are pressed, the corresponding player's movement variable varlues are changed. 
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_a: 
                        
                        self.player_movement[0] = True
                    if event.key == pygame.K_d: 
                        
                        self.player_movement[1] = True

                    if event.key == pygame.K_w:
                        self.player.player_jump() 
                    if event.key == pygame.K_s: 
                        self.player.slide = True 
                    if event.key == pygame.K_g: 
                        self.player.toggle_rapid_fire()

                        
                #define when the right or left arrow keys are then lifted, the corresponding player's movement variable values are changed back to false.
                if event.type == pygame.KEYUP: 
                    if event.key == pygame.K_a: 
                        
                        self.player_movement[0] = False
                    if event.key == pygame.K_d:
                        
                        self.player_movement[1] = False 
                    if event.key == pygame.K_s: 
                        self.player.slide =False 
        
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))
            pygame.display.update()

            self.clock.tick(60)

myGame().run()