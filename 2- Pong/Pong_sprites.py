import pygame
from pygame.locals import *
from sys import exit
import os
from random import choice

dir_img=os.path.join(os.getcwd(),'Sprites_Pong.png')

ss=pygame.image.load(dir_img)

class Ball(pygame.sprite.Sprite):
    def __init__(self,pos):
        '''
        Inicializa a Classe Ball,responsável pela sprite da bola azul
        '''

        pygame.sprite.Sprite.__init__(self)
        self.image=ss.subsurface((0,0),(32,32))
        self.rect=self.image.get_rect()
        self.rect.center=pos
        self.mask=pygame.mask.from_surface(self.image)

class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        '''
        Inicializa a Classe Player,responsável pelas sprites dos jogadores na esquerda e direita da tela
        '''

        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(ss.subsurface((32+14,4),(4,24)),(16,32*3))
        self.rect=self.image.get_rect()
        self.rect.center=pos
        self.mask=pygame.mask.from_surface(self.image)

class Wall(pygame.sprite.Sprite):
    def __init__(self,pos):
        '''
        Inicializa a Classe Wall,responsável pelas sprites das paredes do topo e do fundo da tela
        '''

        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(ss.subsurface((32*2,14),(32,4)),(32*20,16))
        self.rect=self.image.get_rect()
        self.rect.topleft=pos
        self.mask=pygame.mask.from_surface(self.image)
        
class Center(pygame.sprite.Sprite):
    def __init__(self,pos):
        '''
        Inicializa a classe Center,responsável pela sprite da linha de centro do jogo
        '''

        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(ss.subsurface((32*3+11,0),(9,32)),(32*2+16,32*13+25))
        self.rect=self.image.get_rect()
        self.rect.center=pos

if __name__=='__main__':#Executa uma preview caso o módulo seja executado diretamente
    tela=pygame.display.set_mode((640,480))

    tela.fill((0,0,0))
    bola=Ball((320,240))
    
    l1=[bola,Player((10,240)),Player((630,240)),Wall((0,0)),Wall((0,460)),Center((320,238))]
    gp1=pygame.sprite.LayeredUpdates()
    for i in l1:
        gp1.add(i)

    gp1.change_layer(bola,1)

    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                exit()

        gp1.draw(tela)
        gp1.update()

        pygame.display.flip()

    
