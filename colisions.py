import math
from objetos import *
from constantes import *
from modelos import *

def colision_chk(target):
	global pdamaged
	global dmg_cont
	if pdamaged == True:
		if dmg_cont < inv_frames:
			print(dmg_cont)
			dmg_cont += 1
			if dmg_cont%20 == 0:
				Objetos.Player.sprite.fill(blk)
				Modelos.nave(Objetos.Player.sprite, gre)
			elif dmg_cont%20 == 10:
				Objetos.Player.sprite.fill(blk)
				Modelos.nave(Objetos.Player.sprite, wht)
		else:
			dmg_cont = 0
			Objetos.Player.sprite.fill(blk)
			Modelos.nave(Objetos.Player.sprite, wht)
			pdamaged = False
	for contador, bala in enumerate(Objetos.Bala):
		for temp in Objetos.temp_sprite:
			if (temp.objeto.name == "asteroide"):
				_rect = temp.sprite.get_rect()
				_rect.x = temp.pos[0]
				_rect.y = temp.pos[1]
				if math.dist(bala.pos, (_rect.centerx, _rect.centery)) < temp.objeto.raio:
					damage_ast(temp.objeto)
					bala.lifetime = bala_vida+1
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
	print(asteroide.hp)
	if asteroide.hp <= 0:
		Objetos.Asteroides.remove(asteroide)
	else:
		asteroide.hp -= 1