## NEBULA Game Framework by VaclavK
## currently a prototype

# imports
import pygame # library, that powers Nebula GF
import pymunk # physics library for built-in physics objects
import os
import math
import random
""" import pyaudio as pa """

pygame.init()
""" PA = pa.PyAudio """

# pygame window creation
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Snowshooter")

# pymunk space creation
""" phys_space = pymunk.Space() """

# public variables go in here ->
default_font = pygame.font.SysFont("Arial", 40)
counter_font = pygame.font.SysFont("Arial", 80)

# engine default variables ->
window_width, window_heigth = pygame.display.get_surface().get_size()
to_render = []
timers = []

running = True
clock = pygame.time.Clock()
fps = 0
dt = 0
layers_current = 7 # set how many layers your game uses; start from 0, don't use more layers, than you need, because it drastically slows down the render times

# pyaudio setup
""" pa_bitrate = 16000
pa_freq = 500
pa_len = 1

pa_bitrate = max(pa_bitrate, pa_freq + 100)
pa_num_of_frames = int(pa_bitrate * pa_len)
pa_rest_frames = pa_num_of_frames % pa_bitrate
pa_wave_data = ""

for i in range(pa_num_of_frames):
    pa_wave_data += chr(int(math.sin(i/((pa_bitrate/pa_freq)/math.pi))*127+128))

for i in range(pa_rest_frames):
    pa_wave_data += chr(128)

p = PA()

stream = p.open(format=p.get_format_from_width(1),
                channels=1,
                rate=pa_bitrate,
                output=True)
stream.write(pa_wave_data)
stream.stop_stream()
stream.close()
p.terminate() """

# set variable defaults here ->
vstup = []
speed = 100

debug_enabled = False

player_radius = 40
player_health = 3
player_max_health = 3

player_trail = []

white = (255, 255, 255)

mouse_pos = (0, 0)
mouse_left_click = False
mouse_last = False
mouse_current_delta = 0
mouse_set_delta = 0.5#0.06#0.5

r_last = False
r_changed = False

place_key_last = False
place_key_changed = False

cross_pos_start = (100, 100)
cross_pos_end = (200, 200)

bullets = []
bullet_spawned = False
hit_strenght = 25
hit_strenght_divider = 1.5
knockback_strenght = 0#0
bullet_piercing = 0#0

player_rocket_speed = 800
laser_strength = 1000

enemy_small_health = 100#100
enemy_small_speed = 100
enemy_small_size = 40
enemy_small_crystals = 5#5
enemy_small_color = (255, 0, 0)
enemy_small_width = 10

boss_small_health = 400
boss_small_speed = 80
boss_small_size = 80
boss_small_crystals = 250
boss_small_color = (255, 50, 50)
boss_small_width = 15

boss_guard_health = 1000 # is procedural; this is only multiplication base
boss_guard_speed = 80
boss_guard_size = 140
boss_guard_crystals = 300 # is procedural; multip base
boss_guard_color = (255, 60, 40)
boss_guard_width = 30

boss_guard_health_this_effin_wave = 0 # changed in enemy creation
boss_guard_particle_density = 100

enemy_runner_health = 50
enemy_runner_speed = 300
enemy_runner_size = 30
enemy_runner_crystals = 10
enemy_runner_color = (255, 50, 0)
enemy_runner_width = 10

enemy_archer_health = 150
enemy_archer_speed = 90
enemy_archer_size = 45
enemy_archer_crystals = 40
enemy_archer_color = (255, 130, 0)
enemy_archer_width = 13

archer_distancing = 600
archer_shoot_frequency = 6
archer_shoot_distance = 800

enemy_bomber_health = 500
enemy_bomber_speed = 120
enemy_bomber_size = 40
enemy_bomber_crystals = 80
enemy_bomber_color = (255, 90, 0)
enemy_bomber_width = 25

bomber_effect_radius = 200
explosion_particle_density = 60

enemies = []
particles = []
crystals = []

particle_density = 40 #40

crystal_chance = 5 #5
crystal_pickup_dist = 400
crystal_count = 0 # nope

cshop_open = False # false
cshop_selection = []
cshop_pb = [[1, 10, "+20 % firerate", "Firerate"],
            [1, 10, "+20 % damage", "Damage"],
            [1, 10, "+1 health", "Health"],
            [0, 100, "+15 % knockback", "Knockback"],
            [1, 5, "regain 1 health", "Heal"],
            [1, 10, "extend slowtime duration by 0.5s", "Slowtime"],
            [1, 10, "+20 % slowtime regen speed", "Slowtime reg."],
            [1, 10, "+20 % slower time", "Slowtime str."],
            [1, 100, "+10 % magnet range", "Magnet"],
            [1, 500, "+1 enemy pierce", "Piercing"],
            [0, 2000, "unlock shotgun", "Shotgun"],
            [1, 400, "-5° shotgun spread", "SG spread"],
            [1, 1500, "+1 shotgun bullet", "SG bullets"],
            [0, 5000, "unlock rocket launcher", "Rocket"],
            [0, 10000, "buy 1 gun turret", "Gun Turret"],
            [0, 15000, "buy 1 rocket turret", "Rocket Turret"],
            [0, 10000, "buy 1 precision drone", "Kamikadze!"],
            [0, 30000, "unlock laser", "Laser"],
            [0, 50000, "buy 1 laser turret", "Laser turret"],
            [0, 35000, "buy 1 laser drone", "Laser drone"],
            [0, 40000, "buy 1 healer drone", "Healer drone"]] # firerate, damage, health, knockback, heal, slowtime_duration, slowtime_regen, slowtime_strenght, magnet_range, pierce, shotgun, shotgun_precision_angle, shotgun_bullet_number, rocket_launcher, gun_turret, rocket_turret, precision_drone, laser, laser_turret, laser_drone, healer_drone

cshop_possible = [cshop_pb[0], cshop_pb[1], cshop_pb[2], cshop_pb[3], cshop_pb[4], cshop_pb[5], cshop_pb[6], cshop_pb[7]]

cshop_costs = []
cshop_tooltips = []
cshop_selection_int = []
cshop_selection_values = []
cshop_x = 1400
cshop_y = 700
cshop_items = []

slowdown_time = 0
slowdown_limit = 1 #1
slowdown_divider = 2 #2
slowdown_regen = 1
slowdown_active = False

magnet_unlocked = False
piercing_unlocked = False
shotgun_unlocked = False
rocket_unlocked = False
turrets_unlocked = False
laser_unlocked = False
laser_turret_unlocked = False
pdrone_unlocked = False
lhdrone_unlocked = False

shotgun_bought = False
shotgun_precision_angle = 45
shotgun_bullet_number = 3

rocket_bought = False
rocket_damage = 200
rocket_radius = 200

laser_bought = False

enemy_spawn_chance = 600 #600
enemy_id_counter = 1
enemy_arrows = []
arrow_speed = 600

turrets = []
turret_lifetime = 30

gun_turret_delay = 0.5
rocket_turret_delay = 3

gun_turrets_owned = 0
rocket_turrets_owned = 0
laser_turrets_owned = 0

gun_turrets_current = 0
rocket_turrets_current = 0
laser_turrets_current = 0

laser_turrets_strenght = 100

rockets = []

lasers = []

drones = []
drone_enemy_ids = []
orbiting_drones = 0
attacking_drones = 0
orbit_angle = 0
drone_range = 500
drone_healer_progress = 0

wave_started = True # true
wave_health = 0
wave_health_max = 1

current_wave = 0

screen_spawn_block = pygame.Rect(-100, -100, window_width + 100, window_heigth + 100)

# classes
class render_item:
    def __init__(self, item_type, layer, metadata, item_function):
        self.metadata = metadata # all the item data stored in a dictionary
        self.layer = layer # layer, to which should be this item drawn
        self.item_type = item_type # sprite, circle, line, rect

        if item_function == "button": # if it's a button, assign a click event, that triggers set function
            self.click_event = metadata["click_event"]

class timer:
    def __init__(self, time, trigger, step, event):
        self.time = time # active time of running
        self.trigger = trigger # the time, at which the timer sets off
        self.step = step # how much should the timer.time increase (usually 1)
        self.event = event # what happens, when the timer goes off (usually a function)
        self.triggered = False # sets the triggered state to false

# engine functions
def move(item_move, change):
    item_move.rect.x += change(0)
    item_move.rect.y += change(1)

def update_timers(timers, dt):
    for timer in timers:
        timer.time += timer.step*dt
        if timer.time >= timer.trigger and not timer.triggered:
            timer.triggered = True
            timer.event()

def test():
    print("test is working")

# render
def render(to_render):
    window.fill((0, 0, 0))
    for layer in range(layers_current): # goes through every layer; set number of layers at the top in "engine default variables - layers_current"
        for item in to_render: # sprite, rect, line, aaline, circle, text
            if item.layer == layer: # checks if current item is at the set layer, else skips it
                try:
                    if item.item_type == "sprite":
                        window.blit(item.metadata["sprite"], item.metadata["rect"])
                    elif item.item_type == "rect":
                        pygame.draw.rect(window, item.metadata["color"], item.metadata["rect"], item.metadata["width"], item.metadata["border_radius"])
                    elif item.item_type == "line":
                        pygame.draw.line(window, item.metadata["color"], item.metadata["start"], item.metadata["end"], item.metadata["width"])
                    elif item.item_type == "aaline":
                        pygame.draw.aaline(window, item.metadata["color"], item.metadata["start"], item.metadata["end"])
                    elif item.item_type == "circle":
                        pygame.draw.circle(window, item.metadata["color"], item.metadata["center"], item.metadata["radius"], item.metadata["width"])
                    elif item.item_type == "text":
                        if "spec" in item.metadata:
                            if "bgcolor" in item.metadata:
                                text = item.metadata["font"].render(item.metadata["text"], item.metadata["antialias"], item.metadata["color"], item.metadata["bgcolor"])
                                rect = text.get_rect()
                                rect.center = item.metadata["center"]
                                window.blit(text, rect)
                            else:
                                text = item.metadata["font"].render(item.metadata["text"], item.metadata["antialias"], item.metadata["color"])
                                rect = text.get_rect()
                                rect.center = item.metadata["center"]
                                window.blit(text, rect)
                        else:
                            if "bgcolor" in item.metadata:
                                window.blit(item.metadata["font"].render(item.metadata["text"], item.metadata["antialias"], item.metadata["color"], item.metadata["bgcolor"]), item.metadata["rect"])
                            else:
                                window.blit(item.metadata["font"].render(item.metadata["text"], item.metadata["antialias"], item.metadata["color"]), item.metadata["rect"])
                except:
                    print(f"Item '{item.item_type}' in layer {item.layer} couldn't be rendered; check metadata parameters")
    pygame.display.update()

