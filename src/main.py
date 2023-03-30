# ------------------------------------------- Lib
import pygame
from random import randint

from models import *
from constants import *
from objects import *
from colisions import *
from spawn import *


# ------------------------------------------- Variables
Clock = pygame.time.Clock()
Foward = 0
_hitbox = False
dt = 0

# ------------------------------------------- Initialize
def main():
	pygame.init()
	pygame.display.set_caption("Asteroidinho")
	start_game(pygame.display.set_mode(WINSIZE))


# ------------------------------------------- Starts the game
def start_game(screen):
	print(screen.get_size())
	global Clock
	global WINSIZE
	global _hitbox
	global dt
	WINSIZE = pygame.display.get_surface().get_size()
	Objects.Player = PlayerHdlr(0, [400, 300])


# -------------------------------------- Loop while de atualização
	while True:		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYUP and event.key == pygame.K_h:
				_hitbox = False if _hitbox == True else True
		dt = round(Clock.tick(FPS) / 1000.0, 4)
		screen.fill(BLK)
		controls()
		move()
		clear_scr()
		spawn_hdlr(dt)
		ScreenManager.loop_scr(Objects.Player)
		ScreenManager.sprite_transform(Objects.Player)
		for bala in Objects.Bullet:
			ScreenManager.loop_scr(bala)
		for asteroide in Objects.Asteroids:
			ScreenManager.loop_scr(asteroide)
			ScreenManager.sprite_transform(asteroide)
		colision_chk(screen)
		player_hit(dt)
		ScreenManager.update(screen)
		pygame.display.flip()
		pygame.display.set_caption(f"FPS: {int(Clock.get_fps())}, Objetos: {len(Objects.temp_sprite)}")
		Objects.temp_sprite.clear()

# -------------------------------------- Screen Manager
class ScreenManager:
	@staticmethod
	def update(target): #---------- Draw Sprites
		for objeto in Objects.Bullet:
			target.blit(objeto.sprite, objeto.pos)
		for objeto in Objects.Particle:
			target.blit(objeto.sprite, objeto.pos)
		for objeto in Objects.temp_sprite:
			if _hitbox:
				_rect = objeto.sprite.get_rect()
				_rect.x,_rect.y = objeto.pos
				pygame.draw.circle(target, (255,0,0), (_rect.centerx, _rect.centery), objeto.objeto.raio, 1)
			target.blit(objeto.sprite, objeto.pos)

	@staticmethod
	def sprite_transform(target): #---------- Rotate sprites and loop the corners
		obj_transf = pygame.transform.rotate(target.sprite, target.angle)
		centro = obj_transf.get_rect(center=target.sprite.get_rect(center=tuple(target.pos)).center)
		target.center = centro
		TempHndlr(obj_transf, [centro.x,centro.y], target)
		_raio = target.raio*2
		if (centro.y < _raio) or (centro.x < _raio) or (centro.y > WINSIZE[1]-_raio) or centro.x > WINSIZE[0]-_raio:
			if centro.y < _raio:
				TempHndlr(obj_transf, [centro.x, centro.y + WINSIZE[1]], target)
			elif centro.y > WINSIZE[1]-_raio:
				TempHndlr(obj_transf, [centro.x, centro.y - WINSIZE[1]], target)
			if centro.x < _raio:
				TempHndlr(obj_transf, [centro.x + WINSIZE[0], centro.y], target)
			elif centro.x > WINSIZE[0]-_raio:
				TempHndlr(obj_transf, [centro.x - WINSIZE[0], centro.y], target)
			TempHndlr(obj_transf, [centro.x - WINSIZE[0], centro.y - WINSIZE[1]], target)
			TempHndlr(obj_transf, [centro.x - WINSIZE[0], centro.y + WINSIZE[1]], target)
			TempHndlr(obj_transf, [centro.x + WINSIZE[0], centro.y - WINSIZE[1]], target)
			TempHndlr(obj_transf, [centro.x + WINSIZE[0], centro.y + WINSIZE[1]], target)

	@staticmethod
	def loop_scr(target):
		if target.pos[1] <= 0:
			target.pos[1] += WINSIZE[1]
		elif target.pos[1] >= WINSIZE[1]:
			target.pos[1] -= WINSIZE[1]
		elif target.pos[0] <= 0:
			target.pos[0] += WINSIZE[0]
		elif target.pos[0] >= WINSIZE[0]:
			target.pos[0] -= WINSIZE[0]


