# ------------------------------------------- Bibliotecas
import pygame
from random import randint

from models import *
from constants import *
from objects import *
from colisions import *

# ------------------------------------------- Variávieis globais
clock = pygame.time.Clock()

Foward = 0

WINSIZE = (800, 600)
_hitbox = False


# ------------------------------------------- main()
def main():
	pygame.init()
	pygame.display.set_caption("Asteroidinho")
	iniciar_game(pygame.display.set_mode(WINSIZE))


# ------------------------------------------- iniciar_game()
def iniciar_game(screen):
	print(screen.get_size())
	global clock
	global WINSIZE
	global _hitbox
	WINSIZE = pygame.display.get_surface().get_size()
	Objects.Asteroids.append(AsteroidHndlr(3, [500, 300]))
	Objects.Asteroids.append(AsteroidHndlr(1, [400, 200]))
	Objects.Asteroids.append(AsteroidHndlr(3, [100, 100]))
	Objects.Asteroids.append(AsteroidHndlr(3, [300, 100]))
	Objects.Asteroids.append(AsteroidHndlr(2, [600, 100]))
	Objects.Asteroids.append(AsteroidHndlr(1, [700, 100]))
	Objects.Player = PlayerHdlr(0, [400, 300])


# -------------------------------------- Loop while de atualização
	while True:		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYUP and event.key == pygame.K_h:
				_hitbox = False if _hitbox == True else True
				print(_hitbox)
		screen.fill(BLK)
		controls()
		move()
		clear_scr()
		ScreenManager.loop_scr(Objects.Player)
		ScreenManager.sprite_transform(Objects.Player)
		for bala in Objects.Bullet:
			ScreenManager.loop_scr(bala)
		for asteroide in Objects.Asteroids:
			ScreenManager.loop_scr(asteroide)
			ScreenManager.sprite_transform(asteroide)
		colision_chk(screen)
		ScreenManager.update(screen)
		pygame.display.flip()
		pygame.display.set_caption(f"FPS: {int(clock.get_fps())}, Objetos: {len(Objects.temp_sprite)}")
		Objects.temp_sprite.clear()
		clock.tick(60)


# -------------------------------------- Rotates, Draw, and makes the screen "infinite" 
class ScreenManager:
	@staticmethod
	def update(target):
		for objeto in Objects.Bullet:
			target.blit(objeto.sprite, objeto.pos)
		for objeto in Objects.Particle:
			target.blit(objeto.sprite, objeto.pos)
		for objeto in Objects.temp_sprite:
			if _hitbox:
				_rect = objeto.sprite.get_rect()
				_rect.x = objeto.pos[0]
				_rect.y = objeto.pos[1]
				pygame.draw.circle(target, (255,0,0), (_rect.centerx, _rect.centery), objeto.objeto.raio, 1)
			target.blit(objeto.sprite, objeto.pos)

	@staticmethod
	def sprite_transform(target):
		obj_transf = pygame.transform.rotate(target.sprite, target.angle)
		centro = obj_transf.get_rect(center=target.sprite.get_rect(center=tuple(target.pos)).center)
		target.center = centro
		_raio = target.raio*2
		Objects.temp_sprite.append(TempHndlr(obj_transf, [centro.x,centro.y], target))
		if (centro.y < _raio) or (centro.x < _raio) or (centro.y > WINSIZE[1]-_raio) or centro.x > WINSIZE[0]-_raio:
			if centro.y < _raio:
				Objects.temp_sprite.append(TempHndlr(obj_transf, [centro.x, centro.y + WINSIZE[1]], target))
			elif centro.y > WINSIZE[1]-_raio:
				Objects.temp_sprite.append(TempHndlr(obj_transf, [centro.x, centro.y - WINSIZE[1]], target))
			if centro.x < _raio:
				Objects.temp_sprite.append(TempHndlr(obj_transf, [centro.x + WINSIZE[0], centro.y], target))
			elif centro.x > WINSIZE[0]-_raio:
				Objects.temp_sprite.append(TempHndlr(obj_transf, [centro.x - WINSIZE[0], centro.y], target))
			Objects.temp_sprite.append(TempHndlr(obj_transf, [centro.x - WINSIZE[0], centro.y - WINSIZE[1]], target))
			Objects.temp_sprite.append(TempHndlr(obj_transf, [centro.x - WINSIZE[0], centro.y + WINSIZE[1]], target))
			Objects.temp_sprite.append(TempHndlr(obj_transf, [centro.x + WINSIZE[0], centro.y - WINSIZE[1]], target))
			Objects.temp_sprite.append(TempHndlr(obj_transf, [centro.x + WINSIZE[0], centro.y + WINSIZE[1]], target))

	@staticmethod
	def loop_scr(target):
		if target.pos[1] <= 0:
			target.pos[1] = WINSIZE[1] - 1
		elif target.pos[1] >= WINSIZE[1]:
			target.pos[1] = 1
		elif target.pos[0] <= 0:
			target.pos[0] = WINSIZE[0] - 1
		elif target.pos[0] >= WINSIZE[0]:
			target.pos[0] = 1


