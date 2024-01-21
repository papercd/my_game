import pygame 
import math 

class Weapon:
    def __init__(self,type,sprite): 
        self.type = type 
        self.sprite = sprite 
        self.flipped = False 
        self.can_shoot = False 

    def equip(self,holder_entity):
        self.holder = holder_entity
        self.anchor_point = (self.holder.rect().topleft[0], self.holder.rect().topleft[1]+3)

    def update(self,cursor_pos):
        self.mpos = cursor_pos
        self.anchor_point = (self.holder.rect().topleft[0], self.holder.rect().topleft[1]+3)

    
    def render(self,surf,offset = (0,0)):
      
        weapon_display = pygame.Surface(self.sprite.get_size(),pygame.SRCALPHA,32)
        weapon_display.blit(self.sprite,(0,0))

        ANGLE_OFFSET =0

        if self.flipped == False: 
            ANGLE_OFFSET =11
        else: 
            ANGLE_OFFSET = -11
       

        dx, dy = self.mpos[0] - (self.anchor_point[0]-offset[0]), self.mpos[1] - (self.anchor_point[1] -offset[1]) 
        angle = math.degrees(math.atan2(-dy,dx)) -ANGLE_OFFSET

        angle_comp = angle + ANGLE_OFFSET


        if (angle_comp > 90 and angle_comp < 180) or (angle_comp >= -180 and angle_comp < -90):
            #flip the gun sprite. 
            if self.flipped != True: 
                self.sprite = pygame.transform.flip(self.sprite, False,True)
                self.flipped = True 
        else: 
            if self.flipped == True: 
                self.sprite = pygame.transform.flip(self.sprite, False,True)
            self.flipped = False 

        
        
        deviation_fix_x = 0
        deviation_fix_y = 0

        #second quadrant deviation fix 
        second_angle = abs(angle_comp-180)
       
        
        if  second_angle  > 0 and second_angle <=4 :
            deviation_fix_y = second_angle/9
            deviation_fix_x =  second_angle/ 60 +2
        elif second_angle>4 and second_angle<= 10: 
            deviation_fix_y = second_angle/7 -2
            deviation_fix_x =  second_angle/ 70 +1
        elif second_angle>10 and second_angle<=14:
            deviation_fix_y = second_angle/6  -2.3
            deviation_fix_x = -second_angle/ 70 +1
        elif second_angle> 14 and second_angle<= 17: 
            deviation_fix_y = second_angle/ 6.5 -2.3
            deviation_fix_x = second_angle/ 70 + 1
        elif second_angle>17 and second_angle<= 20:
            deviation_fix_y = second_angle/ 6.3   -2.3
            deviation_fix_x = second_angle/ 70    +1
        elif second_angle>20 and second_angle<= 63:   
            deviation_fix_y = second_angle/5.3   -2.3
            deviation_fix_x = second_angle/ 77    +1
        elif second_angle> 63 and second_angle<= 73: 
            deviation_fix_y = second_angle/6.3   -2
            deviation_fix_x = second_angle/ 77    -1
            angle += 10
        elif second_angle>73 and second_angle<= 77: 
            deviation_fix_y = second_angle/6.6  -2.3
            deviation_fix_x = second_angle/ 77    -1
            angle += 12
        elif second_angle> 77 and second_angle<=90: 
            deviation_fix_y = second_angle/6.6   -2.3
            deviation_fix_x = -second_angle/ 88    -1.5
            angle += 13

        third_angle = -(angle_comp + 180)
        
        #third quadrant deviation fix 
        if third_angle < -0 and third_angle >= -16:
            deviation_fix_y = -third_angle/20
            deviation_fix_x = -third_angle/ 88  + 2
        elif third_angle < -16 and third_angle >=-25:
            deviation_fix_y = -third_angle/26
            deviation_fix_x = -third_angle/ 84  +2
        elif third_angle < -25 and third_angle >=-27:
            deviation_fix_y = -third_angle/17
            deviation_fix_x = -third_angle/ 65 +2
        elif third_angle < -27 and third_angle >= -31:
            deviation_fix_y = -third_angle/16
            deviation_fix_x = -third_angle/ 88  +2
        elif third_angle < -31 and third_angle >= -46:
            deviation_fix_y = -third_angle/30
            deviation_fix_x = third_angle/ 60  +1
        elif third_angle < -46 and third_angle >= -57:
            deviation_fix_y = -third_angle/30
            deviation_fix_x = third_angle/ 60  -1
            
        elif third_angle < -57 and third_angle >= -66:
            deviation_fix_y = -third_angle/30 -2
            deviation_fix_x = third_angle/ 60  -4
           
        elif third_angle < -66 and third_angle >= -90:
            deviation_fix_y = -third_angle/30 -2
            deviation_fix_x = third_angle/ 60  -6


        
        #first quadrant deviation fix. 
        if angle_comp  > 0 and angle_comp <=4 :
            deviation_fix_y = angle/9
            deviation_fix_x = - angle/ 60 -1
        elif angle_comp>4 and angle_comp<= 10: 
            deviation_fix_y = angle/7
            deviation_fix_x = - angle/ 70
        elif angle_comp>10 and angle_comp<=14:
            deviation_fix_y = angle/6
            deviation_fix_x = angle/ 70
        elif angle_comp> 14 and angle_comp<= 17: 
            deviation_fix_y = angle/ 6.5
            deviation_fix_x = -angle/ 70 
        elif angle_comp>17 and angle_comp<= 20:
            deviation_fix_y = angle/ 6.3
            deviation_fix_x = -angle/ 70 
        elif angle_comp>20 and angle_comp<= 63:   
            deviation_fix_y = angle/ 5.3
            deviation_fix_x = -angle/ 77 
        elif angle_comp> 63 and angle_comp<= 73: 
            deviation_fix_y = angle/ 6.3
            deviation_fix_x = -angle/ 77 
        elif angle_comp>73 and angle<= 77: 
            deviation_fix_y = angle/ 6.6
            deviation_fix_x = -angle/ 77 
        elif angle_comp> 77 and angle_comp<=90: 
            deviation_fix_y = angle/ 6.6
            deviation_fix_x = angle/ 88 

        #fourth quadrant deviation fix
        if angle_comp < -6 and angle_comp >= -16:
            deviation_fix_y = -angle_comp/20
            deviation_fix_x = angle_comp/ 88 
        elif angle_comp < -16 and angle_comp >=-25:
            deviation_fix_y = -angle_comp/26
            deviation_fix_x = angle_comp/ 84 
        elif angle_comp < -25 and angle_comp >=-27:
            deviation_fix_y = -angle_comp/17
            deviation_fix_x = angle_comp/ 65
        elif angle_comp < -27 and angle_comp >= -31:
            deviation_fix_y = -angle_comp/16
            deviation_fix_x = angle_comp/ 88 
        elif angle_comp < -31 and angle_comp >= -90:
            deviation_fix_y = -angle_comp/30
            deviation_fix_x = -angle_comp/ 60     
        
        rotated_weapon_display = pygame.transform.rotate(weapon_display,angle)

        #now depending on whether the gun is flipped, change the blit location. 

        if self.holder.state == 'idle':
            surf.blit(rotated_weapon_display,(self.anchor_point[0] - offset[0]-deviation_fix_x, self.anchor_point[1]-offset[1]-deviation_fix_y))
        elif self.holder.state == 'run':
            RUN_RENDER_OFFSET = 0
            if self.holder.movement_intent[0] >0:
                #if player is running to the right, 
                if self.flipped: 
                    #if the cursor is on the left side, 
            
                    RUN_RENDER_OFFSET = 2
                else: 
                    #if the cursor is on the right side, 
                    RUN_RENDER_OFFSET = 3
            elif self.holder.movement_intent[0] < 0 :
                #if the player is running to the left, 
                if self.flipped: 
                    #if the cursor is on the left side, 
                    RUN_RENDER_OFFSET = -3
                else: 
                    RUN_RENDER_OFFSET = -2

            
            surf.blit(rotated_weapon_display,(self.anchor_point[0] - offset[0]-deviation_fix_x+RUN_RENDER_OFFSET, self.anchor_point[1]-offset[1]-deviation_fix_y))

  