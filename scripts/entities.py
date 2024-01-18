#alright, so this is where I am going to implement physics for the objects 
#of my game. 

import pygame 

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
        self.anim_offset = (-3,-3)
        self.flip = False
        self.set_state('idle')

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

        self.velocity[1] = min(5,self.velocity[1] +0.1)

        #I will define a frame movement variable that defines how much movement there should be in this particular frame.
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
        self.first_jump = False 
        self.on_wall = self.collisions['left'] or self.collisions['right']
        self.air_time = 0
        
    def update_pos(self, tile_map, movement=(0, 0)):
        super().update_pos(tile_map, movement)
        self.air_time+=1
        if self.collisions['down']:
            self.jump_count =2 
            self.air_time = 0
        if self.air_time > 4:
            self.set_state('jump')
        elif movement[0] != 0:
            self.set_state('run')
        else: 
            self.set_state('idle') 
         
    def player_jump(self):
        if self.jump_count == 2:
            if self.state == 'jump':
                self.jump_count -=2
                self.velocity[1] = -3
            else: 
                self.jump_count -=1
                self.velocity[1] = -3    
        elif self.jump_count ==1: 
            self.jump_count -=1
            self.velocity[1] = -3  


