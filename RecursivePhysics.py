

'''
█   █████████████████   ██████████████████   ████████████████████████████   ███████████████████████████
█   ████████████  ███   ████  ████████████   ██  ████████████████████████   ████  █████████████████████
█   █   █   ███████    █  ████████   █████   █████     █   ████   █████    █  ████████   █████   █   ██
█   ██   ██   █   ███   ███   ██   ██   ██   █   ██████   ███   ██   ████   ███   ██   ██   ███   ██   
█   ██   ██   █   ███   ███   █   ███   ██   █   ████   ████   ███   ████   ███   █   ████   ██   ██   
█   ██   ██   █   ███   █ █   █   ███   ██   █   ███   █████   ███   ████   █ █   ██   ██   ███   ██   
█   █    ██   █   ████   ██   ███   █    █   █   █         ███   █    ████   ██   ████   █████    ██   
███████████████████████████████████████████████████████████████████████████████████████████████████████
'''



import pygame 
import sys 
import random 
import time 
import math 

screen_height = 700 
screen_width = 1200 

moveable_objects_list = [] 
immovable_objects_list = [] 
affected_by_gravity_list = [] 
dampable_objects_list = [] 
projectile_objects_list = [] 
player_movement_velocity = 10 
max_player_velocity = 50 
downward_max_player_velocity = 1000 
player_jump_height = 1000  
player_maximum_jumpheight = 100 
unit_weight = 1 
in_air_multiplier = 1.10 
gravity_strength = 9 
damping_quality = -5 
everything = [] 
file_location = (__file__).removesuffix("Alone Together.py") 
default_image = pygame.image.load(file_location + "Object Image Files\\Game_Block.png") 


up = [1,0,0,0] 
down = [0,0,1,0] 
right = [0,0,0,1] 
left = [0,1,0,0] 

pygame.init() 
game_display = pygame.display.set_mode((screen_width,screen_height)) 
game_clock = pygame.time.Clock() 
fps = 60 


'''
████     ███████████████████████████████████████████████████     ██████   ██████████████████████████████████   ████████
██  ████   ███████████████████████████████████████████████   ████   ███   █████████   ██████████████████████   ████████
█  ██████████████   █████    █   █   █████   ███████████   ████████   █   ████████████████   ████████    █    █  ██████
█   ███████████   ██   ███   ██  ██   ██  ███   ████████   ████████   █   █   █████   ██  ███   ███   ██████   ████████
█   ███      █   ███   ███   ██  ██   █         ████████   ████████   █   ███   ███   █         ██   ███████   ████████
██   ████  ███   ███   ███   ██  ██   █  █████████████████   █████   ██   ███   ███   █  ██████████   ██████   █ ██████
███      ███████   █    █    ██  ██   ███     ██████████████     ██████   █   █████   ███     ███████    ████   ███████
█████████████████████████████████████████████████████████████████████████████████    ██████████████████████████████████
'''