# ------------------------------------------- Removes bullets
def clear_scr():
	global dt
	for count, bala in enumerate(Objects.Bullet):
		if bala.lifetime > B_VIDA:
			i = randint(4, 7)
			n = 0
			while n < i:
				ParticleHdlr([bala.pos[0],bala.pos[1]])
				n += 1
			del Objects.Bullet[count]
		else:
			bala.lifetime += dt
	for count, particle in enumerate(Objects.Particle):
		if particle.curlife > particle.lifetime:
			del Objects.Particle[count]
		else:
			particle.curlife += dt
	Objects.temp_sprite.clear()

# ------------------------------------------- Cálculos
def x_sin(angle: int):
	return math.sin(math.radians(angle))


def y_cos(angle: int):
	return math.cos(math.radians(angle))


# ------------------------------------------- Rotação
def rotate(angle):
	Objects.Player.angle += angle*dt
	if Objects.Player.angle < 0:
		Objects.Player.angle = 359
	elif Objects.Player.angle == 359:
		Objects.Player.angle = 0


# ------------------------------------------- Movimento
def move():
	global dt
	if Foward != 0:
		Objects.Player.pos[0] -= (P_VEL * Foward) * dt * (x_sin(Objects.Player.angle))
		Objects.Player.pos[1] -= (P_VEL * Foward) * dt * (y_cos(Objects.Player.angle))
	if Objects.Bullet:
		for bala in Objects.Bullet:
			bala.pos[0] -= B_VEL * dt * (x_sin(bala.angle))
			bala.pos[1] -= B_VEL * dt * (y_cos(bala.angle))
	if Objects.Particle:
		for particula in Objects.Particle:
			particula.pos[0] -= particula.vel * dt * (x_sin(particula.angle))
			particula.pos[1] -= particula.vel * dt * (y_cos(particula.angle))
	if Objects.Asteroids:
		for asteroide in Objects.Asteroids:
			asteroide.pos[0] -= asteroide.vel * dt * (x_sin(asteroide.direction))
			asteroide.pos[1] -= asteroide.vel * dt * (y_cos(asteroide.direction))
			asteroide.angle += asteroide.rot_vel * dt
			if asteroide.angle > 359:
				asteroide.angle -= 359


# ------------------------------------------- Atira
def shoot():
	global B_DELAY
	cur_time = pygame.time.get_ticks()
	if cur_time - B_DELAY >= 200:
		BulletHdlr(Objects.Player.angle, list([Objects.Player.pos[0] - (30 * x_sin(Objects.Player.angle)), Objects.Player.pos[1] - 30 * y_cos(Objects.Player.angle)]))
		B_DELAY = cur_time


# ------------------------------------------- Controles
def controls():
	global Foward
	global _hitbox
	tecla = pygame.key.get_pressed()
	if tecla[pygame.K_LEFT] or tecla[pygame.K_a]: rotate(180)
	if tecla[pygame.K_RIGHT] or tecla[pygame.K_d]: rotate(-180)
	if tecla[pygame.K_SPACE]: shoot()
	if tecla[pygame.K_UP] or tecla[pygame.K_w]: Foward = 1
	elif tecla[pygame.K_DOWN] or tecla[pygame.K_s]: Foward = -1
	else: Foward = 0

# ------------------------------------------- Inicia
if __name__ == '__main__':
	main()