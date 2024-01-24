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
        self.movement_intent = [0,0]
        self.is_shooting = False

        #attributes required to implement double tap 
      
        self.boost_dir = False 
        self.boost_on_next_tap = False 
        self.frame_count_between_taps = 0
        #self.frame_between_taps = 0
        self.running_time = 0

        #attributes required to implement weapon equipment 
        self.equipped = False 
        self.cur_weapon = None 
        
       
      

    def update_pos(self, tile_map,cursor_pos,movement=(0, 0)):
        super().update_pos(tile_map, movement)
        self.movement_intent = movement
        self.air_time +=1
 
        self.frame_count_between_taps += 1

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

                #self.frame_between_taps = self.frame_count
              
                if self.frame_count_between_taps == 1 :
                    self.running_time += 1
                elif (self.frame_count_between_taps > 1 and self.frame_count_between_taps <40):
    
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
                    

                self.frame_count_between_taps =0

                if self.slide:
                    self.cut_movement_input = True
                    self.set_state('slide')
                    
            else: 
                self.set_state('idle') 

        if self.equipped:
            self.cur_weapon.update(cursor_pos)

        
    
    def render(self,surf,offset):
        super().render(surf,offset)
        if self.equipped: 
            self.cur_weapon.render(surf,offset)
        
    def player_jump(self):
        
        if self.wall_slide: 
            self.jump_count = 1
            
            if self.collisions['left']:
                
                self.velocity[0] =  3.6
            if self.collisions['right']:
                
                self.velocity[0] = -3.6
            self.velocity[1] =-3.3
            air = Particle(self.game,'jump',(self.rect().centerx,self.rect().bottom), velocity=[0,0.1],frame=0)
            self.game.particles.append(air)

        if self.jump_count == 2:
            if self.state == 'jump_down':
                self.jump_count -=2
                self.velocity[1] = -3.5
                air = Particle(self.game,'jump',(self.rect().centerx,self.rect().bottom), velocity=[0,0.1],frame=0)
                self.game.particles.append(air)
            else: 
                self.jump_count -=1
                self.velocity[1] = -3.5    
            
        elif self.jump_count ==1: 
            self.jump_count -=1
            self.velocity[1] = -3.5  
            air = Particle(self.game,'jump',(self.rect().centerx,self.rect().bottom), velocity=[0,0.1],frame=0)
            self.game.particles.append(air)

    def equip_weapon(self,weapon):
        self.cur_weapon = weapon 
        self.equipped = True 
        self.cur_weapon.equip(self)

    def shoot_weapon(self,frame):
        #testing bullet firing
        if self.equipped: 
            if self.cur_weapon.rapid_firing:
                if frame % self.cur_weapon.fire_rate == 0:
                    test_shell_image = self.game.bullets['rifle_small'].copy()
                    test_shell = Bullet(self.game,self.cur_weapon.opening_pos,test_shell_image.get_size(),test_shell_image).copy()
                    self.cur_weapon.load(test_shell)
                    self.game.bullets_on_screen.append(self.cur_weapon.shoot())
            else: 
                test_shell_image = self.game.bullets['rifle_small'].copy()
                test_shell = Bullet(self.game,self.cur_weapon.opening_pos,test_shell_image.get_size(),test_shell_image).copy()
                self.cur_weapon.load(test_shell)
                self.game.bullets_on_screen.append(self.cur_weapon.shoot())
                    
                    
    def toggle_rapid_fire(self):
        if self.equipped:
            self.cur_weapon.toggle_rapid_fire()


    def weapon_toggle_state(self):
        if self.equipped:
            return self.cur_weapon.rapid_firing 


class Bullet(PhysicsEntity): 
    def __init__(self,game,pos,size,sprite):
        super().__init__(game,'bullet',pos,size)
        self.angle = 0
        self.speed = 0 
        self.sprite = sprite
        self.set_state('in_place')
        self.frames_flown = 0
        self.test_tile = None
  
    def set_state(self, action):
        self.state = action

    def rect(self):
        return pygame.Rect(self.pos[0],self.pos[1],self.sprite.get_width(),self.sprite.get_height())

    def update_pos(self, tile_map,offset = (0,0)):
        self.collisions = {'up' :False,'down' : False, 'left': False, 'right': False }
        self.frames_flown +=1 

        if self.frames_flown >= 50:
            del self 
            return True

    

        self.pos[0] += self.velocity[0] 
        
        
        entity_rect = self.rect()
        for rect in tile_map.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if self.velocity[0] > 0: 
                    entity_rect.right = rect.left 
                
                if self.velocity[0] < 0: 
                    entity_rect.left = rect.right 
            
                self.pos[0] = entity_rect.x 
                del self 
                return True
            
        self.pos[1] += self.velocity[1]
        entity_rect = self.rect()
        for rect in tile_map.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if self.velocity[1] > 0: 
                    entity_rect.bottom = rect.top  
                    #get rid of the buulet 
                if self.velocity[1] < 0:  
                    entity_rect.top = rect.bottom
                    #get rid of the bullet 
    
                self.pos[1] = entity_rect.y 
                del self 
                return True
        """
        entity_rect = self.rect()
        tiles = tile_map.bullet_tiles_around(self.pos)
        if tiles:
            self.test_tile = tiles.pop()
        """     
                
                
        """
        
        """
        



        

        """
        entity_rect = self.rect()
        for rect in tile_map.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                del self 
                return True
                
                if frame_movement[1] > 0: 
                    self.collisions['down'] = True
                    entity_rect.bottom = rect.top  
                    #get rid of the buulet 
                if frame_movement[1] < 0:  
                    self.collisions['up'] = True
                    entity_rect.top = rect.bottom
                    #get rid of the bullet 
                self.velocity[1] = 0 
                self.pos[1] = entity_rect.y 
        """
    
    def render(self,surf,offset = (0,0)):
        """test_surface = pygame.Surface((16,16))
        if self.rects:
            surf.blit(test_surface,self.rects.pop())"""
        surf.blit(self.sprite, (self.pos[0]-offset[0],self.pos[1]-offset[1]))
       

    def copy(self):
        return Bullet(self.game,self.pos,self.size,self.sprite)



""" 

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
        

"""
        
