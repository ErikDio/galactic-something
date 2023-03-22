from random import randint, uniform
from modelos import *

class Objetos:
	Asteroides = []
	Player = None
	Bala = []
	Particula = []
	temp_sprite = []

# ------------------------------------------- Asteroides
class AsteroidHndlr:
	def __init__(self, stage: int, posicao: list):
		self.name = "asteroide"
		self.angle = 0
		self.center = None
		self.direction = randint(0, 359)
		self.pos = posicao
		self.stage = stage
		self.sprite = pygame.Surface((0,0))
		self.vel = uniform(0.3, 1)
		self.hp = 0
		self.rot_vel = uniform(-1.0, 1.0)
		if stage == 3:
			self.sprite = pygame.Surface((72,72))
			self.sprite.set_colorkey(BLK)
			Modelos.asteroid3(self.sprite)
			self.hp = 3
			self.vel *= 0.75
			self.rot_vel *= 0.75
		if stage == 2:
			self.sprite = pygame.Surface((42,42))
			self.sprite.set_colorkey(BLK)
			Modelos.asteroid2(self.sprite)
			self.hp = 2
		if stage == 1:
			self.sprite = pygame.Surface((22,22))
			self.sprite.set_colorkey(BLK)
			Modelos.asteroid1(self.sprite)
			self.hp = 1
			self.vel *= 1.5
			self.rot_vel *= 1.5
		self.raio = sum(self.sprite.get_size())/3.5


# ------------------------------------------- Player
class PlayerHdlr:
	def __init__(self, angulo: int, posicao: list):
		self.name = "player"
		self.angle = angulo
		self.pos = posicao
		self.sprite = pygame.Surface((50, 50))
		self.sprite.set_colorkey(BLK)
		Modelos.nave(self.sprite)
		self.raio = (sum(self.sprite.get_size()))/3.5


# ------------------------------------------- Projétil
class ProjetilHdlr:
	def __init__(self, angulo: int, posicao: list, tamanho: tuple):
		self.name = "bala"
		self.angle = angulo
		self.pos = posicao
		self.sprite = pygame.Surface(tamanho)
		self.sprite.set_colorkey(BLK)
		self.const_vel = 3
		self.lifetime = 0
		Modelos.bala(self.sprite)


# ------------------------------------------- Partículas
class ParticleHdlr:
	def __init__(self, posicao: list):
		self.angle = randint(0, 359)
		self.lifetime = randint(15, 60)
		self.curlife = 0
		self.vel = uniform(0.5, 1.5)
		self.sprite = pygame.Surface((1.5, 1.5))
		self.pos = posicao
		self.sprite.fill(WHT)


# ------------------------------------------- Temp Handler
class TempHndlr:
	def __init__(self, spr, posicao: list, obj: Objetos):
		self.pos = posicao
		self.sprite = spr
		self.sprite.set_colorkey(BLK)
		self.objeto = obj
	def __str__(self):
		return f"pos:{self.pos}.....name:{self.name}.....id:{self.id}"