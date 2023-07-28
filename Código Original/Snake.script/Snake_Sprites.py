import pygame
from pygame.locals import *
import os

if '.script' not in os.getcwd():
    os.chdir('Snake.script')

ss=pygame.image.load('./Imagens/Snake_SpriteSheet.png')

class Apple(pygame.sprite.Sprite):
    def __init__(self,pos=(100,100)):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(ss.subsurface((9,8),(12,16)),(12*3,16*3))
        self.rect=self.image.get_rect()
        self.rect.center=pos

class Wall(pygame.sprite.Sprite):
    def __init__(self,pos=(200,100)):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(ss.subsurface((32+9,11),(14,14)),(14*3,14*3))
        self.rect=self.image.get_rect()
        self.rect.center=pos



if __name__=='__main__':
    tela=pygame.display.set_mode((640,480))
    gp=pygame.sprite.Group()
    gp.add(Apple(),Wall())

    while True:
        tela.fill((255,255,255))

        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                exit()
        
        gp.draw(tela)

        pygame.display.flip()