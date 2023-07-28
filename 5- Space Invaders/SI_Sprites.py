import pygame
from pygame.locals import *
from sys import exit
import os

ss=pygame.image.load(os.path.join(os.getcwd(),'SI_SpriteSheet.png'))

class Powercube(pygame.sprite.Sprite):
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        self.at=0
        self.loadimg()
        self.image=self.img[self.at]
        self.rect=self.image.get_rect()
        self.rect.center=x
        self.mask=pygame.mask.from_surface(self.image)

    def update(self):
        if self.at>=4:
            self.at=0
        self.image=self.img[int(self.at)]
        self.at+=0.05

        self.rect.y+=5


    def loadimg(self):
        self.img=[]
        for i in range(16,20):
            self.img.append(ss.subsurface((32*i+5,5),(22,22)))

class Explosion(pygame.sprite.Sprite):
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        self.at=0
        self.loadimg()
        self.image=self.img[self.at]
        self.rect=self.image.get_rect()
        self.rect.center=x

    def update(self):
        if self.at>=3:
            self.kill()
        try:
            self.image=self.img[int(self.at)]
            self.at+=0.5
        except IndexError:
            pass

    def loadimg(self):
        self.img=[]
        for i in range(13,16):
            self.img.append(pygame.transform.scale(ss.subsurface((32*i+8,9),(15,16)),(15*2,16*2)))

class A1(pygame.sprite.Sprite):
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        self.image=ss.subsurface((32*0,0),(32,32))
        self.rect=self.image.get_rect()
        self.rect.center=x
        self.mask=pygame.mask.from_surface(self.image)
        self.loadimg()
        self.life=1

    def update(self):
        if self.life==0:
            for i in self.img:
                self.image=i
            self.kill()

    def loadimg(self):
        self.img=[]
        for i in range(14,17):
            self.img.append(ss.subsurface((32*i,0),(32,32)))




class A2(pygame.sprite.Sprite):
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        self.image=ss.subsurface((32*1,0),(32,32))
        self.rect=self.image.get_rect()
        self.rect.center=x
        self.mask=pygame.mask.from_surface(self.image)

class A3(pygame.sprite.Sprite):
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        self.loadimg()
        self.at=0
        self.image=self.img[self.at]
        self.rect=self.image.get_rect()
        self.rect.center=x
        self.mask=pygame.mask.from_surface(self.image)
    
    def loadimg(self):
        self.img=[]
        for i in range(2,4):
            self.img.append(ss.subsurface((32*i,0),(32,32)))

    def update(self):
        if self.at>=2:
            self.at=0

        self.image=self.img[int(self.at)]
        self.at+=0.05

class A4(pygame.sprite.Sprite):
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        self.image=ss.subsurface((32*4,0),(32,32))
        self.rect=self.image.get_rect()
        self.rect.center=x
        self.mask=pygame.mask.from_surface(self.image)

class T_a(pygame.sprite.Sprite):
    def __init__(self,x=None):
        pygame.sprite.Sprite.__init__(self)
        self.image=ss.subsurface((32*5+14,10),(2,9))
        self.rect=self.image.get_rect()
        self.rect.center=x
        self.mask=pygame.mask.from_surface(self.image)

    def update(self):
        if self.rect.bottom>480:
            self.kill()

        self.rect.y+=10

class T_p(pygame.sprite.Sprite):
    def __init__(self,x=None):
        pygame.sprite.Sprite.__init__(self)
        self.image=ss.subsurface((32*6,0),(32,32))
        self.rect=self.image.get_rect()
        self.rect.center=x
        self.mask=pygame.mask.from_surface(self.image)
        self.pws=False

    def update(self):
        if self.rect.top<0:
            self.kill()

        self.rect.y-=10

class Shield(pygame.sprite.Sprite):
    def __init__(self,x=None):
        pygame.sprite.Sprite.__init__(self)
        self.loadimg()
        self.at=0
        self.image=self.img[self.at]
        self.rect=self.image.get_rect()
        self.rect.center=x
        self.life=500
        self.mask=pygame.mask.from_surface(self.image)

    def loadimg(self):
        self.img=[]
        for i in range(7,11):
            self.img.append(pygame.transform.scale(ss.subsurface((32*i,0),(32,32)),(32+16,32+16)))

    def update(self):
        if self.life>=375:
            self.image=self.img[0]
        elif self.life>=250:
            self.image=self.img[1]
        elif self.life>=125:
            self.image=self.img[2]
        elif self.life>=0:
            self.image=self.img[3]
        else:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loadimg()
        self.image=self.img[0]
        self.rect=self.image.get_rect()
        self.rect.center=320,450
        self.mask=pygame.mask.from_surface(self.image)

    def loadimg(self):
        self.img=[]
        for i in range(11,13):
            self.img.append(ss.subsurface((32*i,0),(32,32)))



if __name__=='__main__':
    tela=pygame.display.set_mode((640,480))
    gp1=pygame.sprite.Group()
    x=[A1((100,100)),A2((200,100)),A3((300,100)),A4((400,100)),T_a((310,240)),T_p((330,240)),Shield((100,400)),Shield((200,400)),Shield((300,400)),Shield((400,400)),Shield((500,400)),Player(),Explosion((300,300)),Powercube((200,300))]

    for i in x:
        gp1.add(x)
    
    while True:
        tela.fill((0,0,0))
        keys=pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                exit()

        gp1.draw(tela)
        d=x[len(x)-1]
        if keys[K_a] and d.rect.bottomleft[0]>0:
            d.rect.x-=1

        if keys[K_d] and d.rect.bottomright[0]<640:
            d.rect.x+=1
            
        gp1.update()

        pygame.display.flip()
    




