from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()


textures = {
    1: load_texture("Assets/Textures/Grass_Block.png"),
    2: load_texture("Assets/Textures/Stone_Block.png"),
    3: load_texture("Assets/Textures/Brick_Block.png"),
    4: load_texture("Assets/Textures/Dirt_Block.png"),
    5: load_texture("Assets/Textures/Wood_Block.png")
}

sky_texture = load_texture("Assets/Textures/Skybox.png")
punch_sound = Audio("Assets/SFX/Punch_Sound.wav", loop=False, autoplay=False)




block_pick = 1

class Block(Button):
    def __init__(self, position = (0,0,0), texture=textures[1], breakable=True):
        super().__init__(
            parent=scene,
            position=position,
            model="Assets/Models/Block",
            origin_y=0.5,
            texture=texture,
            color=color.color(0,0,random.uniform(0.9,1)),
            highlight_color=color.light_gray,
            scale=0.5
        )
        self.breakable=breakable

        
    def input(self,key):
        if self.hovered:
            if key == "right mouse down":
                punch_sound.play()
                new_block = Block(position=self.position + mouse.normal, texture=textures[block_pick])
            elif key == "left mouse down" and self.breakable:
                punch_sound.play()
                destroy(self)


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model="sphere",
            texture=sky_texture,
            scale=150,
            double_sided=True
        )




for z in range(20):
    for x in range(20):
        block = Block(position=(x,0,z))

        


class Tree(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent=scene,
            position=position,
            model="Assets/Models/Lowpoly_tree_sample.obj",
            scale=(0.5,0.5,0.5)
        )

def generate_trees(num_trees=3, terrain_size=20):
    for _ in range(num_trees):
        x = random.randint(0, terrain_size-1)
        y = 0
        z = random.randint(0, terrain_size-1)
        Tree(position=(x,y,z))

generate_trees()

def terrainator():
    height = [[0 for x in range(20)] for z in range(20)]

    for z in range(20):
        for x in range(20):
            height[z][x] = random.randint(3,5)

    for z in range(1,19):
        for x in range(1,19):
            total = height[z][x]
            count = 1

            neighbors = [(0,1), (0,-1), (1,0), (-1,0)]
            for dx, dz in neighbors:
                total += height[z+dz][x+dx]
                count+=1
            height[z][x] = total // count


    
    for z in range(20):
            for x in range(20):
                h = height[z][x]

                for y in range(h+1):
                    if y ==h:
                        Block(position=(x,y,z), texture=textures[1])

                    elif y>=h - 2:
                        Block(position=(x,y,z), texture=textures[4])
                    else:
                        Block(position=(x,y,z), texture=textures[2])
                Block(position=(x,-1,z), texture=textures[2], breakable=False)


terrainator()



def update():
    global block_pick
    for i in range(1,6):
        if held_keys[str(i)]:
            block_pick = i
            break

    if player.y <= -100:
        player.position = (10,10,10)

    if held_keys["escape"]:
        application.quit()



    if held_keys["shift"]:
        player.speed = 10
    else:
        player.speed = 5

    if held_keys["r"]:
        player.jump_height = 10
    else:
        player.jump_height = 2


player = FirstPersonController()
sky = Sky()




if __name__ == "__main__":
    app.run()







