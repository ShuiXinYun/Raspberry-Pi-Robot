import pygame
pygame.init()
pygame.key.set_repeat(100,100)

while(1):
	
	for event in pygame.event.get():
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_w:
				print "movecmd is W"
