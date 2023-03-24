import math
from objetos import *
from constantes import *
from modelos import *

def colision_chk(target):
	global pdamaged
	global dmg_cont
	if pdamaged == True:
		if dmg_cont < inv_frames:
			#print(dmg_cont)
			dmg_cont += 1
			if dmg_cont%20 == 0:
				Objetos.Player.sprite.fill(BLK)
				Modelos.nave(Objetos.Player.sprite, GRE)
			elif dmg_cont%20 == 10:
				Objetos.Player.sprite.fill(BLK)
				Modelos.nave(Objetos.Player.sprite, WHT)
		else:
			dmg_cont = 0
			Objetos.Player.sprite.fill(BLK)
			Modelos.nave(Objetos.Player.sprite, WHT)
			pdamaged = False
	for contador, bala in enumerate(Objetos.Bala):
		for temp in Objetos.temp_sprite:
			if (temp.objeto.name == "asteroide"):
				_rect = temp.sprite.get_rect()
				_rect.x = temp.pos[0]
				_rect.y = temp.pos[1]
				if math.dist(bala.pos, (_rect.centerx, _rect.centery)) < temp.objeto.raio:
					damage_ast(temp.objeto)
					bala.lifetime = B_VIDA+1
					break
	_ptemp = Objetos.temp_sprite[0]
	_prect = _ptemp.sprite.get_rect()
	_prect.x = _ptemp.pos[0]
	_prect.y = _ptemp.pos[1]
	for temp in Objetos.temp_sprite:
		if (temp.objeto.name == "asteroide"):
			_rect = temp.sprite.get_rect()
			_rect.x = temp.pos[0]
			_rect.y = temp.pos[1]
			if not pdamaged and (math.dist((_prect.centerx, _prect.centery), (_rect.centerx, _rect.centery))) < (_ptemp.objeto.raio + temp.objeto.raio):
				pdamaged = True


def damage_ast(asteroide):
	#print(asteroide.hp)
	if asteroide.hp <= 0:
		if asteroide.stage > 1:
			asteroide.stage -= 1
			Objetos.Asteroides.append(AsteroidHndlr(asteroide.stage, [asteroide.pos[0]-25, asteroide.pos[1]-25]))
			Objetos.Asteroides.append(AsteroidHndlr(asteroide.stage, [asteroide.pos[0]+25, asteroide.pos[1]+25]))
		Objetos.Asteroides.remove(asteroide)
	else:
		asteroide.hp -= 1
