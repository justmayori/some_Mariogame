import os

# mario.py
WIN_WIDTH, WIN_HEIGHT = 800, 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = '#000000'
FPS = 60
SCREEN_START = (0, 0)
FILE_DIR = os.path.dirname(__file__)
FILE_PATH = '%s/1.txt' % FILE_DIR

ICON_DIR = os.path.dirname(__file__)

# blocks.py
PLATFORM_WIDTH, PLATFORM_HEIGHT, PLATFORM_COLOR = 32, 32, '#000000'

ANIMATION_PRINCESS = [('%s/blocks/princess_l.png' % ICON_DIR), ('%s/blocks/princess_r.png' % ICON_DIR)]
PATH_BLOCK_PLATFORM = '%s/blocks/platform.png' % ICON_DIR
PATH_BLOCK_DIE = '%s/blocks/dieBlock.png' % ICON_DIR

# player.py
MOVE_SPEED = 7
MOVE_EXTRA_SPEED = 2.5
WIDTH, HEIGHT, COLOR = 22, 32, '#888888'
JUMP_POWER, JUMP_EXTRA_POWER, GRAVITY = 10, 1, 0.25
ANIMATION_DELAY, ANIMATION_SUPER_SPEED_DELAY = 0.1, 0.05

PLATFORM_IMAGE = "%s/blocks/platform.png" % ICON_DIR

ANIMATION_LEFT = [('%s/mario/l1.png' % ICON_DIR),
                  ('%s/mario/l2.png' % ICON_DIR),
                  ('%s/mario/l3.png' % ICON_DIR),
                  ('%s/mario/l4.png' % ICON_DIR),
                  ('%s/mario/l5.png' % ICON_DIR)
                  ]

ANIMATION_RIGHT = [('%s/mario/r1.png' % ICON_DIR),
                   ('%s/mario/r2.png' % ICON_DIR),
                   ('%s/mario/r3.png' % ICON_DIR),
                   ('%s/mario/r4.png' % ICON_DIR),
                   ('%s/mario/r5.png' % ICON_DIR)
                   ]

ANIMATION_JUMP = [('%s/mario/j.png' % ICON_DIR, ANIMATION_DELAY)]
ANIMATION_JUMP_LEFT = [('%s/mario/jl.png' % ICON_DIR, ANIMATION_DELAY)]
ANIMATION_JUMP_RIGHT = [('%s/mario/jr.png' % ICON_DIR, ANIMATION_DELAY)]
ANIMATION_STAY = [('%s/mario/0.png' % ICON_DIR, ANIMATION_DELAY)]

PLAYING, PAUSED, STOPPED = 'playing', 'paused', 'stopped'

