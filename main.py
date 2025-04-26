from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

chunk_size = 4
chunk_range = 2
block_size = 1
block_types = [color.green, color.brown, color.gray]
camera.fov = 105

window.fullscreen = True

chunks = {}

def generate_chunk(chunk_x, chunk_z):
    if (chunk_x, chunk_z) in chunks:
        return

    chunk = []

    for x in range(chunk_size):
        for z in range(chunk_size):
            world_x = chunk_x * chunk_size + x
            world_z = chunk_z * chunk_size + z
            height = 1
            
            for y in range(height):
                position = Vec3(world_x, y, world_z)
                color = random.choice(block_types)

                block = Entity(
                    model='cube', 
                    color=color, 
                    scale=block_size, 
                    position=position,
                    collider='box'
                )
                chunk.append(block)

    chunks[(chunk_x, chunk_z)] = chunk
    print(f"Generated chunk at ({chunk_x}, {chunk_z}) with {len(chunk)} blocks.")

def load_chunks_around_player():
    player_chunk_x = int(player.x // chunk_size)
    player_chunk_z = int(player.z // chunk_size)

    for cx in range(player_chunk_x - chunk_range, player_chunk_x + chunk_range + 1):
        for cz in range(player_chunk_z - chunk_range, player_chunk_z + chunk_range + 1):
            generate_chunk(cx, cz)

player = FirstPersonController()
player.gravity = 0.5
player.cursor.visible = True
player.y = 10

Sky()

coordinates_text = Text(
    text='',
    color=color.blue,
    origin=(0, 0),
    position=(0.1, 0.45),
    scale=2
)

def update():
    load_chunks_around_player()

    coordinates_text.text = f'X: {player.x:.2f} Y: {player.y:.2f} Z: {player.z:.2f}'

    player_chunk_x = int(player.x // chunk_size)
    player_chunk_z = int(player.z // chunk_size)
    for (cx, cz) in list(chunks.keys()):
        if abs(cx - player_chunk_x) > chunk_range or abs(cz - player_chunk_z) > chunk_range:
            for block in chunks[(cx, cz)]:
                block.remove_node()
            del chunks[(cx, cz)]

    if held_keys['p']:
        application.quit()

app.run()
