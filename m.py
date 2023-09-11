import pygame 
import os.path
from blocks import *
from player import *
from settings import WIN_WIDTH, WIN_HEIGHT, DISPLAY, BACKGROUND_COLOR, FPS, FILE_DIR


class Camera:
    def __init__(self, camera_fn, width, height):
        self.camera_fn = camera_fn
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)
    
    def update(self, target):
        self.state = self.camera_fn(self.state, target.rect)


def camera_conf(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = - l + WIN_WIDTH / 2, - t + WIN_HEIGHT / 2

    l = min(0, l)
    l =  max(-(camera.width - WIN_WIDTH), l)
    t = min(0, t)
    t =  max(-(camera.width - WIN_HEIGHT), t)

    return Rect(l, t, w, h)

def load_level():
    global player_x, player_y
    level_file = open('%s/1.txt' % FILE_DIR)
    line = " "
    
    while line[0] != "/":
            line = level_file.readline()
            if line[0] == "[":
                while line[0] != "]":
                    line = level_file.readline()
                    if line[0] != "]":
                        endLine = line.find("|")
                        level.append(line[0: endLine])
            if line[0] != "":
                commands = line.split()
                if len(commands) > 1:
                    if commands[0] == "player":
                        player_x = int(commands[1])
                        player_y = int(commands[2])
                    
def main():
    load_level()
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Mario game")
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color(BACKGROUND_COLOR))

    left = right = up = running = False 

    hero = Player(player_x, player_y)
    entities.add(hero)

    timer = pygame.time.Clock()

    x = y = 0

    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                bd = BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)
            if col == "P":
                pr = Princess(x, y)
                entities.add(pr)
                platforms.append(pr)
                animated_entities.add(pr)

            x += PLATFORM_WIDTH  
        y += PLATFORM_HEIGHT  
        x = 0 

    total_level_width = len(level[0]) * PLATFORM_WIDTH  
    total_level_height = len(level) * PLATFORM_HEIGHT

    camera = Camera(camera_conf, total_level_width, total_level_height)

    while not hero.winner:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit('Quit')
            if event.type == KEYDOWN:
                if event.key == pygame.K_UP:
                    up = True
                if event.key == pygame.K_LEFT:
                    left = True
                if event.key == pygame.K_RIGHT:
                    right = True
                if event.key == pygame.K_LSHIFT:
                    running = True
            
            if event.type == KEYUP:
                if event.key == pygame.K_UP:
                    up = False
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_LSHIFT:
                    running = False
            

        screen.blit(bg, SCREEN_START)
        
        animated_entities.update()
        camera.update(hero)
        hero.update(left, right, up , running, platforms)

        for entity in entities:
            screen.blit(entity.image, camera.apply(entity))
        
        timer.tick(FPS)
        pygame.display.update()


level =[]
platforms = []
entities = pygame.sprite.Group()
animated_entities = pygame.sprite.Group()

if __name__ == "__main__":
    main()

# https://github.com/justmayori/some_Mariogame



