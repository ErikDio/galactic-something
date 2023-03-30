from random import randint

from objects import *
from constants import *

_spawning = []

class Spawning:
    def __init__(self, asteroid: Objects.Asteroids):
        global _spawning
        self._object = asteroid
        self.original_vel = asteroid.vel
        self.alpha = 0
        asteroid.vel = 0
        _spawning.append(self)

def spawn_meteor():
    global _spawning
    AsteroidHndlr(3, [randint(0,WINSIZE[0]), randint(0,WINSIZE[1])], False)
    Spawning(Objects.Asteroids[-1])
    Objects.Asteroids[-1].sprite.set_alpha(0)
    
def spawn_hdlr(dt):
    global _spawning
    if not _spawning:
        if len(Objects.Asteroids) < 10:
            spawn_meteor()
    else:
        for asteroid in _spawning:
            asteroid.alpha += 75 * dt
            if round(asteroid.alpha) <= 255:
                asteroid._object.sprite.set_alpha(asteroid.alpha)
            if asteroid._object.vel < asteroid.original_vel:
                asteroid._object.vel += (asteroid.original_vel*dt)/4         
            elif asteroid._object.is_tangible == False and asteroid.alpha >= 255 and asteroid._object.vel >= asteroid.original_vel:
                asteroid._object.vel += (asteroid.original_vel*dt)/4
                asteroid._object.is_tangible = True
                _spawning.remove(asteroid)