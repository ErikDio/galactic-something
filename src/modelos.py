import pygame
from constantes import *

class Modelos:
	@staticmethod
	def nave(target, cor=WHT):
		pygame.draw.polygon(target, cor, [[0, 50], [25, 0], [50, 50], [25, 35]], 2)

	@staticmethod
	def bala(target):
		pygame.draw.circle(target, WHT, (2, 2), 2, 0)

	@staticmethod
	def asteroid1(target):
		pygame.draw.polygon(target, WHT, [[10, 20], [5, 15], [0, 10], [7, 5], [10, 0], [17, 5]], 2)

	@staticmethod
	def asteroid2(target):
		pygame.draw.polygon(target, WHT, [[10, 0], [40, 10], [30, 20], [40, 30], [20, 40], [20, 30], [0, 20]], 2)

	@staticmethod
	def asteroid3(target):
		pygame.draw.polygon(target, WHT, [[0, 10], [40, 0], [70, 10], [50, 30], [60, 50], [20, 70], [0, 50]], 2)
