import pygame 
import math

class Bullet: 
    def __init__(self,type,speed,sprite):
        self.type = type 
        self.sprite = sprite 
        self.pos = [0,0]
        self.start = [0,0]
        self.speed = speed 
        self.velocity = [0,0]
        self.frames_flown = 0
        self.angle = 0
    
    def copy(self):
        return Bullet(self.type,self.speed,self.sprite)

    def update(self):
        kill = False 
        if self.frames_flown > 200:
            kill = True 
        self.accelerate()
        self.pos[0] += self.velocity[0] * (self.speed + self.accelerate_amount)
        self.pos[1] += self.velocity[1] * (self.speed + self.accelerate_amount)
        self.frames_flown +=1

        return kill 
    
    def accelerate(self):
        self.accelerate_amount = math.sin(math.radians(self.frames_flown)) * 5

    def render(self,surf):
        #rotate the bullet 
        
        rotated_bullet = pygame.transform.rotate(self.sprite,-self.angle)
        surf.blit(rotated_bullet,(self.pos[0] + self.start[0],self.pos[1]+ self.start[1]))
        