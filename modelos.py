import pygame
from constantes import *
blk = (0, 0, 0)
wht = (255, 255, 255)

class Modelos:
	@staticmethod
	def nave(target, cor=wht):
		pygame.draw.polygon(target, cor, [[0, 50], [25, 0], [50, 50], [25, 35]], 2)

	@staticmethod
	def bala(target):
		pygame.draw.circle(target, wht, (2, 2), 2, 0)

	@staticmethod
	def asteroid1(target):
		pygame.draw.polygon(target, wht, [[10, 10], [10, 0]], 2)

	@staticmethod
	def asteroid2(target):
		pygame.draw.polygon(target, wht, [[0, 10], [40, 0], [70, 10], [50, 30], [60, 50], [20, 70], [0, 50]], 2)

	@staticmethod
	def asteroid3(target):
		pygame.draw.polygon(target, wht, [[10, 0], [40, 10], [30, 20], [40, 30], [30, 40], [20, 30], [0, 20]], 2)