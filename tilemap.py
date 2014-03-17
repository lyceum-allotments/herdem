import cocos
import pymunk as pm
from constants import coll_types

class TileMap(cocos.layer.Layer):
    def __init__(self, pathname, controller):
        super(TileMap, self).__init__()

        # bg = cocos.tiles.load(pathname)['map0']
        bg = cocos.tiles.load(pathname)['Tile Layer 1']

        collision_tile_list = {coll_types["wall"] : "wall",
                               coll_types["exit"] : "exit"}
  
  
 
        director = cocos.director.director
        xwin, ywin = director.get_window_size()

        map_tw = len(bg.cells)
        map_th = len(bg.cells[0])

        for k in collision_tile_list.keys():
            for i in range(map_tw):
                for j in range(map_th):
                    # Adding the fence tiles to the static collision manager
                    if collision_tile_list[k] in bg.cells[i][j].tile.properties.keys():
                        add_ctile(bg.cells[i][j], k, controller.space)


        bg = cocos.sprite.Sprite("levels/level1.png")
        bg.position = (xwin/2, ywin/2)
        self.add(bg)





def add_ctile(cell, coll_type, space):
    verts = [(cell.x, cell.y),
             (cell.x + cell.width, cell.y),
             (cell.x + cell.width, cell.y + cell.height),
             (cell.x, cell.y + cell.height)]
    
    body = pm.Body()
    shape = pm.Poly(body, verts, (0,0),auto_order_vertices=True) 
    
    shape.collision_type = coll_type 
    shape.elasticity = 1.0
    shape.parent = cell
    
    space.add(shape)
    return