class game_object(): 
    def __init__(self,size,position,sprite_list,moveable,affected_by_gravity,is_player,is_projectile,initial_movements,dampable,special_function): 
        everything.append(self) 
        self.position = position 
        self.size = size 
        self.tracking = None 
        self.player = is_player 
        self.projectile = is_projectile 
        self.sprite_list = sprite_list 
        self.movements = initial_movements 
        self.dampable = dampable 
        self.last_on_ground_state = False 
        if self.projectile: 
            projectile_objects_list.append(self) 
        if self.dampable: 
            dampable_objects_list.append(self) 
        if affected_by_gravity: 
            affected_by_gravity_list.append(self) 
        self.moveable = moveable 
        if self.moveable: 
            moveable_objects_list.append(self) 
        else: 
            immovable_objects_list.append(self) 
        self.current_sprite = pygame.transform.scale(self.sprite_list[0],self.size) 
        self.update_collision_rect() 
        self.on_ground = True 
        self.special_function = special_function 

    def update_collision_rect(self): 
        self.collision_rect = self.current_sprite.get_rect(topleft = self.position) 
        self.collision_rect.w = self.current_sprite.get_width() 
        self.collision_rect.h = self.current_sprite.get_height() 

    def check_collisions(self): 
        for object in moveable_objects_list+immovable_objects_list: 
            if ((self.collision_rect.colliderect(object.collision_rect)) and (self != object)): 
                return object 
        return False 
    
    def move(self,movements): 

        weight = unit_weight 

        if movements[0] == 0: 
            weight = in_air_multiplier 
        
        for i in range(0,math.ceil(movements[0]/10)): 
            self.move_up() 
            collision = True 
            while collision: 
                collision = self.check_collisions() 
                if collision == False: 
                    pass 
                elif collision.moveable == False: 
                    self.move(down) 
                elif ((self.projectile and collision.player) or (self.player and collision.projectile)): 
                    game_exit()  
                else: 
                    collision.move(up) 
                    
        for i in range(0,math.ceil(weight*movements[1]/10)): 
            self.move_left() 
            collision = True 
            while collision: 
                collision = self.check_collisions() 
                if collision == False: 
                    pass 
                elif collision.moveable == False: 
                    self.move(right) 
                elif (self.projectile and collision.player) or (self.player and collision.projectile): 
                    game_exit()  
                else: 
                    collision.move(left) 
                    
        for i in range(0,math.ceil(movements[2]/10)): 
            self.move_down() 
            collision = True 
            while collision: 
                collision = self.check_collisions() 
                if collision == False: 
                    pass 
                elif collision.moveable == False: 
                    self.move(up) 
                elif (self.projectile and collision.player) or (self.player and collision.projectile): 
                    game_exit()  
                else: 
                    collision.move(down) 
                    
        for i in range(0,math.ceil(weight*movements[3]/10)): 
            self.move_right() 
            collision = True 
            while collision: 
                collision = self.check_collisions() 
                if collision == False: 
                    pass 
                elif collision.moveable == False: 
                    self.move(left) 
                elif (self.projectile and collision.player) or (self.player and collision.projectile): 
                    game_exit()  
                else: 
                    collision.move(right) 
                    
    def move_up(self): 
        self.position[1] -= 1 
        self.update_collision_rect() 

    def move_left(self): 
        self.position[0] -= 1 
        self.update_collision_rect() 

    def move_down(self): 
        self.position[1] += 1 
        self.update_collision_rect() 

    def move_right(self): 
        self.position[0] += 1 
        self.update_collision_rect() 


'''  
████     ███████████████████████████████████████████████        ███████████████████████████████   █████████████████████████████████████████
██  ████   █████████████████████████████████████████████   ████████████████████████████████████   ████  ███████████████████████████████████
█  ██████████████   █████    █   █   █████   ███████████   ███████   ██   █   █   ██████    █    █  ████████   █████   █   ████     ███████
█   ███████████   ██   ███   ██  ██   ██  ███   ████████       ███   ██   ██   ██   ██   ██████   ███   ██   ██   ███   ██   █   ██████████
█   ███      █   ███   ███   ██  ██   █         ████████   ███████   ██   ██   ██   █   ███████   ███   █   ████   ██   ██   ███    ███████
██   ████  ███   ███   ███   ██  ██   █  ███████████████   ███████   ██   ██   ██   ██   ██████   █ █   ██   ██   ███   ██   █████   ██████
███      ███████   █    █    ██  ██   ███     ██████████   █████████      █    ██   ████    ████   ██   ████   █████    ██   █      ███████
███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
''' 


def process_special_functions(game_objects_list): 
    for object in game_objects_list: 
        object.special_function(object) 

def game_close_check(No_Variable): 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            game_exit()  
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                game_exit()  

def apply_gravity(listofobjectstoapplygravityto): 
    for object in listofobjectstoapplygravityto: 
        if object.on_ground == False: 
            object.movements[2] += gravity_strength  
        elif object.last_on_ground_state == False: 
            object.movements[0] = 0 
            object.movements[2] = 0 
        else: 
            object.movements[2] = 0 

def draw_to_screen_and_tick_the_clock(listofobjectstodrawtothescreen): 
    game_display.fill((0,0,0,255)) 
    for object in listofobjectstodrawtothescreen: 
        game_display.blit(object.current_sprite,object.position) 
    pygame.display.update() 
    game_clock.tick(fps) 

def move_objects(listofobjectstomove): 
    for object in listofobjectstomove:  
        object.move(object.movements) 

def apply_damping(listofobjectstodampthevelocitiesof): 
    for object in listofobjectstodampthevelocitiesof: 
        for i in range(0,4): 
            if object.movements[i] != 0: 
                object.movements[i] += damping_quality 

def on_ground_checks(listofobjectstocheck): 
    for object in listofobjectstocheck: 
        object.last_on_ground_state = object.on_ground  
        object.move_down() 
        if object.check_collisions(): 
            object.on_ground = True 
        else: 
            object.on_ground = False 
        object.move_up() 

def game_exit(): 
    pygame.quit() 
    sys.exit() 