""" # pymunk physics update
def update_physics(dt):
    phys_space.step(dt) """

# class pre-run constructors

# creating player
player = render_item("circle",
                     1,
                     {"color":(255, 255, 255), "center":(100,100), "radius":player_radius, "width":10},
                     None)

crosshair = render_item("line",
                        1,
                        {"color":(255, 255, 255), "start":cross_pos_start, "end":cross_pos_end, "width":16},
                        None)

# player movement
def player_movement():
    global player, vstup, speed, mouse_pos

    player_pos = player.metadata["center"]

    step_pos = (player_pos[0] - mouse_pos[0], player_pos[1] - mouse_pos[1])
    step = (step_pos[0] / (round(clock.get_fps()) + 1), step_pos[1] / (round(clock.get_fps()) + 1))

    player.metadata["center"] = (player_pos[0] - step[0], player_pos[1] - step[1])
    crosshair_movement()

def crosshair_movement():
    global player, cross_pos_start, cross_pos_end

    player_pos = player.metadata["center"]

    # calculate angle in rads from positions
    angle_rads = math.atan2(mouse_pos[1] - player_pos[1], mouse_pos[0] - player_pos[0])

    cross_pos_start = (player_pos[0] + 50 * math.cos(angle_rads), player_pos[1] + 50 * math.sin(angle_rads))

    cross_pos_end = (player_pos[0] + 90 * math.cos(angle_rads), player_pos[1] + 90 * math.sin(angle_rads))

    crosshair.metadata["start"] = cross_pos_start
    crosshair.metadata["end"] = cross_pos_end

def bullet_movement(): # enemy dying also here
    if bullets:
        for bullet in bullets:
            bullet.move()
            bullet.render()
            bullet.enemy_handling()

def laser_handling():
    global wave_health
    for laser in lasers:
        for enemy in enemies:
            enemy_rect = pygame.Rect((enemy.x - enemy.size), (enemy.y - enemy.size), enemy.size * 2, enemy.size * 2)
            if enemy_rect.clipline(laser[0][0], laser[0][1]):
                health_before_hit = enemy.health
                enemy.health -= laser[1] * dt
                wave_health -= laser[1] * dt

                enemy.check_death(laser_strength*dt, health_before_hit)
        
        # render
        to_render.append(render_item("line", 1, {"color":(100, 100, 255), "start":laser[0][0], "end":laser[0][1], "width":5}, None))
    lasers.clear()

def arrow_handling():
    if enemy_arrows:
        for arrow in enemy_arrows:
            arrow.move()
            arrow.check_collision_and_window()
            arrow.render()

def bullet_generation():
    destination = (player.metadata["center"][0] + window_width * math.cos(math.atan2(mouse_pos[1] - player.metadata["center"][1], mouse_pos[0] - player.metadata["center"][0])), player.metadata["center"][1] + window_width * math.sin(math.atan2(mouse_pos[1] - player.metadata["center"][1], mouse_pos[0] - player.metadata["center"][0])))
    bullets.append(Bullet(destination, cross_pos_end, bullet_piercing))

def emeny_arrow_generation(enemy_pos): # need to complete this shis <3
    destination = (enemy_pos[0] + window_width * math.cos(math.atan2(player.metadata["center"][1] - enemy_pos[1], player.metadata["center"][0] - enemy_pos[0])), enemy_pos[1] + window_width * math.sin(math.atan2(player.metadata["center"][1] - enemy_pos[1], player.metadata["center"][0] - enemy_pos[0])))
    enemy_arrows.append(Arrow(destination, enemy_pos))

def shotgun_bullet_generation(angle_precision, number_of_bullets):
    for i in range(number_of_bullets):
        angle = i * (angle_precision / number_of_bullets)
        rel_angle = angle_precision/2-angle
        destination = (player.metadata["center"][0] + window_width * math.cos((math.radians(rel_angle) + math.atan2(mouse_pos[1] - player.metadata["center"][1], mouse_pos[0] - player.metadata["center"][0]))), player.metadata["center"][1] + window_width * math.sin((math.radians(rel_angle) +math.atan2(mouse_pos[1] - player.metadata["center"][1], mouse_pos[0] - player.metadata["center"][0]))))
        bullets.append(Bullet(destination, cross_pos_end, bullet_piercing))

def rocket_bullet_generation():
    rockets.append(Rocket(cross_pos_end, math.atan2(mouse_pos[1] - player.metadata["center"][1], mouse_pos[0] - player.metadata["center"][0]), rocket_damage, rocket_radius, player_rocket_speed))

def laser_generation():
    angle = math.atan2(mouse_pos[1] - player.metadata["center"][1], mouse_pos[0] - player.metadata["center"][0])
    laser_poss = (cross_pos_end, (player.metadata["center"][0] + window_width * math.cos(angle), player.metadata["center"][1] + window_width * math.sin(angle)))
    lasers.append((laser_poss, laser_strength))

def enemy_handling():
    global player, player_health, wave_health

    if enemies:
        for enemy in enemies:
            enemy.move()
            enemy.archer_handling()
            enemy.bomber_handling()
            enemy.render()
            
            if math.hypot(player.metadata["center"][0] - enemy.x, player.metadata["center"][1] - enemy.y) < (player_radius + enemy.size):
                if enemy.type != "enemy_bomber":
                    wave_health -= enemy.health
                    enemy.die()
                    match enemy.type:
                        case "enemy_small": player_health -= 1
                        case "boss_small": player_health -= 2
                        case "boss_guard": player_health -= player_health
                        case "enemy_archer": player_health -= 1
                        case "enemy_runner": player_health -= 1
                        case "enemy_bomber": pass
                        case "enemy_dasher": player_health -= 1