# ------------------------------------------- Removes bullets
def clear_scr():
	for count, bala in enumerate(Objects.Bullet):
		if bala.lifetime > B_VIDA:
			i = randint(4, 7)
			n = 0
			while n < i:
				Objects.Particle.append(ParticleHdlr([bala.pos[0],bala.pos[1]]))
				n += 1
			del Objects.Bullet[count]
		else:
			bala.lifetime += 1
	for count, particle in enumerate(Objects.Particle):
		if particle.curlife > particle.lifetime:
			del Objects.Particle[count]
		else:
			particle.curlife += 1
	Objects.temp_sprite.clear()

# ------------------------------------------- Cálculos
def x_sin(angle: int):
	return math.sin(math.radians(angle))


def y_cos(angle: int):
	return math.cos(math.radians(angle))


# ------------------------------------------- Rotação
def rotate(angle):
	Objects.Player.angle += angle
	if Objects.Player.angle < 0:
		Objects.Player.angle = 359
	elif Objects.Player.angle == 359:
		Objects.Player.angle = 0


# ------------------------------------------- Movimento
def move():
	if Foward != 0:
		Objects.Player.pos[0] -= (P_VEL*Foward)*(x_sin(Objects.Player.angle))
		Objects.Player.pos[1] -= (P_VEL*Foward)*(y_cos(Objects.Player.angle))
	if Objects.Bullet:
		for bala in Objects.Bullet:
			bala.pos[0] -= B_VEL * (x_sin(bala.angle))
			bala.pos[1] -= B_VEL * (y_cos(bala.angle))
	if Objects.Particle:
		for particula in Objects.Particle:
			particula.pos[0] -= particula.vel * (x_sin(particula.angle))
			particula.pos[1] -= particula.vel * (y_cos(particula.angle))
	if Objects.Asteroids:
		for asteroide in Objects.Asteroids:
			asteroide.pos[0] -= asteroide.vel*(x_sin(asteroide.direction))
			asteroide.pos[1] -= asteroide.vel*(y_cos(asteroide.direction))
			asteroide.angle += asteroide.rot_vel
			if asteroide.angle > 359:
				asteroide.angle -= 359


# ------------------------------------------- Atira
def shoot():
	global B_DELAY
	cur_time = pygame.time.get_ticks()
	if cur_time - B_DELAY >= 200:
		Objects.Bullet.append(BulletHdlr(Objects.Player.angle, list([Objects.Player.pos[0] - (30 * x_sin(Objects.Player.angle)), Objects.Player.pos[1] - 30 * y_cos(Objects.Player.angle)]), (4, 4)))
		B_DELAY = cur_time


# ------------------------------------------- Controles
def controls():
	global Foward
	global _hitbox
	tecla = pygame.key.get_pressed()
	if tecla[pygame.K_LEFT] or tecla[pygame.K_a]: rotate(+3)
	if tecla[pygame.K_RIGHT] or tecla[pygame.K_d]: rotate(-3)
	if tecla[pygame.K_SPACE]: shoot()
	if tecla[pygame.K_UP] or tecla[pygame.K_w]: Foward = 1
	elif tecla[pygame.K_DOWN] or tecla[pygame.K_s]: Foward = -1
	else: Foward = 0

# ------------------------------------------- Inicia
if __name__ == '__main__':
	main()
