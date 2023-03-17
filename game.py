# ------------------------------------------- Bibliotecas
import pygame
import operator
import math
from random import randint, uniform
# ------------------------------------------- Variávieis globais
blk = (0, 0, 0)
wht = (255, 255, 255)
clock = pygame.time.Clock()
vel = 2
velin = 2.0
maxspd = 5.0
velat = 0.0
velinc = 0.1
Foward = 0
Shoot_delay = 0
Shoot_life = 150
Winsize = (800, 600)
Centro = None
raio = 43
_hitbox = False

# ------------------------------------------- main()
def main():
	pygame.init()
	pygame.display.set_caption("Asteroidinho")
	iniciar_game(pygame.display.set_mode(Winsize))


class Objetos:
	Asteroides = []
	Player = None
	Bala = []
	Particula = []
	temp_sprite = []


# ------------------------------------------- iniciar_game()
def iniciar_game(tela):
	print(tela.get_size())
	global clock
	global Centro
	global Winsize
	Winsize = pygame.display.get_surface().get_size()

	Objetos.Asteroides.append(AsteroidHndlr((70, 70), [500, 300], 3))
	Objetos.Asteroides.append(AsteroidHndlr((70, 70), [400, 200], 3))
	Objetos.Asteroides.append(AsteroidHndlr((70, 70), [100, 100], 3))
	Objetos.Asteroides.append(AsteroidHndlr((70, 70), [300, 100], 3))
	Objetos.Asteroides.append(AsteroidHndlr((70, 70), [600, 100], 3))
	Objetos.Asteroides.append(AsteroidHndlr((70, 70), [700, 100], 3))
	Objetos.Player = PlayerHdlr(0, [400, 300])

	while True:		# -------------------------------------- Loop while de atualização
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		tela.fill(blk)
		controles()
		move()
		limpar()
		ScreenManager.loop_scr(Objetos.Player)
		ScreenManager.transformar(Objetos.Player, "player", 0)
		for bala in Objetos.Bala:
			ScreenManager.loop_scr(bala)
		for spr_id, asteroide in enumerate(Objetos.Asteroides):
			ScreenManager.loop_scr(asteroide)
			ScreenManager.transformar(asteroide, "asteroide", spr_id)
		colision_chk()
		ScreenManager.atualizar(tela)
		pygame.display.flip()
		pygame.display.set_caption(f"FPS: {int(clock.get_fps())}, Objetos: {len(Objetos.temp_sprite)}")
		Objetos.temp_sprite.clear()
		clock.tick(60)


def colision_chk():
	for contador, bala in enumerate(Objetos.Bala):
		#for count, asteroid in enumerate(Objetos.Asteroides):
		#	if math.dist(bala.pos, asteroid.pos) < raio:
		#		damage_ast(count)
		#		del Objetos.Bala[contador]
		#		break
		for temp in Objetos.temp_sprite:
			if temp.name == "asteroide":
				_rect = temp.sprite.get_rect()
				_rect.x = temp.pos[0]
				_rect.y = temp.pos[1]
				if math.dist(bala.pos, (_rect.centerx, _rect.centery)) < raio:
					damage_ast(temp.id)
					bala.lifetime = Shoot_delay+1
					break


def damage_ast(ast_id):
	if Objetos.Asteroides[ast_id].hp <= 0:
		del Objetos.Asteroides[ast_id]
	else:
		Objetos.Asteroides[ast_id].hp -= 1


