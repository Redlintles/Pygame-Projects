import pygame
from pygame.locals import *
from sys import exit
from random import choice as c,shuffle as s

import os

pygame.init()

try:
    ss=pygame.image.load(os.getcwd()+'\Imagens\Breakout.png')

except:
    ss=pygame.image.load(os.getcwd()+'\Breakout.script\Imagens\Breakout.png')




class Rectangle(pygame.sprite.Sprite):
    def __init__(self,pos : tuple ,cor : int):
        pygame.sprite.Sprite.__init__(self)
        self.cor=cor
        self.loadimg()
        self.rect=self.image.get_rect()
        self.rect.topleft=pos

    def loadimg(self):
        self.img=[]
        for i in range(8):
            self.img.append(pygame.transform.scale(ss.subsurface((32*i,7),(32,11)),(68,25)))
    
        self.image=self.img[self.cor]

class Player(pygame.sprite.Sprite):
    def __init__(self,pos : tuple):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(ss.subsurface((32*8,21),(32,11)),(32*3,11*3))
        self.rect=self.image.get_rect()
        self.rect.center=pos

class Ball(pygame.sprite.Sprite):
    def __init__(self,pos : tuple):
        pygame.sprite.Sprite.__init__(self)
        self.image=ss.subsurface((32*9,0),(32,32))
        self.radius=17
        self.rect=self.image.get_rect()
        self.rect.center=pos

if __name__=='__main__':
    tela=pygame.display.set_mode((640,480))
    gp1=pygame.sprite.Group()
    x=[Rectangle((70*i,30*j),-1+j) for i in range(1,9) for j in range(1,8)]+[Player((320,450)),Ball((320,300))]

    for i in x:
        gp1.add(x)
    
    while True:
        tela.fill((0,0,0))
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                exit()
        
        gp1.draw(tela)
        gp1.update()
        pygame.display.flip()
