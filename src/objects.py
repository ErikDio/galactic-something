from random import randint, uniform, choice
from models import *

class Objects:
	Asteroids = []
	Player = None
	Bullet = []
	Particle = []
	temp_sprite = []
	Sprites = {}
	Sprites['asteroid3'] = pygame.Surface((72,72))
	Sprites['asteroid2'] = pygame.Surface((42,42))
	Sprites['asteroid1'] = pygame.Surface((22,22))
	Sprites['player'] = pygame.Surface((50,50))
	Sprites['bullet'] = pygame.Surface((4,4))
	for surf in Sprites.values():
		surf.set_colorkey(BLK)
	Modelos.asteroid1(Sprites['asteroid1'])
	Modelos.asteroid2(Sprites['asteroid2'])
	Modelos.asteroid3(Sprites['asteroid3'])
	Modelos.player(Sprites['player'])
	Modelos.bullet(Sprites['bullet'])
	

# ------------------------------------------- Asteroides
class AsteroidHndlr:
	def __init__(self, stage: int, posicao: list, is_tangible = True):
		self.name = "asteroid"
		self.is_tangible = is_tangible
		self.angle = 0
		self.center = None
		self.direction = randint(0, 359)
		self.pos = posicao
		self.stage = stage
		self.sprite = pygame.Surface((0,0))
		self.vel = uniform(0.3, 1) * SPEED
		self.hp = stage
		_n1 = randint(-135, -35)
		_n2 = randint(35, 135)
		self.rot_vel = choice([_n1, _n2])
		if stage == 3:
			self.sprite = Objects.Sprites['asteroid3'].copy()
			self.vel *= 0.75
			self.rot_vel *= 0.75
		if stage == 2:
			self.sprite = Objects.Sprites['asteroid2']
		if stage == 1:
			self.sprite = Objects.Sprites['asteroid1']
			self.vel *= 1.5
			self.rot_vel *= 1.5
		self.raio = sum(self.sprite.get_size())/3.5
		Objects.Asteroids.append(self)


# ------------------------------------------- Player
class PlayerHdlr:
	def __init__(self, angle: int, posicao: list):
		self.name = "player"
		self.center = None
		self.angle = angle
		self.pos = posicao
		self.sprite = Objects.Sprites['player'].copy()
		self.raio = (sum(self.sprite.get_size()))/3.5


# ------------------------------------------- Projétil
class BulletHdlr:
	def __init__(self, angle: int, posicao: list):
		self.name = "bullet"
		self.angle = angle
		self.pos = posicao
		self.sprite = Objects.Sprites['bullet']
		self.lifetime = 0
		Objects.Bullet.append(self)


# ------------------------------------------- Partículas
class ParticleHdlr:
	def __init__(self, posicao: list):
		self.angle = randint(0, 359)
		self.lifetime = uniform(0.25, 1.0)
		self.curlife = 0
		self.vel = uniform(0.5, 1.0) * SPEED
		self.sprite = pygame.Surface((1.5, 1.5))
		self.pos = posicao
		self.sprite.fill(WHT)
		Objects.Particle.append(self)


# ------------------------------------------- Temp Handler
class TempHndlr:
	def __init__(self, spr, posicao: list, obj: Objects):
		self.pos = posicao
		self.sprite = spr
		self.sprite.set_colorkey(BLK)
		self.objeto = obj
		Objects.temp_sprite.append(self)
	def __str__(self):
		return f"pos:{self.pos}.....name:{self.name}.....id:{self.id}"