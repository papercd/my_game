import pygame
import sys 

#now we need to add in the we have the player, now we need to add in the tiles. Now this is where things get a lot more difficult to follow. 

class myGame:
    def __init__(self):
        pygame.init() 
        pygame.display.set_caption('myGame')
        self.screen = pygame.display.set_mode((500,500))
        self.clock = pygame.Clock()

        self.player = pygame.image.load('data/images/entities/player.png')
        self.player.set_colorkey((0,0,0))
        self.player_pos = [100,100]
        self.player_movement = [False,False]
    

    def run(self):
        while True: 
            self.screen.fill((100,100,100))

            self.player_pos[0] += (self.player_movement[1] - self.player_movement[0])* 3

            self.screen.blit(self.player, self.player_pos)
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
                #define when the right or left arrow keys are then lifted, the corresponding player's movement variable values are changed back to false.
                if event.type == pygame.KEYUP: 
                    if event.key == pygame.K_LEFT: 
                        self.player_movement[0] = False
                    if event.key == pygame.K_RIGHT: 
                        self.player_movement[1] = False 
        
            #pygame.display.update() updates the screen, and the clock.tick() adds the sleep in between every frame. 
            pygame.display.update()
            self.clock.tick(60)

myGame().run()