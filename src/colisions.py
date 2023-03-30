import math
from objects import *
from constants import *
from models import *

pdamaged = False
dmg_cont = 0

def player_hit(dt):
	global pdamaged
	global dmg_cont
	if pdamaged == True:
		if dmg_cont < P_INV_T:
			dmg_cont += dt
			if round(dmg_cont%0.2,1)==0.1:
				Objects.Player.sprite.set_alpha(100)
			elif round(dmg_cont%0.2,1)==0.0:
				Objects.Player.sprite.set_alpha(255)
		else:
			dmg_cont = 0
			Objects.Player.sprite.set_alpha(255)
			pdamaged = False

def colision_chk(target):
	global pdamaged
	for bala in Objects.Bullet:
		for temp in Objects.temp_sprite:
			if (temp.objeto.name == "asteroid" and temp.objeto.is_tangible == True):
				_rect = temp.sprite.get_rect()
				_rect.x = temp.pos[0]
				_rect.y = temp.pos[1]
				if math.dist(bala.pos, (_rect.centerx, _rect.centery)) < temp.objeto.raio:
					damage_ast(temp.objeto)
					bala.lifetime = B_VIDA+1
					break
	_ptemp = Objects.temp_sprite[0]
	_prect = _ptemp.sprite.get_rect()
	_prect.x = _ptemp.pos[0]
	_prect.y = _ptemp.pos[1]
	for temp in Objects.temp_sprite:
		if (temp.objeto.name == "asteroid" and temp.objeto.is_tangible == True):
			_rect = temp.sprite.get_rect()
			_rect.x = temp.pos[0]
			_rect.y = temp.pos[1]
			if not pdamaged and (math.dist((_prect.centerx, _prect.centery), (_rect.centerx, _rect.centery))) < (_ptemp.objeto.raio + temp.objeto.raio):
				pdamaged = True
				Objects.Player.sprite.set_alpha(100)


def damage_ast(asteroide):
	if asteroide.hp <= 0:
		if asteroide.stage > 1:
			asteroide.stage -= 1
			AsteroidHndlr(asteroide.stage, [asteroide.pos[0]-25, asteroide.pos[1]-25])
			AsteroidHndlr(asteroide.stage, [asteroide.pos[0]+25, asteroide.pos[1]+25])
		try:
			Objects.Asteroids.remove(asteroide)
		except:
			print(f"{asteroide} não existe mais???")
	else:
		asteroide.hp -= 1