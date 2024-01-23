import pygame 
import math 

class Weapon:
    def __init__(self,type,sprite,fire_rate,img_pivot):  
        self.type = type 
        self.sprite = sprite 
        self.img_pivot = img_pivot
        self.flipped = False 
    
        self.fire_rate = fire_rate
        self.fire_frame = 0
        self.magazine = []

        self.is_shooting = False 
        self.opening_pos = [0,0]
    

    
    def rotate(self,surface, angle, pivot, offset):
        rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  
        rotated_offset = offset.rotate(angle)  
        rect = rotated_image.get_rect(center=pivot+rotated_offset)
        return rotated_image, rect  
    

    def equip(self,holder_entity):
        self.holder = holder_entity

    def load(self,bullet):
        self.magazine.append(bullet)

    def shoot(self):
        if self.fire_frame % self.fire_rate == 0:
            bullet = self.magazine.pop()
            if bullet: 
                self.fire_frame += 1
        
                bullet.start = self.opening_pos.copy()
                bullet.angle = -self.angle_opening
                bullet.velocity = [math.cos(math.radians(bullet.angle)),math.sin(math.radians(bullet.angle))]
                return bullet 
            else: 
                return None 
        else: 
            self.fire_frame += 1

                

    def update(self,cursor_pos):
        self.mpos = cursor_pos

    def render(self,surf,offset = (0,0)):
        #save surf to use when passing it to bullet 
        self.surf = surf 

        #you need to define the anchor point positions for every state of the player. 

        left_and_right_anchors = {  True: {"idle": {"left": (2,6), "right": (13,6)}, 'run' :{"left": (1,6), "right": (8,5)} 
                                           ,'jump_up' :{"left": (0,4), "right": (9,4)},'jump_down' :{"left": (3,5), "right": (10,4)}
                                           ,'slide' :{ "left" : (11,9) ,"right": (11,9)} , 'wall_slide' : {"left": (4,5), "right": (8,5)} 
                                           },
                                    False: {"idle": {"left": (2,6), "right": (13,6)}, 'run' :{"left": (7,5), "right": (14,6)} 
                                           ,'jump_up' :{"left": (6,4), "right": (15,5)},'jump_down' :{"left": (2,4), "right": (7,5)}
                                           ,'slide' :{ "left": (4,9), "right": (4,9) }, 'wall_slide': {'left' : (7,5), 'right' : (11,5)} 
                                           },
        }

        #get the anchors. 

        self.left_anchor = left_and_right_anchors[self.holder.flip][self.holder.state]["left"]
        self.right_anchor = left_and_right_anchors[self.holder.flip][self.holder.state]["right"]
       
        rotate_cap_left = False
        rotate_cap_right = False

        if self.holder.state == 'slide' or self.holder.state == 'wall_slide':
            if self.holder.flip:
                rotate_cap_left = True 
            else: 
                rotate_cap_right = True 

        #get the angle, the pivot, and offset
        if self.flipped: 
            self.pivot = [self.holder.pos[0]+self.right_anchor[0]-offset[0]-1,self.holder.pos[1]+self.right_anchor[1] -offset[1]]
            self.render_offset = pygame.math.Vector2(-self.sprite.get_rect().centerx + self.img_pivot[0],self.sprite.get_rect().centery - self.img_pivot[1] )       
        else: 
            self.pivot = [self.holder.pos[0]+self.left_anchor[0]-offset[0]+1,self.holder.pos[1]+self.left_anchor[1] -offset[1]]
            self.render_offset = pygame.math.Vector2(self.sprite.get_rect().centerx - self.img_pivot[0], self.sprite.get_rect().centery - self.img_pivot[1])

        dx,dy = self.mpos[0] - self.pivot[0], self.mpos[1]- self.pivot[1]
        angle = math.degrees(math.atan2(-dy,dx)) 
        sprite_width = self.sprite.get_width()
        
        #separate angle varialble for the gun's opening - to apply angle cap and to pass onto firing bullet 
        self.angle_opening = angle 

        #flip transition lag exists. If it happens, don't blit the gun, and turn off the shooting function. 
        blitz = False

        #based on the angle, flip the sprite.If you are sliding, cap the angle. 
        if (angle > 90 and angle <= 180) or (angle < -90 and angle >= -180):
            if rotate_cap_right:
                if self.flipped:
                    self.sprite = pygame.transform.flip(self.sprite,True,False)
                    self.flipped = False
                    blitz = True 
                if (angle > 90 and angle <= 180):
                    angle = -82
                elif (angle < -90 and angle >= -180):
                    angle = 83
                self.angle_opening = -angle 
            else: 
                if self.flipped != True: 
                    self.sprite = pygame.transform.flip(self.sprite,True,False)
                    self.flipped = True 
                    blitz = True 
                angle += 180
                angle = -angle
        else: 
            if rotate_cap_left:
                if self.flipped == False: 
                    self.sprite = pygame.transform.flip(self.sprite,True,False)
                    self.flipped = True
                    blitz = True 
                if (angle >0 and angle <= 90) : 
                    angle = 65
                elif (angle <= 0 and angle >= -90):
                    angle =  -72
                self.angle_opening = 180-angle 
            else: 
                if self.flipped != False: 
                    self.sprite = self.sprite = pygame.transform.flip(self.sprite,True,False)
                    self.flipped = False  
                    blitz = True 
                angle = -angle


        weapon_display = pygame.Surface((self.sprite.get_width(),self.sprite.get_height()),pygame.SRCALPHA)
        weapon_display.blit(self.sprite,(0,0))
        rotated_image,rect = self.rotate(weapon_display,angle,self.pivot,self.render_offset)

        #the gun's opening position  
        self.opening_pos[0] = self.pivot[0] + math.cos(math.radians(-self.angle_opening)) * sprite_width
        self.opening_pos[1] = self.pivot[1] + math.sin(math.radians(-self.angle_opening)) * sprite_width


        if not blitz: 

            surf.blit(rotated_image,rect)
         
        


  