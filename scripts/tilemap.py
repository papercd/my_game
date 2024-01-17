#alright, now to what I think is the most questionable part of this session. 
#adding a tilemap. If I were to create a tilemap class, I would 
#have an iterable of some kind containing all the tiles, and the tiles 
#would be defined by the type of tiles it is, the variant of type it is, 
#and the position that it is supposed to have. So let's define that.
#Now the idea that pops into mind is to create a tile class, 
#then create another class called the tilemap class which is effectively 
#a list of the tile objects. 
import pygame 

PHYSICS_APPLIED_TILE_TYPES = {'grass','stone'}
SURROUNDING_TILE_OFFSET = [(1,0),(1,-1),(0,-1),(0,0),(-1,-1),(-1,0),(-1,1),(0,1),(1,1)]

class Tilemap: 
    def __init__(self,game,tile_size = 16):
        self.tile_size = tile_size
        self.game = game
        self.tilemap = {}
        self.offgrid_tiles = [] 

    


    #the function that we are going to use to initialize tilemaps. Gonna be changed later 
    def draw_tilemap(self):
        for i in range(10):
            self.tilemap[str(3+i) + ';10'] = Tile('grass',1,(3+i,10))
            self.tilemap['10;' + str(i+5)] = Tile('stone',1,(10,5+i))


    #this function returns a list of tiles that surround a given position.
    def tiles_around(self,pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size),int(pos[1] // self.tile_size))
        for offset in SURROUNDING_TILE_OFFSET: 
            check_loc = str(tile_loc[0]+offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap: 
                tiles.append(self.tilemap[check_loc])
        return tiles 
    
    #this function will return the list of rectangles(grids) that surround a given position.
    #We want this function to select out the grids that we want to apply physics onto, so in this case, only 
    # when the grid is solid, grass or stone. 

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile.type in PHYSICS_APPLIED_TILE_TYPES:
                rect = pygame.Rect(tile.pos[0]*self.tile_size,tile.pos[1]*self.tile_size,self.tile_size,self.tile_size) 
                rects.append(rect)
        return rects 

    def render(self, surf, offset):
        for tile in self.offgrid_tiles: 
            surf.blit(self.game.assets[tile.type][tile.variant], (tile.pos[0] - offset[0],tile.pos[1]-offset[1]))
        
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile.type][tile.variant],(tile.pos[0] * self.tile_size-offset[0], tile.pos[1] *self.tile_size-offset[1]))
        
class Tile: 
    def __init__(self,type,variant,pos):
        self.type = type 
        self.variant = variant
        self.pos = pos 
        
