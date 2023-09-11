from pygame import *
import animation
from settings import PLATFORM_WIDTH, PLATFORM_HEIGHT, PLATFORM_COLOR, \
    ANIMATION_PRINCESS, PATH_BLOCK_PLATFORM, PATH_BLOCK_DIE, SCREEN_START


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load(PATH_BLOCK_PLATFORM)
        self.image.set_colorkey(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load(PATH_BLOCK_DIE)


class Princess(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.bolt_anim = animation.Animation([(anim, 0.8) for anim in ANIMATION_PRINCESS])
        self.bolt_anim.play()

    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.bolt_anim.blit(self.image, SCREEN_START)
