import pygame 
import math 

class Weapon:
    def __init__(self,type,sprite,fire_rate,opening_pos): 
        self.type = type 
        self.sprite = sprite 
        self.fire_rate = fire_rate
        self.opening_pos = list(opening_pos)
        self.flipped = False 
        self.can_shoot = False 
        self.left_anchor = self.sprite.get_rect().topleft
        self.right_anchor = self.sprite.get_rect().topright
        self.pivot = [0,0]
    

    
    def rotate(self,surface, angle, pivot, offset):
        
        rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
        rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
        # Add the offset vector to the center/pivot point to shift the rect.
        rect = rotated_image.get_rect(center=pivot+rotated_offset)
        return rotated_image, rect  # Return the rotated image and shifted rect.
    

    def equip(self,holder_entity):
        self.holder = holder_entity

    def shoot(self,firerate_frame):
        if firerate_frame % self.fire_rate == 0:
            #then you shoot. 
            pass   

    def update(self,cursor_pos):
        self.mpos = cursor_pos


    
    def render(self,surf,offset = (0,0)):
        
        rotate_cap_left = False
        rotate_cap_right = False

        #you need to define the anchor point positions for every state of the player. 
        if self.holder.state == 'idle':
            self.left_anchor = (2,6)
            self.right_anchor = (13,6)
        elif self.holder.state == 'run':
            if self.holder.flip: 
                self.left_anchor = (1,6)
                self.right_anchor = (8,5)
            else:
                self.left_anchor = (7,5)
                self.right_anchor = (14,6)
        elif self.holder.state == 'jump_up':
            if self.holder.flip: 
                self.left_anchor = (0,4)
                self.right_anchor =  (9,4) 
            else: 
                self.left_anchor = (6,4)
                self.right_anchor = (15,5)

        elif self.holder.state == 'jump_down':
            if self.holder.flip: 
                self.left_anchor = (3,5)
                self.right_anchor = (10,4)
            else: 
                self.left_anchor = (2,4)
                self.right_anchor = (7,5)
               
        elif self.holder.state == 'slide': 
            if self.holder.flip:
                rotate_cap_left = True
                self.right_anchor = (11,9)
            else: 
                self.left_anchor = (4,9)
                rotate_cap_right = True 
        
        #there is a bug wehere you can see frames blitz over at the 90 and - 90 line. think there is something going on when flip occurs. 
       

        if self.flipped: 
            dx, dy = self.mpos[0] - (self.holder.pos[0]+self.right_anchor[0]-offset[0]), self.mpos[1] - (self.holder.pos[1]+self.right_anchor[1]-offset[1])  
            self.pivot = [self.holder.pos[0]+self.right_anchor[0]-offset[0]-1,self.holder.pos[1]+self.right_anchor[1] -offset[1]]
            self.render_offset = pygame.math.Vector2(-7,2)       
        else: 
            dx,dy = self.mpos[0] - (self.holder.pos[0]+self.left_anchor[0]-offset[0]), self.mpos[1] - (self.holder.pos[1]+self.left_anchor[1] -offset[1]) 
            self.pivot = [self.holder.pos[0]+self.left_anchor[0]-offset[0]+1,self.holder.pos[1]+self.left_anchor[1] -offset[1]]
            self.render_offset = pygame.math.Vector2(7,2)

        angle = math.degrees(math.atan2(-dy,dx)) 
        print(angle)

        if (angle > 90 and angle <= 180) or (angle < -90 and angle >= -180):
            
            if rotate_cap_right:
                if self.flipped:
                    self.sprite = pygame.transform.flip(self.sprite,True,False)
                    self.flipped = False
                if (angle > 90 and angle <= 180):
                    
                    angle = -82
                elif (angle < -90 and angle >= -180):
                    
                    angle = 83
            else: 
                if self.flipped != True: 
                    self.sprite = pygame.transform.flip(self.sprite,True,False)
                    self.flipped = True 
                angle += 180
                angle = -angle
        else: 
            if rotate_cap_left:
                if self.flipped == False: 
                    self.sprite = pygame.transform.flip(self.sprite,True,False)
                    self.flipped = True
                if (angle >0 and angle <= 90) : 
                    pass
                    angle = 65
                elif (angle <= 0 and angle >= -90):
                    pass
                    angle =  -72
            else: 
                if self.flipped != False: 
                    self.sprite = self.sprite = pygame.transform.flip(self.sprite,True,False)
                    self.flipped = False             
                angle = -angle

        

        weapon_display = pygame.Surface((self.sprite.get_width(),self.sprite.get_height()),pygame.SRCALPHA)
        weapon_display.blit(self.sprite,(0,0))

        rotated_image,rect = self.rotate(weapon_display,angle,self.pivot,self.render_offset)

        surf.blit(rotated_image,rect)


  