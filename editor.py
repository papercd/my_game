
import pygame
import sys 
from scripts.tilemap import Tilemap,Tile
from scripts.utils import load_images

RENDER_SCALE = 2.0

#now we need to add in the we have the player, now we need to add in the tiles. Now this is where things get a lot more difficult to follow. 

class Editor:
    def __init__(self):
        pygame.init() 
        pygame.display.set_caption('editor')
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
        } 

        self.movement = [False,False,False,False]

        self.Tilemap = Tilemap(self,tile_size=16)
        self.Tilemap.draw_tilemap()
        
        self.scroll = [0,0]

        #different variables that we can vary to choose different tiles to set down. 
        self.tile_list = list(self.assets)
        self.tile_group = 0 
        self.tile_variant = 0
        self.clicking = False 
        self.right_clicking = False 
        self.var_shift = False 
    
    def run(self):
        while True: 
            self.display.fill((0,0,0))
            #now we want to be able to move around our camera. with the arrow keys. 

            SCROLL_SPEED =2

            self.scroll[0] += (self.movement[1] - self.movement[0]) * SCROLL_SPEED
            self.scroll[1] += (self.movement[3] - self.movement[2]) * SCROLL_SPEED



            render_scroll = (int(self.scroll[0]),int(self.scroll[1]))

            #render the tilemap on the editor window 
            self.Tilemap.render(self.display, offset = render_scroll)

            #display the current tile selected from the tile list. 
            selected_tile = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy() 

            #make the selected tile partially transparent 
            selected_tile.set_alpha(100)

            #we need to scale down the mouse position as we scaled up our display on our viewing surface twicefold. 
            mpos = pygame.mouse.get_pos() 
            mpos = (mpos[0]/ RENDER_SCALE, mpos[1]/RENDER_SCALE)

            tile_pos = (int((mpos[0]+self.scroll[0])//self.Tilemap.tile_size) ,int((mpos[1]+self.scroll[1])//self.Tilemap.tile_size))
            

            #you want to know where your selected tile is going to be placed. 

            self.display.blit(selected_tile, (tile_pos[0]*self.Tilemap.tile_size - self.scroll[0],tile_pos[1]*self.Tilemap.tile_size - self.scroll[1]))


            #now that we have our mouse position, we are going to place the selected tile into our tilemap. 
            if self.clicking: 
                self.Tilemap.tilemap[str(tile_pos[0])+';'+str(tile_pos[1])] = Tile(self.tile_list[self.tile_group],self.tile_variant,tile_pos)
            
            #now that is nice and all, but now I need to be able to delete tiles from our tilemap. 
            if self.right_clicking: 
                click_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if click_loc in self.Tilemap.tilemap: 
                    del self.Tilemap.tilemap[click_loc]
                

            self.display.blit(selected_tile,(5,5))

            for event in pygame.event.get():
                #We need to define when the close button is pressed on the window. 
                if event.type == pygame.QUIT: 
                    #then pygame is closed, and the system is closed. 
                    pygame.quit() 
                    sys.exit() 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                    if event.button == 3:
                        self.right_clicking = True  
                    if self.var_shift: 
                        if event.button == 4:
                            self.tile_group = (self.tile_group -1) % len(self.tile_list)
                            self.tile_variant=0
                        if event.button == 5:
                            self.tile_group = (self.tile_group +1 ) % len(self.tile_list)
                            self.tile_variant=0
                    else: 
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant -1) % len(self.assets[self.tile_list[self.tile_group]])
                            
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant +1 ) % len(self.assets[self.tile_list[self.tile_group]])
                if event.type == pygame.MOUSEBUTTONUP: 
                    if event.button == 1 :
                        self.clicking = False 
                    if event.button == 3:
                        self.right_clicking = False 
                            
                #define when the right or left arrow keys are pressed, the corresponding player's movement variable varlues are changed. 
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_a: 
                        self.movement[0] = True 
                    if event.key == pygame.K_d: 
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_LSHIFT:
                        self.var_shift = True 

                if event.type == pygame.KEYUP: 
                    if event.key == pygame.K_a: 
                        self.movement[0] = False 
                    if event.key == pygame.K_d: 
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.var_shift = False 
        
            #pygame.display.update() updates the screen, and the clock.tick() adds the sleep in between every frame. 
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()),(0,0))
            pygame.display.update()
            self.clock.tick(60)

Editor().run()