def move_up_max(object): 
    if object.on_ground: 
        for i in range(0,100): 
            object.move([5,0,0,0]) 

def enable_camera_complete(self): 
    offsetx = - self.position[0] + screen_width/2 
    offsety = - self.position[1] + screen_height/2 
    for object in moveable_objects_list+immovable_objects_list: 
        object.position = [offsetx+object.position[0],offsety+object.position[1]] 
        object.update_collision_rect()  

def get_unit_sign(integer_value): 
    return integer_value/abs(integer_value) 


'''
███      ██████████████████████████████████████████████   ███████        ███████████████████████████████   █████████████████████████████████████████
█   ████   ██████████████████████████████  ████████████   ███████   ████████████████████████████████████   ████  ███████████████████████████████████
██   ███████  █   ██████   ████████    ████████   █████   ███████   ███████   ██   █   █   ██████    █    █  ████████   █████   █   ████     ███████
████   █████  ██   ███  ███   ███   ████   ██   ██   ██   ███████       ███   ██   ██   ██   ██   ██████   ███   ██   ██   ███   ██   █   ██████████
███████   ██  ███   █         ██   █████   █   ███   ██   ███████   ███████   ██   ██   ██   █   ███████   ███   █   ████   ██   ██   ███    ███████
█   ████   █   █   ██  ██████████   ████   █   ███   ██   ███████   ███████   ██   ██   ██   ██   ██████   █ █   ██   ██   ███   ██   █████   ██████
███      ███   ████████     ███████    █   ███   █    █   ███████   █████████      █    ██   ████    ████   ██   ████   █████    ██   █      ███████
████████████   █████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
'''

def process_player_movements(player): 

    keypressed = pygame.key.get_pressed()     

    if keypressed[pygame.K_x]: 
        minimum_distance = 0 
        for object in moveable_objects_list: 
            distance = calculate_distance(player,object) 
            if distance < minimum_distance: 
                projectile_object = object 
                minimum_distance = distance 

        projectile_object.special_function = projectile_logic 

    if keypressed[pygame.K_w] and player.on_ground: 
        player.movements[0] = min(player.movements[0] + player_jump_height,player_maximum_jumpheight)  
        player.direction = "0" 
    if keypressed[pygame.K_s]: 
        player.movements[2] = min(player.movements[2] + player_movement_velocity,downward_max_player_velocity)  
        player.direction = "2" 
    if keypressed[pygame.K_a]: 
        player.movements[1] = min(player.movements[1] + player_movement_velocity,max_player_velocity)  
        player.direction = "1" 
    if keypressed[pygame.K_d]: 
        player.movements[3] = min(player.movements[3] + player_movement_velocity,max_player_velocity)  
        player.direction = "3" 

def do_nothing(object): 
    pass 

#def 



player = game_object([25,75],[100,100],[default_image],True,True,True,False,[0,0,0,0],True,process_player_movements) 
box = game_object([100, 100],[500, 100], [default_image],True,True,False,False,[0,0,0,0],False,do_nothing) 

'''
████     ███████████████████████████████████████████████   ████████████████████████████████████████████
██  ████   █████████████████████████████████████████████   ████████████████████████████████████████████
█  ██████████████   █████    █   █   █████   ███████████   ███████████   ████████   █████  █   ████████
█   ███████████   ██   ███   ██  ██   ██  ███   ████████   █████████   ██   ███   ██   ██  ██   ███████
█   ███      █   ███   ███   ██  ██   █         ████████   ████████   ████   █   ████   █  ███   ██████
██   ████  ███   ███   ███   ██  ██   █  ███████████████   █████████   ██   ███   ██   ██   █   ███████
███      ███████   █    █    ██  ██   ███     ██████████          ████   ████████   █████   ███████████
█████████████████████████████████████████████████████████████████████████████████████████   ███████████
'''  

### The below is a demo 

running = True 

player.jumping = False 
player.direction = 3 

for line in open(file_location + "Game Objects File.txt","r"): #All game objects, such as the floor, cieling, platforms, player, and moveable objects must be stored in a seperate file, inputted here. A game_objects file has been included in the repository. 
    eval(line) 

not_on_ground = 0 

while (running): 
    game_close_check(None) 
    on_ground_checks(moveable_objects_list) 
    apply_gravity(affected_by_gravity_list) 
    apply_damping(dampable_objects_list) 
    process_special_functions(everything) 
    move_objects(moveable_objects_list) 
    enable_camera_complete(player) 
    draw_to_screen_and_tick_the_clock(everything) 