def enemy_generation():
    temp_allow = False
    while not temp_allow:
        temp_pos = (random.randint(-40, window_width//10 + 40), random.randint(-40, window_heigth//10 + 40))
        temp_pos = (temp_pos[0]*10, temp_pos[1]*10)
        if not screen_spawn_block.collidepoint(temp_pos): #(temp_pos[0] > 0 and temp_pos[0] < window_width or temp_pos[1] > 0 and temp_pos[1] < window_heigth):
            temp_allow = True
        else:
            temp_allow = False
    enemies.append(Enemy(temp_pos, enemy_small_health, enemy_small_health, enemy_small_speed, enemy_small_size, enemy_small_crystals, enemy_small_width, enemy_small_color, True))

def boss_generation():
    temp_allow = False
    while not temp_allow:
        temp_pos = (random.randint(-40, window_width//10 + 40), random.randint(-40, window_heigth//10 + 40))
        temp_pos = (temp_pos[0]*10, temp_pos[1]*10)
        if not screen_spawn_block.collidepoint(temp_pos):
            temp_allow = True
        else:
            temp_allow = False
    enemies.append(Enemy(temp_pos, boss_small_health, boss_small_health, boss_small_speed, boss_small_size, boss_small_crystals, boss_small_width, boss_small_color, True))

def guard_generation():
    temp_allow = False
    while not temp_allow:
        temp_pos = (random.randint(-40, window_width//10 + 40), random.randint(-40, window_heigth//10 + 40))
        temp_pos = (temp_pos[0]*10, temp_pos[1]*10)
        if not screen_spawn_block.collidepoint(temp_pos):
            temp_allow = True
        else:
            temp_allow = False
    enemies.append(Enemy(temp_pos, boss_guard_health * 1.4 * current_wave, boss_guard_health * 1.4 * current_wave, boss_guard_speed, boss_guard_size, boss_guard_crystals * 1.2 * current_wave, boss_guard_width, boss_guard_color, True))

def runner_generation():
    temp_allow = False
    while not temp_allow:
        temp_pos = (random.randint(-40, window_width//10 + 40), random.randint(-40, window_heigth//10 + 40))
        temp_pos = (temp_pos[0]*10, temp_pos[1]*10)
        if not screen_spawn_block.collidepoint(temp_pos):
            temp_allow = True
        else:
            temp_allow = False
    enemies.append(Enemy(temp_pos, enemy_runner_health, enemy_runner_health, enemy_runner_speed, enemy_runner_size, enemy_runner_crystals, enemy_runner_width, enemy_runner_color, True))

def archer_generation():
    temp_allow = False
    while not temp_allow:
        temp_pos = (random.randint(-40, window_width//10 + 40), random.randint(-40, window_heigth//10 + 40))
        temp_pos = (temp_pos[0]*10, temp_pos[1]*10)
        if not screen_spawn_block.collidepoint(temp_pos):
            temp_allow = True
        else:
            temp_allow = False
    enemies.append(Enemy(temp_pos, enemy_archer_health, enemy_archer_health, enemy_archer_speed, enemy_archer_size, enemy_archer_crystals, enemy_archer_width, enemy_archer_color, True))

def bomber_generation():
    temp_allow = False
    while not temp_allow:
        temp_pos = (random.randint(-40, window_width//10 + 40), random.randint(-40, window_heigth//10 + 40))
        temp_pos = (temp_pos[0]*10, temp_pos[1]*10)
        if not screen_spawn_block.collidepoint(temp_pos):
            temp_allow = True
        else:
            temp_allow = False
    enemies.append(Enemy(temp_pos, enemy_bomber_health, enemy_bomber_health, enemy_bomber_speed, enemy_bomber_size, enemy_bomber_crystals, enemy_bomber_width, enemy_bomber_color, True))

def turret_handling():
    if turrets:
        for turret in turrets:
            if turret.alive_for >= turret_lifetime:
                turret.die()
            turret.rotate()
            turret.get_target()
            if turret.shoot_delay_current >= turret.shoot_delay_set and enemies:
                turret.shoot_handling()
            turret.render()

            if enemies:
                turret.alive_for += 1*dt
            turret.shoot_delay_current += 1*dt

def drone_handling():
    global orbiting_drones, orbit_angle, attacking_drones, drone_enemy_ids, drone_healer_progress, player_health, player_max_health

    if drones:
        orbiting_drones = 0
        attacking_drones = 0
        drone_enemy_ids.clear()
        orbit_angle += 1*dt
        for drone in drones:
            drone.update_state()
        for drone in drones:
            drone.update_target_pos(drones.index(drone))
            drone.update_movement_angle()
            drone.move()
            drone.attack()
            drone.render()
        
        if drone_healer_progress >= 10 and player_health < player_max_health:
            player_health += 1
            drone_healer_progress = 0

def place_turret(turret_type):
    if turret_type == "gun_turret":
        turrets.append(Turret(player.metadata["center"], turret_type, gun_turret_delay))
    elif turret_type == "rocket_turret":
        turrets.append(Turret(player.metadata["center"], turret_type, rocket_turret_delay))
    elif turret_type == "laser_turret":
        turrets.append(Turret(player.metadata["center"], turret_type, 0))

def rocket_handling():
    if rockets:
        for rocket in rockets:
            rocket.move()
            rocket.check_collision()
            rocket.render()

def particle_handling():
    global explosion_particle_density

    if particles:
        for particle in particles:
            particle.handle_size_and_trans()
            particle.move()
            particle.render()

        if clock.get_fps() > 200:
            explosion_particle_density = 40
        elif clock.get_fps() > 100:
            explosion_particle_density = 20
        else:
            explosion_particle_density = 5

def particle_pure_rendering():
    if particles:
        for particle in particles:
            particle.render()

def player_trail_handling():
    if slowdown_active:
        player_trail.append(player.metadata["center"])
    else:
        try: player_trail.pop(len(player_trail)-1)
        except: pass

    if player_trail:
        for instance in player_trail:
            to_render.append(render_item("circle", 1, {"color":(150, 150, 150), "center":player_trail[player_trail.index(instance)], "width":10, "radius":player_radius}, None))

    if len(player_trail) > 40:
        player_trail.reverse()
        player_trail.pop(40)
        player_trail.reverse()

def crystal_handling():
    if crystals:
        for crystal in crystals:
            crystal.handle_offscreen()
            crystal.handle_after_spawn()
            crystal.handle_angle_adjustment()
            crystal.move()
            crystal.render()

def wave_handling():
    global wave_started, current_wave, cshop_open, particle_density, wave_health, wave_health_max, cshop_possible, cshop_pb, magnet_unlocked, shotgun_unlocked
    if len(enemies) == 0 and len(crystals) == 0 or len(enemies) == 0 and False:
        if wave_started:
            while len(enemies) < (round(current_wave*1.5)):
                enemy_generation()

            if (current_wave+1) >= 6:
                for i in range(round(1.2 * ((current_wave + 1) // 6 ))):
                    runner_generation()

            if (current_wave+1) >= 15:
                for i in range(round(1.2 * ((current_wave + 1) // 10 ))):
                    archer_generation()

            if (current_wave+1) >= 25:
                for i in range(round(1.2 * ((current_wave + 1) // 13 ))):
                    bomber_generation()

            if (current_wave+1) % 10 == 0:
                for i in range(round(1.2 * ((current_wave + 1) // 10))):
                    boss_generation()

            if (current_wave+1) >= 30 and (current_wave+1) % 10 == 0:
                guard_generation()

            wave_started = False

            wave_health_max = 0
            wave_health = 0
            
            for enemy in enemies:
                wave_health_max += enemy.health
            wave_health = wave_health_max

            current_wave += 1
            
            cshop_refresh()
        else:
            cshop_open = True

        # particle reduction
        if current_wave == 8: particle_density = 20
        if current_wave == 14: particle_density = 10
        if current_wave == 30: particle_density = 5
        if current_wave == 50: particle_density = 2
        if current_wave == 70: particle_density = 1

        # cshop item unlocking
        cshop_unlocks()

    if wave_health < 0: # this feels so wrong
        wave_health = 0

def cshop_unlocks():
    global current_wave, cshop_possible, cshop_pb, magnet_unlocked, shotgun_unlocked, piercing_unlocked, rocket_unlocked, turrets_unlocked, laser_unlocked, laser_turret_unlocked, pdrone_unlocked, lhdrone_unlocked
    if current_wave >= 8 and not magnet_unlocked:
        cshop_possible.append(cshop_pb[8])
        magnet_unlocked = True
    if current_wave >= 12 and not piercing_unlocked:
        cshop_possible.append(cshop_pb[9])
        piercing_unlocked = True
    if current_wave >= 20 and not shotgun_unlocked:
        cshop_possible.append(cshop_pb[10])
        cshop_possible.append(cshop_pb[11])
        cshop_possible.append(cshop_pb[12])
        shotgun_unlocked = True
    if current_wave >= 32 and not rocket_unlocked:
        cshop_possible.append(cshop_pb[14])
        rocket_unlocked = True
    if current_wave >= 35 and not turrets_unlocked:
        cshop_possible.append(cshop_pb[14])
        cshop_possible.append(cshop_pb[15])
        turrets_unlocked = True
    if current_wave >= 55 and not pdrone_unlocked:
        cshop_possible.append(cshop_pb[16])
        pdrone_unlocked = True
    if current_wave >= 60 and not laser_unlocked:
        cshop_possible.append(cshop_pb[17])
        laser_unlocked = True
    if current_wave >= 80 and not laser_turret_unlocked:
        cshop_possible.append(cshop_pb[18])
        laser_turret_unlocked = True
    if current_wave >= 85 and not lhdrone_unlocked:
        cshop_possible.append(cshop_pb[19])
        cshop_possible.append(cshop_pb[20])
        lhdrone_unlocked = True

def mouse_handling():
    global slowdown_time, slowdown_limit, slowdown_regen, slowdown_divider, slowdown_active, dt, mouse_changed, mouse_last, spawn_bullet, bullet_spawned, mouse_current_delta, mouse_set_delta, cshop_open

    """ mouse_up = False

    for event in pygame.event.get(): # get active events
        if event.type == pygame.MOUSEBUTTONUP: mouse_up = True """

    if not cshop_open:
        # time slowdown detection
        slowdown_active = False
        if pygame.mouse.get_pressed()[2] and slowdown_time < slowdown_limit:
            slowdown_time += 1*dt
            dt /= slowdown_divider
            slowdown_active = True
        elif slowdown_time - slowdown_regen*dt > 0 and not pygame.mouse.get_pressed()[2]:
            slowdown_time -= slowdown_regen*dt

        if pygame.mouse.get_pressed()[0] and player.metadata["weapon"] == "laser":
            spawn_bullet = True

        if pygame.mouse.get_pressed()[0] and mouse_changed and mouse_current_delta > mouse_set_delta and player.metadata["weapon"] != "laser" or pygame.mouse.get_pressed()[0] and mouse_current_delta > mouse_set_delta and player.metadata["weapon"] != "laser":
            spawn_bullet = True
            bullet_spawned = True
            mouse_current_delta = 0

        mouse_current_delta += 1 * dt

    if pygame.mouse.get_pressed()[0] == mouse_last:
        mouse_changed = False
    else:
        mouse_changed = True
    
    mouse_last = pygame.mouse.get_pressed()[0]

def key_handling():
    global vstup, enemy_spawn_chance, cshop_open, wave_started, r_last, r_changed, place_key_last, place_key_changed, gun_turrets_current, rocket_turrets_current, gun_turrets_owned, rocket_turrets_owned, laser_turrets_current, laser_turrets_owned, crystal_count, debug_enabled
    if vstup[pygame.K_e]: #or random.randint(0, enemy_spawn_chance) == 1:
        enemy_generation()

    if cshop_open and vstup[pygame.K_TAB]:
        cshop_open = False
        wave_started = True

    if cshop_open and vstup[pygame.K_r] and r_changed:
        cshop_refresh()

    # checks, if 'r' is being held
    if vstup[pygame.K_r] == r_last:
        r_changed = False
    else:
        r_changed = True

    r_last = vstup[pygame.K_r]

    # checks if any place key is being held
    if (vstup[pygame.K_1] or vstup[pygame.K_2] or vstup[pygame.K_3] or vstup[pygame.K_4] or vstup[pygame.K_5] or vstup[pygame.K_0] or vstup[pygame.K_F3]) == place_key_last:
        place_key_changed = False
    else:
        place_key_changed = True

    place_key_last = (vstup[pygame.K_1] or vstup[pygame.K_2] or vstup[pygame.K_3] or vstup[pygame.K_4] or vstup[pygame.K_5] or vstup[pygame.K_9] or vstup[pygame.K_0] or vstup[pygame.K_F3])

    # placing of turrets and stuff
    if vstup[pygame.K_1] and place_key_changed and gun_turrets_current < gun_turrets_owned:
        place_turret("gun_turret")
        gun_turrets_current += 1
    elif vstup[pygame.K_2] and place_key_changed and rocket_turrets_current < rocket_turrets_owned:
        place_turret("rocket_turret")
        rocket_turrets_current += 1
    elif vstup[pygame.K_3] and place_key_changed and laser_turrets_current < laser_turrets_owned:
        place_turret("laser_turret")
        laser_turrets_current += 1
    elif vstup[pygame.K_9] and place_key_changed: # cheat - ends wave
        enemies.clear()
    elif vstup[pygame.K_0] and place_key_changed: # cheat - adds 10 000 crysts.
        crystal_count += 10000
    elif vstup[pygame.K_F3] and place_key_changed:
        if debug_enabled:
            debug_enabled = False
        else:
            debug_enabled = True

def render_ui():
    
    # time slowdown bar render
    slowdown_bar = render_item("rect", 6, {"color":(100, 100, 255), "rect":pygame.Rect(10, window_heigth - 30, (window_width-20)-slowdown_time/slowdown_limit * (window_width - 10), 20), "width":0, "border_radius":0}, None)
    to_render.append(slowdown_bar)

    # wave render
    #wavebar - it could show, how far into the wave you are
    try: wave_health_for_bar = wave_health/wave_health_max
    except: wave_health_for_bar = 0
    wave_bar_rect = pygame.Rect(0, 0, wave_health_for_bar * 600, 30)
    wave_bar_rect.center = (window_width//2, 50)
    wave_bar_rect_full = pygame.Rect(0, 0, 600, 30)
    wave_bar_rect_full.center = (window_width//2, 50)
    wave_bar_back = render_item("rect", 6, {"color":(40, 40, 40), "rect":wave_bar_rect_full, "width":0, "border_radius":0}, None)
    wave_bar = render_item("rect", 6, {"color":(255, 0, 0), "rect":wave_bar_rect, "width":0, "border_radius":0}, None)
    to_render.append(wave_bar_back)
    to_render.append(wave_bar)

    wave_text = render_item("text", 6, {"spec":True, "center":(window_width//2, 100), "font":default_font, "text":f"wave: {current_wave}", "antialias":True, "color":(255, 255, 255), "rect":pygame.Rect(window_width - 200, 40, 100, 100)}, None)
    to_render.append(wave_text)

    wave_health_text = render_item("text", 6, {"spec":True, "center":(window_width//2, 50), "font":default_font, "text":str(round(wave_health)), "antialias":True, "color":(255, 255, 255), "rect":pygame.Rect(window_width - 200, 40, 100, 100)}, None)
    to_render.append(wave_health_text)

    # crystal count render
    crystal_icon = render_item("circle", 6, {"color":(200, 200, 255), "center":(window_width - 300, 80), "width":0, "radius":20}, None)
    to_render.append(crystal_icon)

    crystal_counter_text = str(crystal_count)
    crystal_counter_base = render_item("text", 6, {"font":counter_font, "text":"0000000", "antialias":True, "color":(10, 10, 80), "rect":pygame.Rect(window_width - 260, 40, 100, 100)}, None)
    crystal_counter = render_item("text", 6, {"font":counter_font, "text":crystal_counter_text, "antialias":True, "color":(170, 170, 255), "rect":pygame.Rect(window_width - 260, 40, 100, 100)}, None)
    to_render.append(crystal_counter_base)
    to_render.append(crystal_counter)

    # health bar render
    health_icon = render_item("circle", 6, {"color":(100, 255, 100), "center":(window_width - 600, 80), "width":8, "radius":20}, None)
    health_counter = render_item("text", 6, {"font":counter_font, "text":(f"{player_health}/{player_max_health}"), "antialias":True, "color":(170, 255, 170), "rect":pygame.Rect(window_width - 550, 40, 100, 100)}, None)
    to_render.append(health_icon)
    to_render.append(health_counter)

    # place key text render
    if gun_turrets_owned > 0:
        to_render.append(render_item("text", 6, {"spec":True, "center":(150, window_heigth - 80), "font":default_font, "text":f"[1] Gun Turret ({gun_turrets_owned - gun_turrets_current})", "antialias":True, "color":(230, 230, 230), "rect":pygame.Rect(0, 0, 0, 0)}, None))
    if rocket_turrets_owned > 0:
        to_render.append(render_item("text", 6, {"spec":True, "center":(450, window_heigth - 80), "font":default_font, "text":f"[2] Rocket Turret ({rocket_turrets_owned - rocket_turrets_current})", "antialias":True, "color":(230, 230, 230), "rect":pygame.Rect(0, 0, 0, 0)}, None))
    if laser_turrets_owned > 0:
        to_render.append(render_item("text", 6, {"spec":True, "center":(750, window_heigth - 80), "font":default_font, "text":f"[3] Laser Turret ({laser_turrets_owned - laser_turrets_current})", "antialias":True, "color":(230, 230, 230), "rect":pygame.Rect(0, 0, 0, 0)}, None))

    if cshop_open:
        handle_crystal_shop()

def handle_crystal_shop():

    # render background
    cshop_background_rect = pygame.Rect(0, 0, cshop_x, cshop_y)
    cshop_background_rect.center = (window_width//2, window_heigth//2)
    cshop_background_back = render_item("rect", 6, {"color":(30, 30, 30), "rect":cshop_background_rect, "width":0, "border_radius":40}, None)
    cshop_background_front = render_item("rect", 6, {"color":(230, 230, 230), "rect":cshop_background_rect, "width":4, "border_radius":40}, None)

    to_render.append(cshop_background_back)
    to_render.append(cshop_background_front)

    # render shop items
    for item in cshop_items:
        item.clicked() # maybe also updating the cost of items here?
        try:
            item.update_level(cshop_selection_values[cshop_items.index(item)][0], cshop_costs[cshop_items.index(item)]) # this has some problem with the shotgun at pos 1 (out of range) idk
        except:
            """ print(f"'{item.name}' level couldn't be updated") """
            pass
        item.render()

def cshop_refresh():
    cshop_unlocks()

    global cshop_selection, cshop_possible, cshop_selection_values, cshop_selection_int, cshop_tooltips, cshop_costs, knockback_strenght
    cshop_selection_int.clear()
    cshop_selection_int = [random.randint(0, len(cshop_possible)-1), random.randint(0, len(cshop_possible)-1), random.randint(0, len(cshop_possible)-1)]

    print(cshop_selection_int)

    cshop_selection_values.clear()
    cshop_selection.clear()
    cshop_items.clear()
    cshop_tooltips.clear()

    for i in cshop_selection_int:
        match i:
            case 0:
                cshop_selection_values.append(cshop_possible[0])
                cshop_selection.append(cshop_possible[0][3])
                cshop_tooltips.append(cshop_possible[0][2])
            case 1:
                cshop_selection_values.append(cshop_possible[1])
                cshop_selection.append(cshop_possible[1][3])
                cshop_tooltips.append(cshop_possible[1][2])
            case 2:
                cshop_selection_values.append(cshop_possible[2])
                cshop_selection.append(cshop_possible[2][3])
                cshop_tooltips.append(cshop_possible[2][2])
            case 3:
                cshop_selection.append(cshop_possible[3][3])
                if knockback_strenght == 0: 
                    cshop_tooltips.append("unlock knockback")
                    cshop_selection_values.append([0, 100, "unlock knockback"])
                else:
                    cshop_tooltips.append(cshop_possible[3][2])
                    cshop_selection_values.append(cshop_possible[3])
            case 4:
                cshop_selection_values.append(cshop_possible[4])
                cshop_selection.append(cshop_possible[4][3])
                cshop_tooltips.append(cshop_possible[4][2])
            case 5:
                cshop_selection_values.append(cshop_possible[5])
                cshop_selection.append(cshop_possible[5][3])
                cshop_tooltips.append(cshop_possible[5][2])
            case 6:
                cshop_selection_values.append(cshop_possible[6])
                cshop_selection.append(cshop_possible[6][3])
                cshop_tooltips.append(cshop_possible[6][2])
            case 7:
                cshop_selection_values.append(cshop_possible[7])
                cshop_selection.append(cshop_possible[7][3])
                cshop_tooltips.append(cshop_possible[7][2])
            case 8: # magnet - unlockable
                cshop_selection_values.append(cshop_possible[8])
                cshop_selection.append(cshop_possible[8][3])
                cshop_tooltips.append(cshop_possible[8][2])
            case 9: # piercing - unlockable
                cshop_selection_values.append(cshop_possible[9])
                cshop_selection.append(cshop_possible[9][3])
                cshop_tooltips.append(cshop_possible[9][2])
            case 10: # shotgun - unlockable
                if shotgun_bought:
                    cshop_refresh()
                    break
                else:
                    cshop_selection_values.append(cshop_possible[10])
                    cshop_selection.append(cshop_possible[10][3])
                    if cshop_possible[0][0] >= 6 and cshop_possible[1][0] >= 6:
                        cshop_tooltips.append(cshop_possible[10][2])
                    else:
                        cshop_tooltips.append("Min dmg: 6 and min frr: 6")
            case 11: # SG spread - unlockable
                if shotgun_bought:
                    cshop_selection_values.append(cshop_possible[11])
                    cshop_selection.append(cshop_possible[11][3])
                    if shotgun_unlocked:
                        cshop_tooltips.append(cshop_possible[11][2])
                    else:
                        cshop_tooltips.append("Need shotgun! "+cshop_possible[11][2])
                else:
                    cshop_refresh()
                    break
            case 12: # SG bullets - unlockable
                if shotgun_bought:
                    cshop_selection_values.append(cshop_possible[12])
                    cshop_selection.append(cshop_possible[12][3])
                    if shotgun_unlocked:
                        cshop_tooltips.append(cshop_possible[12][2])
                    else:
                        cshop_tooltips.append("Need shotgun! "+cshop_possible[12][2])
                else:
                    cshop_refresh()
                    break
            case 13: # Rocket Launcher - unlockable
                if rocket_bought:
                    cshop_refresh()
                    break
                else:
                    cshop_selection_values.append(cshop_possible[13])
                    cshop_selection.append(cshop_possible[13][3])
                    cshop_tooltips.append(cshop_possible[13][2])
            case 14: # Gun turret - classic buy
                cshop_selection_values.append(cshop_possible[14])
                cshop_selection.append(cshop_possible[14][3])
                cshop_tooltips.append(cshop_possible[14][2])
            case 15: # Rocket turret - classic buy
                cshop_selection_values.append(cshop_possible[15])
                cshop_selection.append(cshop_possible[15][3])
                cshop_tooltips.append(cshop_possible[15][2])
            case 16: # Precision drone - classic buy
                cshop_selection_values.append(cshop_possible[16])
                cshop_selection.append(cshop_possible[16][3])
                cshop_tooltips.append(cshop_possible[16][2])
            case 17: # Laser - unlockable
                if laser_bought:
                    cshop_refresh()
                    break
                else:
                    cshop_selection_values.append(cshop_possible[17])
                    cshop_selection.append(cshop_possible[17][3])
                    cshop_tooltips.append(cshop_possible[17][2])
            case 18: # Laser turret - classic buy
                cshop_selection_values.append(cshop_possible[18])
                cshop_selection.append(cshop_possible[18][3])
                cshop_tooltips.append(cshop_possible[18][2])
            case 19: # Laser drone - classic buy
                cshop_selection_values.append(cshop_possible[19])
                cshop_selection.append(cshop_possible[19][3])
                cshop_tooltips.append(cshop_possible[19][2])
            case 20: # Healer drone - classic buy
                cshop_selection_values.append(cshop_possible[20])
                cshop_selection.append(cshop_possible[20][3])
                cshop_tooltips.append(cshop_possible[20][2])

    print(cshop_selection_values)
    print(cshop_selection)

    cshop_costs = (random.randint(cshop_selection_values[0][1]//1.3, cshop_selection_values[0][1]), random.randint(cshop_selection_values[1][1]//1.3, cshop_selection_values[1][1]), random.randint(cshop_selection_values[2][1]//1.3, cshop_selection_values[2][1]))
    print(cshop_costs)

    cshop_item0 = CShop_Item((window_width//2 - (cshop_x - 20)//3, window_heigth//2), ((cshop_x - 60) // 3, cshop_y - 40), cshop_selection[0], cshop_costs[0], cshop_selection_values[0][0], cshop_tooltips[0], cshop_selection_int[0])
    cshop_item1 = CShop_Item((window_width//2, window_heigth//2), ((cshop_x - 60) // 3, cshop_y - 40), cshop_selection[1], cshop_costs[1], cshop_selection_values[1][0], cshop_tooltips[1], cshop_selection_int[1])
    cshop_item2 = CShop_Item((window_width//2 + (cshop_x - 20)//3, window_heigth//2), ((cshop_x - 60) // 3, cshop_y - 40), cshop_selection[2], cshop_costs[2], cshop_selection_values[2][0], cshop_tooltips[2], cshop_selection_int[2])

    cshop_items.append(cshop_item0)
    cshop_items.append(cshop_item1)
    cshop_items.append(cshop_item2)

# bullet?
class Bullet:
    def __init__(self, destination, position, piercing):
        self.x, self.y = position
        self.dest = destination
        self.piercing = piercing
        self.angle = math.atan2(self.dest[1] - self.y, self.dest[0] - self.x)
        self.player_pos = player.metadata["center"]
        self.mouse_pos = mouse_pos
        self.texture = pygame.Surface((10, 20))
        self.texture.fill(white)
        self.texture = pygame.transform.rotate(self.texture, 30)#-math.degrees(self.angle)
        self.last_enemy_id = 0

    def move(self):
        self.x += math.cos(self.angle) * 1000*dt
        self.y += math.sin(self.angle) * 1000*dt

        # removal of bullet in case of going off the screen
        if self.x > window_width + 100 or self.x < -100 or self.y > window_heigth + 100 or self.y < -100:
            bullets.remove(self)

    def enemy_handling(self):
        global wave_health

        for enemy in enemies:
            if math.hypot(enemy.x - self.x, enemy.y - self.y) < enemy.size and enemy.id != self.last_enemy_id:
                health_before_hit = enemy.health
                hit_current = random.randint(hit_strenght // hit_strenght_divider, hit_strenght)
                enemy.health -= hit_current
                wave_health -= hit_current

                knockback_rads = math.atan2(self.mouse_pos[1] - self.player_pos[1], self.mouse_pos[0] - self.player_pos[0])

                enemy.knockback[0] += (-knockback_strenght * math.cos(knockback_rads))
                enemy.knockback[1] += (-knockback_strenght * math.sin(knockback_rads))

                if self.piercing <= 0:
                    try:
                        bullets.remove(self)
                    except:
                        pass
                else:
                    self.piercing -= 1

                self.last_enemy_id = enemy.id

                enemy.check_death(hit_current, health_before_hit)

    def render(self):
        bullet_rect = pygame.Rect(self.x, self.y, self.texture.get_width(), self.texture.get_height())
        bullet_rect.center = (self.x, self.y)

        # sending current bullet to be rendered
        to_render.append(render_item("sprite", 1, {"sprite":self.texture, "rect":bullet_rect}, None))

class Rocket:
    def __init__(self, position, angle, strenght, radius, speed):
        self.x, self.y = position
        self.speed = speed
        self.angle = angle
        self.strenght = strenght
        self.radius = radius
        self.particle_timer = 0

    def move(self):
        self.x += math.cos(self.angle) * self.speed*dt
        self.y += math.sin(self.angle) * self.speed*dt

        # removal of bullet in case of going off the screen
        if self.x > window_width + 100 or self.x < -100 or self.y > window_heigth + 100 or self.y < -100:
            rockets.remove(self)

        self.particle_timer += 1*dt

    def check_collision(self):
        if enemies:
            for enemy in enemies:
                if math.hypot(enemy.x - self.x, enemy.y - self.y) < enemy.size:
                    self.explode()

    def explode(self):
        Explosion((self.x, self.y), self.radius, self.strenght, 200, 200, "player_shot")
        try: rockets.remove(self)
        except: pass

    def render(self):
        point_two = (self.x - 100 * math.cos(self.angle), self.y - 100 * math.sin(self.angle))
        to_render.append(render_item("line", 3, {"color":(100, 100, 100), "start":(self.x, self.y), "end":point_two, "width":30}, None))

        if self.particle_timer >= 0.2:
            particles.append(Death_Particle(point_two, 0.8, 120, 80, (130, 130, 130)))
            particles.append(Death_Particle(point_two, 0.5, 140, 40, (255, 100, 0)))
            self.particle_timer = 0

class Arrow:
    def __init__(self, destination, enemy_pos):
        self.x, self.y = enemy_pos
        self.dest = destination
        self.angle = math.atan2(self.dest[1] - self.y, self.dest[0] - self.x)
        self.angle_rads = math.radians(self.angle)
    
    def move(self):
        self.x += math.cos(self.angle) * arrow_speed*dt
        self.y += math.sin(self.angle) * arrow_speed*dt

    def check_collision_and_window(self):
        global player_health

        if math.hypot(player.metadata["center"][0] - self.x, player.metadata["center"][1] - self.y) < player_radius:
            player_health -= 1
            for i in range(50):
                particle = Death_Particle((self.x, self.y), .8, 300, 25, (255, 100, 0))
                particles.append(particle)

            try: enemy_arrows.remove(self)
            except: pass

        if self.x < -100 or self.x > window_width + 100 or self.y < -100 or self.y > window_heigth + 100:
            try: enemy_arrows.remove(self)
            except: pass

    def render(self):
        point_two = (self.x - 100 * math.cos(self.angle), self.y - 100 * math.sin(self.angle))
        to_render.append(render_item("line", 1, {"color":(255, 130, 0), "start":(self.x, self.y), "end":point_two, "width":8}, None))

class Explosion:
    def __init__(self, position, radius, strength, speed, size, explosion_type):
        global player_health, wave_health, enemies

        self.x, self.y = position
        self.radius = radius
        self.strength = strength
        self.speed = speed
        self.size = size
        self.type = explosion_type

        if self.type == "player_shot":
            for enemy in enemies:
                if math.hypot(enemy.x - self.x, enemy.y - self.y) < (enemy.size + self.radius):
                    health_before_hit = enemy.health
                    enemy.health -= self.strength
                    wave_health -= self.strength

                    knockback_rads = math.atan2(self.y - enemy.y, self.x - enemy.x)

                    enemy.knockback[0] += (self.strength * 1.2 * math.cos(knockback_rads))
                    enemy.knockback[1] += (self.strength * 1.2 * math.sin(knockback_rads))

                    enemy.check_death(self.strength, health_before_hit)

        elif self.type == "enemy_shot":
            if math.hypot(player.metadata["center"][0] - self.x, player.metadata["center"][1] - self.y) < (player_radius + self.radius):
                player_health -= self.strength // 100

        elif self.type == "bomber_shot":
            for enemy in enemies:
                if math.hypot(enemy.x - self.x, enemy.y - self.y) < (enemy.size + self.radius):
                    health_before_hit = enemy.health
                    enemy.health -= self.strength
                    wave_health -= self.strength

                    knockback_rads = math.atan2(self.y - enemy.y, self.x - enemy.x)

                    enemy.knockback[0] += (self.strength * 1.2 * math.cos(knockback_rads))
                    enemy.knockback[1] += (self.strength * 1.2 * math.sin(knockback_rads))

                    if enemy.type == "enemy_bomber": enemy.health = 0

                    enemy.check_death(self.strength, health_before_hit)

            if math.hypot(player.metadata["center"][0] - self.x, player.metadata["center"][1] - self.y) < (player_radius + self.radius):
                player_health -= self.strength // 100

        # maybe later player knockback?
                
        for i in range(explosion_particle_density):
            particles.append(Death_Particle((self.x, self.y), 1.5, self.speed, self.size, (255, 100, 0)))
            particles.append(Death_Particle((self.x, self.y), 1.5, self.speed, self.size//1.2, (255, 200, 0)))
        for i in range(round(explosion_particle_density/1.3)):
            particles.append(Death_Particle((self.x, self.y), 1.7, random.randint(self.speed//3, self.speed), self.size//4, (100, 100, 100)))

class Death_Particle: # sorry, any particle
    def __init__(self, position, lifetime, speed, size, color):
        self.x, self.y = position
        self.lifetime = lifetime
        self.alive_for = 0
        self.transparency = 1
        self.angle = random.randint(0, 360)
        self.speed = random.randint(speed//3, speed)
        self.size = random.randint(size//4, size)
        self.color = color

    def handle_size_and_trans(self):
        global particles

        self.alive_for += 1*dt
        self.transparency = 1-self.alive_for/self.lifetime
        if 0.9-(self.alive_for/self.lifetime) <= 0:
            particles.remove(self)

    def move(self):
        self.x += math.cos(self.angle) * self.speed*dt
        self.y += math.sin(self.angle) * self.speed*dt

    def render(self):
        to_render.append(render_item("circle", 1, {"color":(round(self.color[0] * self.transparency), round(self.color[1] * self.transparency), round(self.color[2] * self.transparency)), "center":(self.x, self.y), "width":0, "radius":self.size//2}, None))

class Crystal:
    def __init__(self, position, speed):
        self.x, self.y = position
        self.speed = speed
        self.angle = random.randint(0, 360)

    def handle_after_spawn(self):
        if self.speed - self.speed/2*dt > 0.1:
            self.speed -= 1-self.speed/2*dt
        else:
            self.speed = 0

    def handle_angle_adjustment(self):
        global crystal_count

        if math.hypot(player.metadata["center"][0] - self.x, player.metadata["center"][1] - self.y) < crystal_pickup_dist:
            self.angle = math.atan2(player.metadata["center"][1] - self.y, player.metadata["center"][0] - self.x)
            self.speed += 2000 * dt

        if math.hypot(player.metadata["center"][0] - self.x, player.metadata["center"][1] - self.y) < player_radius:
            crystal_count += 1
            crystals.remove(self)

    def handle_offscreen(self):
        if self.x < 0 or self.x > window_width or self.y < 0 or self.y > window_heigth:
            self.angle = math.atan2(window_heigth//2 - self.y, window_width//2 - self.x)
            self.speed = 500

    def move(self):
        self.x += math.cos(self.angle) * self.speed*dt
        self.y += math.sin(self.angle) * self.speed*dt

    def render(self):
        to_render.append(render_item("circle", 3, {"color":(200, 200, 255), "center":(self.x, self.y), "width":0, "radius":10}, None))

class Enemy:
    def __init__(self, position, health, max_health, speed, size, crystal_chance, width, color, drop_crystals):
        global enemy_id_counter, current_wave, boss_guard_health, boss_guard_health_this_effin_wave

        self.x, self.y = position
        self.health = health
        self.max_health = max_health
        self.knockback = [0, 0]
        self.speed = speed
        self.angle = 0
        self.size = size
        self.crystal_chance = crystal_chance
        self.width = width
        self.color = color
        self.id = enemy_id_counter
        self.on_screen = False
        self.drop_crystals = drop_crystals
        enemy_id_counter += 1
        
        boss_guard_health_this_effin_wave = round(current_wave*1.4*boss_guard_health)
        self.bgtew = boss_guard_health_this_effin_wave

        match self.max_health:
            case 100: self.type = "enemy_small"
            case 400: self.type = "boss_small"
            case self.bgtew: # set type and new self.minion_spawn_timer
                self.type = "boss_guard"
                self.minion_spawn_timer = 0
                self.minion_spawn_set = 10
            case 150: self.type ="enemy_archer"
            case 50: self.type = "enemy_runner"
            case 500: self.type = "enemy_bomber"
            case 999: self.type = "enemydasher"

        if self.type == "enemy_archer":
            self.timer = 0

    def move(self):
        on_screen = (self.x < window_width - self.size and self.x > 0 + self.size) and (self.y < window_heigth - self.size and self.y > 0 + self.size)
        in_borders = (self.x > -400 and self.x < window_width + 400 and self.y > -400 and self.y < window_heigth + 400)
        dst_to_player_ctr = math.hypot(player.metadata["center"][0] - self.x, player.metadata["center"][1] - self.y)
        has_knockback = (self.knockback[0] > 1 or self.knockback[1] > 1 or self.knockback[0] < -1 or self.knockback[1] < -1)

        self.angle = math.atan2(player.metadata["center"][1] - self.y, player.metadata["center"][0] - self.x)

        if self.type == "enemy_archer":
            if dst_to_player_ctr >= archer_distancing and in_borders:
                self.move_w_knockback()
            else:
                if on_screen:
                    self.move_back_w_knockback()
                else:
                    self.move_wo_knockback()
                    self.reset_knockback()

        elif has_knockback and in_borders and (not self.type == "boss_guard"):
            self.move_w_knockback()

        else:
            self.move_wo_knockback()

            self.reset_knockback()

        if self.knockback[0] > 0: self.knockback[0] -= 200 * dt
        if self.knockback[0] < 0: self.knockback[0] += 200 * dt
        if self.knockback[1] > 0: self.knockback[1] -= 200 * dt
        if self.knockback[1] < 0: self.knockback[1] += 200 * dt

        if self.type == "boss_guard":
            self.boss_guard_handling()

    def move_w_knockback(self):
        self.x += (math.cos(self.angle) * self.speed * 1/random.randint(1, 4) - self.knockback[0]) * dt
        self.y += (math.sin(self.angle) * self.speed * 1/random.randint(1, 4) - self.knockback[1]) * dt

    def move_back_w_knockback(self):
        self.x += (math.cos(self.angle) * -self.speed//2 * 1/random.randint(1, 4) - self.knockback[0]) * dt
        self.y += (math.sin(self.angle) * -self.speed//2 * 1/random.randint(1, 4) - self.knockback[1]) * dt
        
    def move_wo_knockback(self):
        self.x += (math.cos(self.angle) * self.speed * 1/random.randint(1, 4)) * dt
        self.y += (math.sin(self.angle) * self.speed * 1/random.randint(1, 4)) * dt

    def reset_knockback(self):
        self.knockback = [0, 0]

    def archer_handling(self):
        if self.type == "enemy_archer":
            self.timer += 1*dt
            if self.timer >= archer_shoot_frequency and math.hypot(player.metadata["center"][0] - self.x, player.metadata["center"][1] - self.y) <= archer_shoot_distance:
                self.timer = 0
                emeny_arrow_generation((self.x, self.y))

    def bomber_handling(self):
        global wave_health

        if self.type == "enemy_bomber":
            if math.hypot(player.metadata["center"][0] - self.x, player.metadata["center"][1] - self.y) < (player_radius + self.size) or self.health <= 0:
                self.die()
                wave_health -= self.health
                Explosion((self.x, self.y), bomber_effect_radius, 300, 200, 200, "bomber_shot")

    def boss_guard_handling(self):
        global wave_health

        if self.minion_spawn_timer > self.minion_spawn_set:
            for i in range(10):
                enemy_spawn_angle = random.randint(0, 360)
                enemy_spawn_pos = (self.x + self.size * 1.4 * math.cos(enemy_spawn_angle), self.y + self.size * 1.4 * math.sin(enemy_spawn_angle))
                enemies.append(Enemy(enemy_spawn_pos, boss_small_health, boss_small_health, boss_small_speed, boss_small_size, boss_small_crystals, boss_small_width, boss_small_color, False))
                wave_health += boss_small_health
            
            self.minion_spawn_timer = 0
        self.minion_spawn_timer += 1*dt

    def spawn_crystals(self):
        global crystal_count

        if self.type == "boss_guard":
            for i in range(random.randint(self.crystal_chance//4, self.crystal_chance)):
                crystal_count += 1
        else:
            for i in range(random.randint(self.crystal_chance//4, self.crystal_chance)):
                crystal = Crystal((self.x, self.y), 200)
                crystals.append(crystal)
    
    def spawn_particles(self):
        if self.type == "boss_guard":
            for i in range(boss_guard_particle_density):
                particle = Death_Particle((self.x, self.y), .8, 300, 25, (255, 0, 0))
                particles.append(particle)
        else:
            for i in range(particle_density):
                particle = Death_Particle((self.x, self.y), .8, 300, 25, (255, 0, 0))
                particles.append(particle)

    def check_death(self, hit_current, health_before_hit):
        global wave_health


        if self.health <= 0:
            wave_health += -(health_before_hit - hit_current)
            if self.type == "enemy_bomber":
                pass
            else:
                self.die()

    def die(self):
        self.spawn_particles()
        if self.drop_crystals:
            self.spawn_crystals()
        enemies.remove(self)

    def render(self):

        self.on_screen = (self.x < window_width + self.size and self.x > 0 - self.size) and (self.y < window_heigth + self.size and self.y > 0 - self.size)

        if self.on_screen:
            # draw enemy healthbar
            if self.health < self.max_health:
                healthbar_rect = pygame.Rect(0, 0, (self.health / self.max_health * 2.5 * self.size), 10)
                healthbar_rect.center = (self.x, self.y - 1.5 * self.size)
                healthbar = render_item("rect", 4, {"color":(255, 0, 100), "rect":healthbar_rect, "width":0, "border_radius":0}, None)
                to_render.append(healthbar)

            to_render.append(render_item("circle", 2, {"color":self.color, "center":(self.x, self.y), "radius":self.size, "width":self.width}, None))
        
class CShop_Item:
    def __init__(self, position, size, name, cost, level, tooltip, index):
        self.x, self.y = position
        self.size = size
        self.name = name
        self.cost = cost
        self.level = str(level)
        self.tooltip = tooltip
        self.index = index
        self.cost_text = str(cost)
        self.bought = False
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.rect.center = (self.x, self.y)
        self.name_rect = pygame.Rect(0, 0, self.size[0], 10)
        self.name_rect.center = (self.x, self.y - self.size[1]//2)

    def clicked(self):
        global crystal_count, mouse_set_delta, hit_strenght, player_health, player_max_health, knockback_strenght, slowdown_limit, slowdown_regen, slowdown_divider, crystal_pickup_dist, bullet_piercing, shotgun_precision_angle, shotgun_bullet_number, shotgun_bought, shotgun_unlocked, gun_turrets_owned, rocket_turrets_owned, rocket_bought, laser_bought, laser_turrets_owned

        if not self.bought and crystal_count >= self.cost and self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and mouse_changed:
            if self.index == 4:
                if player_health < player_max_health:
                    self.bought = True
                    crystal_count -= self.cost
                    cshop_possible[self.index][1] = round(cshop_possible[self.index][1] * 1.1)

                    player_health += 1
                else:
                    pass

            elif self.index == 10:
                if not shotgun_bought:
                    if cshop_possible[0][1] >= 6 and cshop_possible[1][1] >= 6:
                        self.bought = True
                        crystal_count -= self.cost

                        player.metadata["weapon"] = "shotgun"
                        cshop_possible[0][0] = 1
                        cshop_possible[0][1] = 400
                        cshop_possible[1][0] = 1
                        cshop_possible[1][1] = 400
                        mouse_set_delta = 0.4
                        hit_strenght = 45

                        shotgun_bought = True
                    
                    else:
                        pass

                else:
                    cshop_refresh()

            elif (self.index == 11 or self.index == 12) and not (shotgun_bought and shotgun_unlocked): # something like a failsafe, but seems useless now
                cshop_refresh()

            elif self.index == 13:
                if not rocket_bought:
                    if cshop_possible[0][1] >= 6 and cshop_possible[1][1] >= 6:
                        self.bought = True
                        crystal_count -= self.cost

                        player.metadata["weapon"] = "rocket"
                        cshop_possible[0][0] = 1
                        cshop_possible[0][1] = 400
                        cshop_possible[1][0] = 1
                        cshop_possible[1][1] = 400
                        mouse_set_delta = 0.4
                        hit_strenght = 45

                        rocket_bought = True
                    
                    else:
                        pass

                else:
                    cshop_refresh()

            elif self.index == 14:
                self.bought = True
                crystal_count -= self.cost
                cshop_possible[self.index][1] = round(cshop_possible[self.index][1] * 1.5)

                gun_turrets_owned += 1

            elif self.index == 15:
                self.bought = True
                crystal_count -= self.cost
                cshop_possible[self.index][1] = round(cshop_possible[self.index][1] * 1.5)

                rocket_turrets_owned += 1

            elif self.index == 16:
                self.bought = True
                crystal_count -= self.cost
                cshop_possible[self.index][1] = round(cshop_possible[self.index][1] * 1.5)

                drones.append(Drone("precision_drone", 500, 550))

            elif self.index == 17:
                if not laser_bought:
                    if cshop_possible[0][1] >= 6 and cshop_possible[1][1] >= 6:
                        self.bought = True
                        crystal_count -= self.cost

                        player.metadata["weapon"] = "laser"
                        cshop_possible[0][0] = 1
                        cshop_possible[0][1] = 400
                        cshop_possible[1][0] = 1
                        cshop_possible[1][1] = 400
                        mouse_set_delta = 0.4
                        hit_strenght = 45

                        laser_bought = True
                    
                    else:
                        pass

                else:
                    cshop_refresh()

            elif self.index == 18:
                self.bought = True
                crystal_count -= self.cost
                cshop_possible[self.index][1] = round(cshop_possible[self.index][1] * 1.5)

                laser_turrets_owned += 1

            elif self.index == 19:
                self.bought = True
                crystal_count -= self.cost
                cshop_possible[self.index][1] = round(cshop_possible[self.index][1] * 1.5)

                drones.append(Drone("laser_drone", 500, 400))

            elif self.index == 20:
                self.bought = True
                crystal_count -= self.cost
                cshop_possible[self.index][1] = round(cshop_possible[self.index][1] * 1.5)

                drones.append(Drone("healer_drone", 500, 400))

            else:
                self.bought = True
                crystal_count -= self.cost

                cshop_possible[self.index][0] += 1
                cshop_possible[self.index][1] = round(cshop_possible[self.index][1] * 1.5)

                match self.index:
                    case 0: mouse_set_delta -= mouse_set_delta/5
                    case 1: hit_strenght += hit_strenght//5
                    case 2: 
                        player_health += 1
                        player_max_health += 1
                    case 3: 
                        if knockback_strenght == 0: knockback_strenght = 40
                        else: knockback_strenght += knockback_strenght/6.6
                    case 4: player_health += 1
                    case 5: slowdown_limit += 0.5
                    case 6: slowdown_regen += slowdown_regen/5
                    case 7: slowdown_divider += slowdown_divider/5
                    case 8: crystal_pickup_dist += crystal_pickup_dist/10
                    case 9: bullet_piercing += 1
                    case 10: # this is useless here; moved to actually buying the SG
                        player.metadata["weapon"] = "shotgun"
                        cshop_possible[0][0] = 1
                        cshop_possible[0][1] = 400
                        cshop_possible[1][0] = 1
                        cshop_possible[1][1] = 400
                        mouse_set_delta = 0.4
                        hit_strenght = 45
                    case 11: shotgun_precision_angle -= 5
                    case 12: shotgun_bullet_number += 1
                    case 13: pass # you can just buy a RL, same thing as with SG
                    case 14: pass # same as heal
                    case 15: pass # yup, same
                    case 16: pass # precision drone just adds one
                    case 17: pass # you can just buy the Laser, same thing as with SG and RL
                    case 18: pass # laser turret, mr smartass
                    case 19: pass # drone go brrr
                    case 20: pass # its late, lemme sleep


    def update_level(self, level, cost):
        self.level = str(level)
        self.cost = cost
        self.cost_text = str(cost)

    def render(self):
        if self.rect.collidepoint(mouse_pos) and not self.bought:
                to_render.append(render_item("rect", 6, {"color":(50, 50, 50), "rect":self.rect, "width":0, "border_radius":10}, None))
        else:
            to_render.append(render_item("rect", 6, {"color":(30, 30, 30), "rect":self.rect, "width":0, "border_radius":10}, None))
        to_render.append(render_item("rect", 6, {"color":(230, 230, 230), "rect":self.rect, "width":4, "border_radius":10}, None))
        if not self.bought:
            # not going through pipeline? ## yes, it is, I modified it <:
            to_render.append(render_item("text", 6, {"spec":True, "center":(self.x, self.y - self.size[1]//2.5), "font":counter_font, "text":self.name, "antialias":True, "color":(230, 230, 230), "rect":self.name_rect}, None))
            to_render.append(render_item("text", 6, {"spec":True, "center":(self.x, self.y - self.size[1]//3.3), "font":default_font, "text":self.tooltip, "antialias":True, "color":(230, 230, 230), "rect":self.name_rect}, None))
            to_render.append(render_item("text", 6, {"spec":True, "center":(self.x, self.y + self.size[1]//4), "font":counter_font, "text":(f"cost: {self.cost_text}"), "antialias":True, "color":(230, 230, 230), "rect":self.name_rect}, None))
            to_render.append(render_item("text", 6, {"spec":True, "center":(self.x, self.y + self.size[1]//2.5), "font":counter_font, "text":(f"lvl: {self.level}"), "antialias":True, "color":(230, 230, 230), "rect":self.name_rect}, None))

class Turret:
    def __init__(self, position, turret_type, shoot_delay_set):
        self.x, self.y = position
        self.type = turret_type
        self.shoot_delay_current = 0
        self.shoot_delay_set = shoot_delay_set
        self.target = (0, 0)
        self.rotation = 0
        self.alive_for = 0

    def rotate(self):
        if enemies:
            target_rotation = math.atan2(self.target[1] - self.y, self.target[0] - self.x)
            if self.type != "laser_turret":
                self.rotation = target_rotation
            else:
                if self.rotation < target_rotation:
                    self.rotation += 1*dt
                else:
                    self.rotation -= 1*dt
        else:
            self.rotation += 1 * dt

    def shoot_handling(self):
        match self.type:
            case "gun_turret": self.shoot_bullet()
            case "rocket_turret": self.shoot_rocket()
            case "laser_turret": self.shoot_laser()

        self.shoot_delay_current = 0

    def get_target(self):
        closest_dist = window_width*10
        if enemies:
            for enemy in enemies:
                if enemy.on_screen:
                    if math.hypot(enemy.x - self.x, enemy.y - self.y) < closest_dist:
                        closest_dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                        self.target = (enemy.x, enemy.y)

    def shoot_bullet(self):
        bullets.append(Bullet(self.target, (self.x, self.y), bullet_piercing))

    def shoot_rocket(self):
        rockets.append(Rocket((self.x, self.y), self.rotation, 100, 150, 500))

    def shoot_laser(self):
        lasers.append((((self.x + 50 * (math.cos(self.rotation)), self.y + 50 * (math.sin(self.rotation))), (self.x + window_width * (math.cos(self.rotation)), self.y + window_width * (math.sin(self.rotation)))), laser_turrets_strenght))

    def die(self):
        global gun_turrets_current, rocket_turrets_current, laser_turrets_current
        match self.type:
            case "gun_turret":
                for i in range(40):
                    bullets.append(Bullet((random.randint(0, window_width), random.randint(0, window_heigth)), (self.x, self.y), bullet_piercing))
                turrets.remove(self)
                gun_turrets_current -= 1
            
            case "rocket_turret":
                Explosion((self.x, self.y), 300, 150, 300, 200, "player_shot")
                turrets.remove(self)
                rocket_turrets_current -= 1

            case "laser_turret":
                for i in range(20):
                    particles.append(Death_Particle((self.x, self.y), 1, 100, 100, (200, 0, 255)))
                turrets.remove(self)
                laser_turrets_current -= 1

    def render(self):
        match self.type:
            case "gun_turret":
                self.render_gturret()
            case "rocket_turret":
                self.render_rturret()
            case "laser_turret":
                self.render_lturret()

        # lifebar render
        lifebar_rect = pygame.Rect(0, 0, ((((turret_lifetime - self.alive_for) / turret_lifetime) * 2.5 * 50)), 10)
        lifebar_rect.center = (self.x, self.y - 1.5 * 45)
        lifebar = render_item("rect", 4, {"color":(255, 255, 255), "rect":lifebar_rect, "width":0, "border_radius":0}, None)
        to_render.append(lifebar)

    def render_gturret(self):
        line_points = []
        for i in range(3):
            line_p = (self.x + 50 * (math.cos((360 / 4 * i) + self.rotation)), self.y + 50 * (math.sin((360 / 4 * i) + self.rotation)))
            line_points.append(line_p)
        
        for i in range(len(line_points)):
            if i < (len(line_points)-1):
                line = render_item("line", 3, {"color":(255, 255, 255), "start":line_points[i], "end":line_points[i+1], "width":10}, None)
            else:
                line = render_item("line", 3, {"color":(255, 255, 255), "start":line_points[i], "end":line_points[0], "width":10}, None)
            to_render.append(line)
        if enemies:
            to_render.append(render_item("aaline", 1, {"color":(0, 255, 0), "start":(self.x, self.y), "end":self.target, "width":16}, None))

    def render_rturret(self):
        line_points = []
        for i in range(3):
            line_p = (self.x + 50 * (math.cos((360 / 4 * i) + self.rotation)), self.y + 50 * (math.sin((360 / 4 * i) + self.rotation)))
            line_points.append(line_p)
        
        for i in range(len(line_points)):
            if i < (len(line_points)-1):
                line = render_item("line", 3, {"color":(255, 200, 0), "start":line_points[i], "end":line_points[i+1], "width":10}, None)
            else:
                line = render_item("line", 3, {"color":(255, 200, 0), "start":line_points[i], "end":line_points[0], "width":10}, None)
            to_render.append(line)
        if enemies:
            to_render.append(render_item("aaline", 1, {"color":(0, 255, 0), "start":(self.x, self.y), "end":self.target, "width":16}, None))

    def render_lturret(self):
        line_points = []
        for i in range(3):
            line_p = (self.x + 50 * (math.cos((360 / 4 * i) + self.rotation)), self.y + 50 * (math.sin((360 / 4 * i) + self.rotation)))
            line_points.append(line_p)
        
        for i in range(len(line_points)):
            if i < (len(line_points)-1):
                line = render_item("line", 3, {"color":(255, 0, 200), "start":line_points[i], "end":line_points[i+1], "width":10}, None)
            else:
                line = render_item("line", 3, {"color":(255, 0, 200), "start":line_points[i], "end":line_points[0], "width":10}, None)
            to_render.append(line)
        if enemies:
            to_render.append(render_item("aaline", 1, {"color":(0, 255, 0), "start":(self.x, self.y), "end":self.target, "width":16}, None))

class Drone:
    def __init__(self, drone_type, drone_range, drone_speed):
        self.x, self.y = player.metadata["center"]
        self.type = drone_type # precision, laser, healer, ?repulsor, ?void
        self.range = drone_range
        self.state = "idle"
        self.speed = drone_speed
        self.precision_speef = drone_speed * 2
        self.target = (0, 0)
        self.target_pos = (0, 0)
        self.move_angle = 0

    def update_state(self):
        global orbiting_drones, attacking_drones, drone_enemy_ids, wave_health, player_health, player_max_health

        if enemies:
            for enemy in enemies:
                if self.type == "precision_drone" and math.hypot(enemy.x - self.x, enemy.y - self.y) <= (enemy.size):
                    self.state = "attack"
                    attacking_drones += 1
                    self.target = (enemy.x, enemy.y)
                    drone_enemy_ids.append(enemy.id)
                    self.pdrone_attack()
                    break

                elif self.type == "healer_drone" and math.hypot(enemy.x - self.x, enemy.y - self.y) < (enemy.size + self.range) and math.hypot(enemy.x - player.metadata["center"][0], enemy.y - player.metadata["center"][1]) < (enemy.size + drone_range) and ((enemy.id not in drone_enemy_ids) or enemy.type == "boss_guard") and player_health < player_max_health:
                    health_before_hit = enemy.health
                    self.state = "attack"
                    attacking_drones += 1
                    self.target = (enemy.x, enemy.y)
                    drone_enemy_ids.append(enemy.id)
                    self.hdrone_attack()
                    enemy.health -= 100*dt
                    wave_health -= 100*dt
                    enemy.check_death(100*dt, health_before_hit)
                    break

                elif math.hypot(enemy.x - self.x, enemy.y - self.y) < (enemy.size + self.range) and math.hypot(enemy.x - player.metadata["center"][0], enemy.y - player.metadata["center"][1]) < (enemy.size + drone_range) and ((enemy.id not in drone_enemy_ids) or enemy.type == "boss_guard") and (self.type != "healer_drone"):
                    self.state = "attack"
                    attacking_drones += 1
                    self.target = (enemy.x, enemy.y)
                    drone_enemy_ids.append(enemy.id)
                    break

                else:
                    self.state = "idle"
                    orbiting_drones += 1
        else:
                    self.state = "idle"
                    orbiting_drones += 1

    def update_target_pos(self, temp_index):
        global orbiting_drones
        """ print(orbiting_drones) """
        """ print(((360 / (orbiting_drones+1)) * temp_index)) """
        if self.state == "idle": # return to orbiting player when idle
            self.target_pos = (player.metadata["center"][0] + 100 * math.cos(((360 / (orbiting_drones/2+1)) * temp_index) + orbit_angle), player.metadata["center"][1] + 100 * math.sin(((360 / (orbiting_drones/2+1)) * temp_index) + orbit_angle))
        elif self.state == "attack":
            if self.type == "precision_drone":
                self.target_pos = self.target
            elif self.type == "laser_drone":
                self.target_pos = (self.target[0] + 100 * math.cos(self.move_angle), self.target[1] + 100 * math.sin(self.move_angle))
            elif self.type == "healer_drone":
                self.target_pos = (self.target[0] + 100 * math.cos(self.move_angle), self.target[1] + 100 * math.sin(self.move_angle))

    def update_movement_angle(self):
        self.move_angle = math.atan2(self.target_pos[1] - self.y, self.target_pos[0] - self.x)

    def move(self):
        self.x += math.cos(self.move_angle) * self.speed*dt
        self.y += math.sin(self.move_angle) * self.speed*dt

    def attack(self):
        if self.state == "attack":
            match self.type:
                case "laser_drone":
                    if math.hypot(self.target[0] - self.x, self.target[1] - self.y) < self.range:
                        lasers.append((((self.x, self.y), self.target), 100))
                case "precision_drone":
                    if math.hypot(self.target[0] - self.x, self.target[1] - self.y) <= 10:
                        self.pdrone_attack()
                case "healer_drone":
                    if math.hypot(self.target[0] - self.x, self.target[1] - self.y) < self.range:
                        """ self.hdrone_attack() """
                        pass

    def pdrone_attack(self):
        Explosion((self.x, self.y), 100, 200, 200, 50, "player_shot")
        self.x, self.y = player.metadata["center"]

    def hdrone_attack(self):
        global drone_healer_progress

        drone_healer_progress += 1*dt

        to_render.append(render_item("line", 3, {"color":(255, 200, 0), "start":(self.x, self.y), "end":self.target, "width":6}, None))

    def render(self):
        match self.type:
            case "precision_drone": self.render_pdrone()
            case "laser_drone": self.render_ldrone()
            case "healer_drone": self.render_hdrone()
        
        if debug_enabled:
            """ to_render.append(render_item("circle", 6, {"color":(0, 255, 0), "center":(self.x, self.y), "radius":self.range, "width":1}, None)) """
            to_render.append(render_item("circle", 6, {"color":(0, 0, 255), "center":player.metadata["center"], "radius":self.range, "width":3}, None))

    def render_pdrone(self):
        line_points = []
        for i in range(3):
            line_p = (self.x + 20 * (math.cos((360 / 4 * i) + self.move_angle)), self.y + 20 * (math.sin((360 / 4 * i) + self.move_angle)))
            line_points.append(line_p)
        
        for i in range(len(line_points)):
            if i < (len(line_points)-1):
                line = render_item("line", 3, {"color":(255, 200, 0), "start":line_points[i], "end":line_points[i+1], "width":6}, None)
            else:
                line = render_item("line", 3, {"color":(255, 200, 0), "start":line_points[i], "end":line_points[0], "width":6}, None)
            to_render.append(line)
        if debug_enabled:
            to_render.append(render_item("aaline", 1, {"color":(0, 255, 0), "start":(self.x, self.y), "end":self.target_pos, "width":16}, None))
            to_render.append(render_item("aaline", 1, {"color":(0, 0, 255), "start":(self.x, self.y), "end":self.target, "width":16}, None))

    def render_ldrone(self):
        line_points = []
        for i in range(3):
            line_p = (self.x + 20 * (math.cos((360 / 4 * i) + self.move_angle)), self.y + 20 * (math.sin((360 / 4 * i) + self.move_angle)))
            line_points.append(line_p)
        
        for i in range(len(line_points)):
            if i < (len(line_points)-1):
                line = render_item("line", 3, {"color":(255, 0, 200), "start":line_points[i], "end":line_points[i+1], "width":6}, None)
            else:
                line = render_item("line", 3, {"color":(255, 0, 200), "start":line_points[i], "end":line_points[0], "width":6}, None)
            to_render.append(line)
        if debug_enabled:
            to_render.append(render_item("aaline", 1, {"color":(0, 255, 0), "start":(self.x, self.y), "end":self.target_pos, "width":16}, None))
            to_render.append(render_item("aaline", 1, {"color":(0, 0, 255), "start":(self.x, self.y), "end":self.target, "width":16}, None))

    def render_hdrone(self):
        line_points = []
        for i in range(3):
            line_p = (self.x + 20 * (math.cos((360 / 4 * i) + self.move_angle)), self.y + 20 * (math.sin((360 / 4 * i) + self.move_angle)))
            line_points.append(line_p)
        
        for i in range(len(line_points)):
            if i < (len(line_points)-1):
                line = render_item("line", 3, {"color":(0, 255, 100), "start":line_points[i], "end":line_points[i+1], "width":6}, None)
            else:
                line = render_item("line", 3, {"color":(0, 255, 100), "start":line_points[i], "end":line_points[0], "width":6}, None)
            to_render.append(line)
        if debug_enabled:
            to_render.append(render_item("aaline", 1, {"color":(0, 255, 0), "start":(self.x, self.y), "end":self.target_pos, "width":16}, None))
            to_render.append(render_item("aaline", 1, {"color":(0, 0, 255), "start":(self.x, self.y), "end":self.target, "width":16}, None))

# game code (if not running from file)
def main():

    # global variables declaration
    global running, dt, to_render, vstup, mouse_pos, mouse_left_click, bullet_spawned, mouse_last, mouse_current_delta, mouse_set_delta, slowdown_time, slowdown_limit, slowdown_divider, slowdown_regen, cshop_open, spawn_bullet, shotgun_precision_angle, shotgun_bullet_number

    player.metadata["weapon"] = "gun" # gun
    cshop_refresh()
    """ for i in range(18):
        turrets.append(Turret((100*(i+1), 500), "gun_turret", 1))
    for i in range(18):
        turrets.append(Turret((100*(i+1), 600), "rocket_turret", 2)) """
    """ for i in range(2):
        drones.append(Drone("laser_drone", 500, 400))
    for i in range(2):
        drones.append(Drone("precision_drone", 500, 550))
    for i in range(2):
        drones.append(Drone("healer_drone", 500, 400)) """
    while running: 
        dt = clock.tick(fps)/1000 # set deltatime
        for event in pygame.event.get(): # get active events
            if event.type == pygame.QUIT:
                running = False
            mouse_pos = pygame.mouse.get_pos() # get mouse position
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_left_click = True
            else:
                mouse_left_click = False

        vstup = pygame.key.get_pressed()
        to_render.clear()
        bullet_spawned = False
        spawn_bullet = False

        mouse_handling()
        key_handling()

        if not cshop_open:

            player_movement()
            player_trail_handling()
            wave_handling()
            bullet_movement()
            laser_handling()
            arrow_handling()
            turret_handling()
            drone_handling()
            rocket_handling()
            enemy_handling()
            crystal_handling()
            particle_handling()
            
            if spawn_bullet:
                if player.metadata["weapon"] == "gun":
                    bullet_generation()
                elif player.metadata["weapon"] == "shotgun":
                    shotgun_bullet_generation(shotgun_precision_angle, shotgun_bullet_number) # 45, 3
                elif player.metadata["weapon"] == "rocket":
                    rocket_bullet_generation()
                elif player.metadata["weapon"] == "laser":
                    laser_generation()
                spawn_bullet = False

            if debug_enabled:
                to_render.append(render_item("aaline", 6, {"color":(255, 0, 0), "start":player.metadata["center"], "end":mouse_pos}, None))
                to_render.append(render_item("circle", 6, {"color":(0, 200, 200), "center":player.metadata["center"], "radius":crystal_pickup_dist, "width":1}, None))
                """ to_render.append(render_item("rect", 6, {"color":(0, 255, 0), "rect":pygame.Rect(mouse_pos[0], mouse_pos[1], player.metadata["center"][0], player.metadata["center"][1]), "width":1, "border_radius":0}, None)) """

        else:
            particle_pure_rendering()

        render_ui()

        fps_text = render_item("text",
                3,
                {"text":str(round(clock.get_fps())), "font":default_font, "antialias":False, "color":(0, 255, 0), "bgcolor":None, "rect":pygame.Rect(100, 10, 50, 50)},
                None)
        to_render.append(fps_text)
        to_render.append(player)
        to_render.append(crosshair)
        
        update_timers(timers, dt) # runs thru every added timer and updates it based on parameters
        """ update_physics(dt) # updates pymunk physics every frame """
        render(to_render) # renders every item added to 'to_render' list onto the game window
				
    pygame.quit()

# program execution
if __name__ == "__main__":
	main()