class ScreenManager:
	@staticmethod
	def atualizar(target):
		for objeto in Objetos.Bala:
			target.blit(objeto.sprite, objeto.pos)
		for objeto in Objetos.Particula:
			target.blit(objeto.sprite, objeto.pos)
		for objeto in Objetos.temp_sprite:
			if objeto.name == "asteroide" and _hitbox:
				_rect = objeto.sprite.get_rect()
				_rect.x = objeto.pos[0]
				_rect.y = objeto.pos[1]
				pygame.draw.circle(target, (255,0,0), (_rect.centerx, _rect.centery), raio,1)
			target.blit(objeto.sprite, objeto.pos)

	@staticmethod
	def transformar(target, nome, spr_id):
		obj_transf = pygame.transform.rotate(target.sprite, target.angle)
		centro = obj_transf.get_rect(center=target.sprite.get_rect(center=tuple(target.pos)).center)
		target.centro = centro
		Objetos.temp_sprite.append(TempHndlr(obj_transf, [centro[0],centro[1]], nome, spr_id))
		if (centro[1] < 100) or (centro[0] < 100) or (centro[1] > Winsize[1]-100) or centro[0] > Winsize[0]-100:
			if centro[1] < 100:
				Objetos.temp_sprite.append(TempHndlr(obj_transf, [centro[0], centro[1] + Winsize[1]], nome, spr_id))
			elif centro[1] > Winsize[1]-100:
				Objetos.temp_sprite.append(TempHndlr(obj_transf, [centro[0], centro[1] - Winsize[1]], nome, spr_id))
			if centro[0] < 100:
				Objetos.temp_sprite.append(TempHndlr(obj_transf, [centro[0] + Winsize[0], centro[1]], nome, spr_id))
			elif centro[0] > Winsize[0]-100:
				Objetos.temp_sprite.append(TempHndlr(obj_transf, [centro[0] - Winsize[0], centro[1]], nome, spr_id))
			Objetos.temp_sprite.append(TempHndlr(obj_transf, [centro[0] - Winsize[0], centro[1] - Winsize[1]], nome, spr_id))
			Objetos.temp_sprite.append(TempHndlr(obj_transf, [centro[0] - Winsize[0], centro[1] + Winsize[1]], nome, spr_id))
			Objetos.temp_sprite.append(TempHndlr(obj_transf, [centro[0] + Winsize[0], centro[1] - Winsize[1]], nome, spr_id))
			Objetos.temp_sprite.append(TempHndlr(obj_transf, [centro[0] + Winsize[0], centro[1] + Winsize[1]], nome, spr_id))

	@staticmethod
	def loop_scr(target):
		if target.pos[1] <= 0:
			target.pos[1] = Winsize[1] - 1
		elif target.pos[1] >= Winsize[1]:
			target.pos[1] = 1
		elif target.pos[0] <= 0:
			target.pos[0] = Winsize[0] - 1
		elif target.pos[0] >= Winsize[0]:
			target.pos[0] = 1


# ------------------------------------------- Limpar sprites
def limpar():
	for count, bala in enumerate(Objetos.Bala):
		if bala.lifetime > Shoot_life:
			i = randint(4, 7)
			n = 0
			while n < i:
				Objetos.Particula.append(ParticleHdlr(bala.pos))
				n += 1
			del Objetos.Bala[count]
		else:
			bala.lifetime += 1
	for count, particula in enumerate(Objetos.Particula):
		if particula.curlife > particula.lifetime:
			del Objetos.Particula[count]
		else:
			particula.curlife += 1
	Objetos.temp_sprite.clear()


# ------------------------------------------- Asteroides
class AsteroidHndlr:
	def __init__(self, tamanho: tuple, posicao: list, hp: int):
		self.angle = 0
		self.center = None
		self.direction = randint(0, 359)
		self.pos = posicao
		self.sprite = pygame.Surface(tamanho)
		self.sprite.set_colorkey(blk)
		Modelos.asteroid2(self.sprite)
		self.rot_vel = uniform(-1.0, 1.0)
		self.vel = uniform(0.3, 1)
		self.hp = hp


# ------------------------------------------- Temp Handler
class TempHndlr:
	def __init__(self, spr, posicao: list, name: str, spr_id: int):
		self.pos = posicao
		self.sprite = spr
		self.sprite.set_colorkey(blk)
		self.name = name
		self.id = spr_id
	def __str__(self):
		return f"pos:{self.pos}.....name:{self.name}.....id:{self.id}"


# ------------------------------------------- Player
class PlayerHdlr:
	def __init__(self, angulo: int, posicao: list):
		self.angle = angulo
		self.pos = posicao
		self.sprite = pygame.Surface((50, 50))
		self.sprite.set_colorkey(blk)
		Modelos.nave(self.sprite)


