import pgzrun
from pygame import Rect

# screen size configs --> creating a type of mesh to facilitate the definition of positions
TILE = 16
ROWS = 60
COLS = 32

WIDTH = TILE * ROWS
HEIGHT = TILE * COLS

TITLE = "Chiquinho's Adventure [Python Test]"

background_menu = Actor('background_m')
background_menu.pos = (400, 250)

game_title = Actor('game_title')
game_title.pos = (WIDTH//2, 100)

background_stage = Actor('background_stage')
background_stage.pos = (500, 250)

infos = Actor('infos')
infos.pos = (WIDTH//2, HEIGHT//2)

prize = Actor("prize")
prize.pos = (TILE * 3, TILE * 5)

# menu
menu_on = True
options = ["Start", "Exit", "Music and Sounds"]
selected_option = 0
sound_on = True

# set background music
music.play("music_background")
music.set_volume(0.4)

# background
platforms = [
    {"rect": Rect(TILE * 21, TILE * 8, TILE * 7, TILE),
     "imagem": "platforms"},  # Platform 1
    {"rect": Rect(TILE * 39, TILE * 8, TILE * 7, TILE),
     "imagem": "platforms"},  # Platform 2
    {"rect": Rect(TILE * 28, TILE * 22, TILE * 7, TILE),
     "imagem": "platforms"},  # Platform 3
    {"rect": Rect(TILE * 44, TILE * 19, TILE * 7, TILE),
     "imagem": "platforms"},  # Platform 4
]

blocks = [
    {"rect": Rect(TILE * 12.5, TILE * 25, TILE * 10, TILE * 64),
     "imagem": "blocks"},  # Block 1
    {"rect": Rect(0, TILE * 6, TILE * 10, TILE * 5),
     "imagem": "blocks"},  # Block 2
    {"rect": Rect(TILE * 55, TILE * 14, TILE * 5, TILE * 14),
     "imagem": "blocks2"},  # Block 3
]

grounds = [
    {"rect": Rect(0, HEIGHT - 4 * TILE, WIDTH, TILE * 4),
     "imagem": "ground"},  # Ground
]

# player
player = Actor("player_standing1")
player.pos = (TILE * 4, HEIGHT - TILE * 4)

player.velocity_x = 3
player.velocity_y = 0
player.current_frame = 0
player.direction = 1
in_floor = False

# values
gravity = 0.5
game_over = False
game_over_timer = 0
game_won = False
win_timer = 0
showing_infos = False
info_timer = 0

# sprites
player.walking_right = [
    "player_walking_right1", "player_walking_right2"]
player.walking_left = [
    "player_walking_left1", "player_walking_left2"]
player.standing_right = [
    "player_standing_right1", "player_standing_right2"]
player.standing_left = [
    "player_standing_left1", "player_standing_left2"]
player.actual_frame = 0
player.animation_time = 0
player.status = "standing"

# enemies
enemies = [
    {"actor": Actor("enemy_right1", pos=(TILE * 35, HEIGHT - TILE * 6)),
     "velocity_x": 2, "direction": 1, "walking_right": ["enemy_right1", "enemy_right2", "enemy_right3"],
     "walking_left": ["enemy_left1", "enemy_left2", "enemy_left3"], "current_frame": 0, "animation_time": 0,
     "limits": (TILE * 30, TILE * 50)},

    {"actor": Actor("enemy_right1", pos=(TILE * 50, HEIGHT - TILE * 6)),
     "velocity_x": 2, "direction": 1, "walking_right": ["enemy_right1", "enemy_right2", "enemy_right3"],
     "walking_left": ["enemy_left1", "enemy_left2", "enemy_left3"], "current_frame": 0, "animation_time": 0,
     "limits": (TILE * 30, TILE * 50)}
]


def play_sound():
    if sound_on:
        sounds.sound_options.play()


def draw():
    screen.clear()

    if menu_on:
        draw_menu()
    elif showing_infos:
        draw_infos()
    else:
        # draw background
        background_stage.draw()
        # draw player
        player.draw()
        # draw enemies
        for enemy in enemies:
            enemy["actor"].draw()
        # draw prize
        prize.draw()
        # draw platforms
        for platform in platforms:
            screen.blit(platform["imagem"],
                        (platform["rect"].x, platform["rect"].y))
        # draw blocks
        for block in blocks:
            screen.blit(block["imagem"], (block["rect"].x, block["rect"].y))
        # draw ground
        for ground in grounds:
            screen.blit(ground["imagem"], (ground["rect"].x, ground["rect"].y))
    # show game over message
    if game_over:
        screen.draw.text("Game Over :(", center=(
            WIDTH//2, HEIGHT//2), fontsize=50, color="white")
    # show win message
    if game_won:
        screen.draw.text("You Win! :)", center=(
            WIDTH//2, HEIGHT//2), fontsize=50, color="yellow")


def draw_menu():
    background_menu.draw()
    game_title.draw()

    for i, option in enumerate(options):
        cor = "yellow" if i == selected_option else "white"
        if option == "Music and Sounds":
            option += " (On)" if sound_on else " (Off)"
        screen.draw.text(option, center=(
            WIDTH//2, 200 + i * 50), fontsize=40, color=cor)


def draw_infos():
    screen.clear()
    screen.fill("black")
    infos.draw()


def update_animation():
    player.animation_time += 1
    if player.animation_time >= 10:
        player.animation_time = 0
        player.current_frame = (player.current_frame + 1) % 2

    if player.status == "walking":
        if player.direction == 1:
            player.image = player.walking_right[player.current_frame]
        else:
            player.image = player.walking_left[player.current_frame]
    else:
        if player.direction == 1:
            player.image = player.standing_right[player.current_frame]
        else:
            player.image = player.standing_left[player.current_frame]


def update_enemies():
    for enemy in enemies:
        actor = enemy["actor"]
        actor.x += enemy["velocity_x"] * enemy["direction"]

        if actor.x > TILE * 50 or actor.x < TILE * 30:
            enemy["direction"] *= -1

        enemy["animation_time"] += 1
        if enemy["animation_time"] >= 10:
            enemy["animation_time"] = 0
            enemy["current_frame"] = (enemy["current_frame"] + 1) % 2

        if enemy["direction"] == 1:
            actor.image = enemy["walking_right"][enemy["current_frame"]]
        else:
            actor.image = enemy["walking_left"][enemy["current_frame"]]


def restart_game():
    global game_over, game_over_timer
    game_over = False
    game_over_timer = 0

    player.pos = (TILE * 3, HEIGHT - TILE * 4)
    player.velocity_x = 3
    player.velocity_y = 0
    player.direction = 1
    player.status = "standing"

    enemies[0]["actor"].pos = (TILE * 35, HEIGHT - TILE * 6)
    enemies[0]["direction"] = 1
    enemies[1]["actor"].pos = (TILE * 50, HEIGHT - TILE * 6)
    enemies[1]["direction"] = 1


def trigger_game_over():
    global game_over, game_over_timer
    game_over = True
    game_over_timer = 0
    sounds.died.play()


def trigger_win():
    global game_won, win_timer, sound_on
    game_won = True
    win_timer = 0
    if sound_on == True:
        sounds.win.play()
    else:
        music.stop()


def update():
    global in_floor, velocity_x, game_over, game_over_timer, game_won, win_timer, showing_infos, info_timer

    if game_won:
        win_timer += 1
        if win_timer > 300:
            reset_to_menu()
        return

    if game_over:
        game_over_timer += 1
        if game_over_timer >= 200:
            restart_game()
        return

    if player.current_frame >= len(player.walking_right):
        player.current_frame = 0

    if keyboard.LEFT and player.midleft[0] > 0:
        player.x -= player.velocity_x
        player.status = "walking"
        player.direction = -1
        update_animation()

    elif keyboard.RIGHT and player.midright[0] < WIDTH:
        player.x += player.velocity_x
        player.status = "walking"
        player.direction = 1
        update_animation()

    else:
        player.status = "standing"
        update_animation()

    # gravity
    player.y += player.velocity_y
    player.velocity_y += gravity

    # platform collision
    for platform in platforms:
        if player.colliderect(platform["rect"]) and player.velocity_y >= 0:
            player.y = platform["rect"].top - (player.height / 2)
            player.velocity_y = 0
            in_floor = True
    # blocks collision
    for block in blocks:
        if player.colliderect(block["rect"]) and player.velocity_y >= 0:
            player.y = block["rect"].top - (player.height / 2)
            player.velocity_y = 0
            in_floor = True
    # ground collision
    for ground in grounds:
        if player.colliderect(ground["rect"]) and player.velocity_y >= 0:
            player.y = ground["rect"].top - (player.height / 2)
            player.velocity_y = 0
            in_floor = True
    # enemy collision
    for enemy in enemies:
        enemy["actor"].x += 2 * enemy["direction"]
        if enemy["actor"].x < enemy["limits"][0] or enemy["actor"].x > enemy["limits"][1]:
            enemy["direction"] *= -1
    # prize collision
    if player.colliderect(prize):
        trigger_win()

    for enemy in enemies:
        if player.colliderect(enemy["actor"]):
            trigger_game_over()

    if showing_infos:
        info_timer -= 1
        if info_timer <= 0:
            showing_infos = False
        return

    update_enemies()


def action(option):
    global menu_on, sound_on, showing_infos, info_timer
    if option == 0:
        menu_on = False
        showing_infos = True
        info_timer = 8 * 60
    elif option == 1:
        exit()
    elif option == 2:
        sound_on = not sound_on
        if sound_on:
            music.play("music_background")
        else:
            music.stop()


def on_key_down(key):
    global in_floor, selected_option, menu_on, sound_on, velocity_y

    if menu_on:
        if key == keys.UP:
            selected_option = (selected_option - 1) % len(options)
            play_sound()
        elif key == keys.DOWN:
            selected_option = (selected_option + 1) % len(options)
            play_sound()
        elif key == keys.RETURN:
            action(selected_option)

    else:
        if key == keys.SPACE and in_floor:
            player.velocity_y = -10
            in_floor = False
            if sound_on == True:
                sounds.jump.play()
            else:
                music.stop()


pgzrun.go()
