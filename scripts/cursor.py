import pygame 


class Cursor:
    def __init__(self,game,pos,type = 'default'):
        self.game = game 
        self.type = type
        self.pos = list(pos)
        self.sprite = self.game.assets['cursor' + '/' + self.type]


    def update(self):
        self.pos = pygame.mouse.get_pos()
        self.pos = (self.pos[0]/2,self.pos[1]/2)
    
    def render(self,surf):
        surf.blit(self.sprite,self.pos)