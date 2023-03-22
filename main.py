# ------------------------------------------- Bibliotecas
import pygame
from random import randint

from modelos import *
from constantes import *
from objetos import *
from colisions import *

# ------------------------------------------- Variávieis globais
clock = pygame.time.Clock()

Foward = 0

Winsize = (800, 600)
_hitbox = False


# ------------------------------------------- main()
def main():
	pygame.init()
	pygame.display.set_caption("Asteroidinho")
	iniciar_game(pygame.display.set_mode(Winsize))


# ------------------------------------------- iniciar_game()
def iniciar_game(tela):
	print(tela.get_size())
	global clock
	global Winsize
	Winsize = pygame.display.get_surface().get_size()
	Objetos.Asteroides.append(AsteroidHndlr(3, [500, 300]))
	Objetos.Asteroides.append(AsteroidHndlr(1, [400, 200]))
	Objetos.Asteroides.append(AsteroidHndlr(3, [100, 100]))
	Objetos.Asteroides.append(AsteroidHndlr(3, [300, 100]))
	Objetos.Asteroides.append(AsteroidHndlr(2, [600, 100]))
	Objetos.Asteroides.append(AsteroidHndlr(1, [700, 100]))
	Objetos.Player = PlayerHdlr(0, [400, 300])

	while True:		# -------------------------------------- Loop while de atualização
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		tela.fill(BLK)
		controles()
		move()
		limpar()
		ScreenManager.loop_scr(Objetos.Player)
		ScreenManager.transformar(Objetos.Player)
		for bala in Objetos.Bala:
			ScreenManager.loop_scr(bala)
		for asteroide in Objetos.Asteroides:
			ScreenManager.loop_scr(asteroide)
			ScreenManager.transformar(asteroide)
		colision_chk(tela)
		ScreenManager.atualizar(tela)
		pygame.display.flip()
		pygame.display.set_caption(f"FPS: {int(clock.get_fps())}, Objetos: {len(Objetos.temp_sprite)}")
		Objetos.temp_sprite.clear()
		clock.tick(60)

class ScreenManager:
	@staticmethod
	def atualizar(target):
		for objeto in Objetos.Bala:
			target.blit(objeto.sprite, objeto.pos)
		for objeto in Objetos.Particula:
			target.blit(objeto.sprite, objeto.pos)
		for objeto in Objetos.temp_sprite:
			if objeto.objeto.name == "asteroide" and _hitbox:
				_rect = objeto.sprite.get_rect()
				_rect.x = objeto.pos[0]
				_rect.y = objeto.pos[1]
				pygame.draw.circle(target, (255,0,0), (_rect.centerx, _rect.centery), objeto.objeto.raio, 1)
			target.blit(objeto.sprite, objeto.pos)

	@staticmethod
	def transformar(target):
		obj_transf = pygame.transform.rotate(target.sprite, target.angle)
		centro = obj_transf.get_rect(center=target.sprite.get_rect(center=tuple(target.pos)).center)
		target.centro = centro
		Objetos.temp_sprite.append(TempHndlr(obj_transf, [centro.x,centro.y], target))
		if (centro.y < 100) or (centro.x < 100) or (centro.y > Winsize[1]-100) or centro.x > Winsize[0]-100:
			if centro.y < 100:
				Objetos.temp_sprite.append(TempHndlr(obj_transf, [centro.x, centro.y + Winsize[1]], target))
			elif centro.y > Winsize[1]-100:
				Objetos.temp_sprite.append(TempHndlr(obj_transf, [centro.x, centro.y - Winsize[1]], target))
			if centro.x < 100:
				Objetos.temp_sprite.append(TempHndlr(obj_transf, [centro.x + Winsize[0], centro.y], target))
			elif centro.x > Winsize[0]-100:
				Objetos.temp_sprite.append(TempHndlr(obj_transf, [centro.x - Winsize[0], centro.y], target))
			Objetos.temp_sprite.append(TempHndlr(obj_transf, [centro.x - Winsize[0], centro.y - Winsize[1]], target))
			Objetos.temp_sprite.append(TempHndlr(obj_transf, [centro.x - Winsize[0], centro.y + Winsize[1]], target))
			Objetos.temp_sprite.append(TempHndlr(obj_transf, [centro.x + Winsize[0], centro.y - Winsize[1]], target))
			Objetos.temp_sprite.append(TempHndlr(obj_transf, [centro.x + Winsize[0], centro.y + Winsize[1]], target))

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
		if bala.lifetime > B_VIDA:
			i = randint(4, 7)
			n = 0
			while n < i:
				Objetos.Particula.append(ParticleHdlr([bala.pos[0],bala.pos[1]]))
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

# ------------------------------------------- Cálculos
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
			#print(len(Objetos.Particula))
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
	global B_DELAY
	cur_time = pygame.time.get_ticks()
	if cur_time - B_DELAY >= 200:
		Objetos.Bala.append(ProjetilHdlr(Objetos.Player.angle, list([Objetos.Player.pos[0] - (30 * x_sin(Objetos.Player.angle)), Objetos.Player.pos[1] - 30 * y_cos(Objetos.Player.angle)]), (4, 4)))
		B_DELAY = cur_time
		#print(len(Objetos.Bala))


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