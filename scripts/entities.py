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
        self.size = size
        self.velocity = [0,0]
    
    def update_pos(self, movement = (0,0)):


        #ok, so this function allows us to update the position of the physics entity
        #when updating the position of the physics entity, we need to think about movement in two dimensions. 
        #the x-dimension, where the movement is directly modified by the player, and the y-dimension, where gravity 
        #is the only factor affecting its movement. 

        #I am going to add the gravity factor here now.gravity affects the player to accelerate downwards. meaning that velocity increases every frame, until the 
        #velocity reaches terminal velocity. 

        self.velocity[1] = min(5,self.velocity[1] +0.3)

        #I will define a frame movement variable that defines how much movement there should be in this particular frame.
        frame_movement =  (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        #and this works because think of it like a frame being a single point in time. the current position in that frame 
        #plus the velocity of the entity in that frame would give you? The position of the entity in the next frame.            

        #add the collision detection here. So, a physics entity has a size. which represents the dimensions of the encompassing rectangle
        #if any of the edges of the rectangle meets with an edge of any other rectangle, the position is set to the edge of the
        # rectangle that is being collided against. 

        
        #update the position of the entity by this frame movement 
        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]
    

    #for any render function, you will need to pass it the surface on which you want to blit the object on. 
    def render(self,surf):
        #now here you need a sprite, and you need the position on which you want to print this on. 
        
        surf.blit(self.game.assets[self.type],self.pos)


#I realized that to specifically add a sprite to the player, I would need to create a separate class that is 
#inherited from the PhysicsEntity class.
class PlayerEntity(PhysicsEntity):
    def __init__(self,game,pos,size):
        super().__init__(game,'player',pos,size)

        #the player class will have all the properties and methods of the physicsEntity class, it's just that its size 
        #and type is predefined.
        


