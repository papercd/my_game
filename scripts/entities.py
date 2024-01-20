#alright, so this is where I am going to implement physics for the objects 
#of my game. 

import pygame 
from scripts.particles import Particle

class PhysicsEntity:
    #alright, what does a physics entity need? it needs a size, in 2 dimensions, 
    #and for my game, a physics entity will need a sprite, a position, and velocity. We would also need to define
    #the type of entity it is. Because there are different objects we can render in the game. Like rocks, grass, players. etc.
    #I will also add the game as a parameter so that any physics entity can access any other entity in the game. 

    def __init__(self,game,e_type,pos,size):
        self.game = game 
        self.type = e_type 
        self.pos = list(pos)  #this list() ensures that the position variable that you pass to the constructor 
                              #becomes a list. This gives us flexibility with passing argumments here for example 
                              #when we pass a tuple, this allows us to actually manage the position variable, as tuples can't be modified after initialization.
        self.collisions = {'up' :False,'down' : False, 'left': False, 'right': False }
        self.size = size
        self.velocity = [0,0]
        self.state = ''
        self.anim_offset = (-0,-0)
        self.flip = False
        self.set_state('idle')
        self.cut_movement_input = False 

    def set_state(self,action):
        if action != self.state: 
            self.state = action 
            self.animation = self.game.assets[self.type + '/' + self.state].copy() 

    def rect(self):
        return pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])
    
    def update_pos(self, tile_map, movement = (0,0)):
        
        self.collisions = {'up' :False,'down' : False, 'left': False, 'right': False }
        #ok, so this function allows us to update the position of the physics entity
        #when updating the position of the physics entity, we need to think about movement in two dimensions. 
        #the x-dimension, where the movement is directly modified by the player, and the y-dimension, where gravity 
        #is the only factor affecting its movement. 

        #I am going to add the gravity factor here now.gravity affects the player to accelerate downwards. meaning that velocity increases every frame, until the 
        #velocity reaches terminal velocity. 


        #this velocity part should be unique to the player, but whatever. I can change this later. 
        self.velocity[1] = min(5,self.velocity[1] +0.2)

        if self.velocity[0] < 0:
            self.velocity[0] = min(self.velocity[0]+0.25, 0)  
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] -0.25,0)

         

        #I will define a frame movement variable that defines how much movement there should be in this particular frame.
        if self.cut_movement_input:
            frame_movement = (self.velocity[0],self.velocity[1])
        else: 
            frame_movement =  (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        #and this works because think of it like a frame being a single point in time. the current position in that frame 
        #plus the velocity of the entity in that frame would give you? The position of the entity in the next frame.            

        #add the collision detection here. So, a physics entity has a size. which represents the dimensions of the encompassing rectangle
        #if any of the edges of the rectangle meets with an edge of any other rectangle, the position is set to the edge of the
        # rectangle that is being collided against. 
        
    
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect() 
        for rect in tile_map.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0: 
                    self.collisions['right'] = True
                    entity_rect.right = rect.left 
                if frame_movement[0] < 0: 
                    self.collisions['left'] = True
                    entity_rect.left = rect.right 
                self.pos[0] = entity_rect.x 
        



        self.pos[1] += frame_movement[1]
        entity_rect = self.rect() 
        for rect in tile_map.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0: 
                    self.collisions['down'] = True
                    entity_rect.bottom = rect.top  
                if frame_movement[1] < 0:  
                    self.collisions['up'] = True
                    entity_rect.top = rect.bottom
                self.velocity[1] = 0 
                self.pos[1] = entity_rect.y 

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0 :
            self.flip = True 

        self.animation.update()



    #for any render function, you will need to pass it the surface on which you want to blit the object on. 
    def render(self,surf,offset):
        #now here you need a sprite, and you need the position on which you want to print this on. 
        surf.blit(pygame.transform.flip(self.animation.img(),self.flip, False),(self.pos[0]-offset[0]+self.anim_offset[0],self.pos[1]-offset[1]+self.anim_offset[1]))
        


#I realized that to specifically add a sprite to the player, I would need to create a separate class that is 
#inherited from the PhysicsEntity class.
        
class PlayerEntity(PhysicsEntity):
    def __init__(self,game,pos,size):
        super().__init__(game,'player',pos,size)
        self.jump_count = 2
        self.wall_slide = False
        self.slide = False 
        self.on_wall = self.collisions['left'] or self.collisions['right']
        self.air_time = 0

        #attributes required to implement double tap 
      
        self.boost_dir = False 
        self.boost_on_next_tap = False 
        self.frame_count = 0
        self.frame_between_taps = 0
        self.running_time = 0
        

    def update_pos(self, tile_map, movement=(0, 0)):
        super().update_pos(tile_map, movement)
        self.air_time +=1
        self.frame_count += 1
        self.cut_movement_input = False 

        if self.collisions['down']:
            self.jump_count =2 
            self.air_time = 0
            
            
        self.wall_slide = False
        self.on_wall = self.collisions['left'] or self.collisions['right']

        if self.on_wall and self.air_time > 4:
            self.wall_slide = True 
            self.velocity[1] = min(self.velocity[1],0.5)
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True 
            
            self.set_state('wall_slide')
        
        if not self.wall_slide: 
            if self.air_time > 4:
                self.boost_on_next_tap = False 
                if self.velocity[1] < 0:
                    self.set_state('jump_up')
                elif self.velocity[1] >0:
                    self.set_state('jump_down')
                
            elif movement[0] != 0:
                self.set_state('run')

                self.frame_between_taps = self.frame_count
              
                if self.frame_between_taps == 1 :
                    self.running_time += 1
                elif (self.frame_between_taps > 1 and self.frame_between_taps <40):
    
                    if self.boost_on_next_tap and self.running_time < 10:
                        #then you boost.
                        dust = None
                        
                        if movement[0] > 0 and self.boost_dir == False:
                            dust = Particle(self.game,'dash_right',(self.rect().topleft[0]-1.4,self.rect().topleft[1]+2),velocity=[0,0],frame=0)
                            self.velocity[0] = 5.0
                        if movement[0] < 0 and self.boost_dir:
                             
                            #flip the dust particle effect
                            dust = Particle(self.game,'dash_left',(self.rect().topright[0]+1.4,self.rect().topright[1]+2),velocity=[0,0],frame=0)
                            self.velocity[0] = -5.0

                        
                        self.game.particles.append(dust)
                        self.boost_on_next_tap = False
                    else:
                        if movement[0] > 0:
                            self.boost_dir = False
                        if movement[0] < 0: 
                            self.boost_dir = True 
                        self.boost_on_next_tap = True 
                    self.running_time = 0
                    

                self.frame_count =0

                if self.slide:
                    self.cut_movement_input = True
                    self.set_state('slide')
                    
            else: 
                self.set_state('idle') 

        
    def player_jump(self):

        if self.wall_slide: 
            self.jump_count = 1
            if self.collisions['left']:
                
                self.velocity[0] =  3.6
            if self.collisions['right']:
                
                self.velocity[0] = -3.6
            self.velocity[1] =-3.3
            

        if self.jump_count == 2:
            if self.state == 'jump':
                self.jump_count -=2
                self.velocity[1] = -3.5
            else: 
                self.jump_count -=1
                self.velocity[1] = -3.5    
        elif self.jump_count ==1: 
            self.jump_count -=1
            self.velocity[1] = -3.5  