# ------------------------------------------- Projétil
class ProjetilHdlr:
	def __init__(self, angulo: int, posicao: list, tamanho: tuple):
		self.angle = angulo
		self.pos = posicao
		self.sprite = pygame.Surface(tamanho)
		self.sprite.set_colorkey(blk)
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
		self.sprite = pygame.Surface((1, 1))
		self.pos = list(posicao)
		self.sprite.fill(wht)


# ------------------------------------------- Modelos e Cálculos
class Modelos:
	@staticmethod
	def nave(target):
		pygame.draw.polygon(target, wht, [[0, 50], [25, 0], [50, 50], [25, 35]], 1)

	@staticmethod
	def bala(target):
		pygame.draw.circle(target, wht, (2, 2), 1, 0)

	@staticmethod
	def asteroid1(target):
		pygame.draw.polygon(target, wht, [[10, 10], [10, 0]], 1)

	@staticmethod
	def asteroid2(target):
		pygame.draw.polygon(target, wht, [[0, 10], [40, 0], [70, 10], [50, 30], [60, 50], [20, 70], [0, 50]], 1)

	@staticmethod
	def asteroid3(target):
		pygame.draw.polygon(target, wht, [[10, 0], [40, 10], [30, 20], [40, 30], [30, 40], [20, 30], [0, 20]], 1)


def x_sin(angulo: int):
	return math.sin(math.radians(angulo))


def y_cos(angulo: int):
	return math.cos(math.radians(angulo))


# ------------------------------------------- Rotação
def rotaciona(angulo):
	Objetos.Player.angle += angulo
	if Objetos.Player.angle < 0:
		Objetos.Player.angle = 359
	elif Objetos.Player.angle == 359:
		Objetos.Player.angle = 0


# ------------------------------------------- Movimento
def move():
	if Foward != 0:
		Objetos.Player.pos[0] -= (vel*Foward)*(x_sin(Objetos.Player.angle))
		Objetos.Player.pos[1] -= (vel*Foward)*(y_cos(Objetos.Player.angle))
	if Objetos.Bala:
		for bala in Objetos.Bala:
			bala.pos[0] -= bala.const_vel * (x_sin(bala.angle))
			bala.pos[1] -= bala.const_vel * (y_cos(bala.angle))
	if Objetos.Particula:
		for particula in Objetos.Particula:
			print(len(Objetos.Particula))
			particula.pos[0] -= particula.vel * (x_sin(particula.angle))
			particula.pos[1] -= particula.vel * (y_cos(particula.angle))
	if Objetos.Asteroides:
		for asteroide in Objetos.Asteroides:
			asteroide.pos[0] -= asteroide.vel*(x_sin(asteroide.direction))
			asteroide.pos[1] -= asteroide.vel*(y_cos(asteroide.direction))
			asteroide.angle += asteroide.rot_vel
			if asteroide.angle > 359:
				asteroide.angle -= 359


# ------------------------------------------- Atira
def atirar():
	global Shoot_delay
	cur_time = pygame.time.get_ticks()
	if cur_time - Shoot_delay >= 200:
		Objetos.Bala.append(ProjetilHdlr(Objetos.Player.angle, list([Objetos.Player.pos[0] - (30 * x_sin(Objetos.Player.angle)), Objetos.Player.pos[1] - 30 * y_cos(Objetos.Player.angle)]), (4, 4)))
		Shoot_delay = cur_time
		print(len(Objetos.Bala))


# ------------------------------------------- Controles
def controles():
	global Foward
	global _hitbox
	tecla = pygame.key.get_pressed()
	if tecla[pygame.K_h]: _hitbox = (True if _hitbox==False else False)
	if tecla[pygame.K_LEFT] or tecla[pygame.K_a]: rotaciona(+3)
	if tecla[pygame.K_RIGHT] or tecla[pygame.K_d]: rotaciona(-3)
	if tecla[pygame.K_SPACE]: atirar()
	if tecla[pygame.K_UP] or tecla[pygame.K_w]: Foward = 1
	elif tecla[pygame.K_DOWN] or tecla[pygame.K_s]: Foward = -1
	else: Foward = 0


# ------------------------------------------- Inicia
main()