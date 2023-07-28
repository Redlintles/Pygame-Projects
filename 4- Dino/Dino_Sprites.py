import pygame
from pygame.locals import *
from random import choice as c
from Dino_Functions import *

pygame.init()
try:
    ss=pygame.image.load('./SpriteSheet.png')
except:
    ss=pygame.image.load('./Imagens/SpriteSheet.png')


#Abaixo teremos 2 Superclasses

class Spra(pygame.sprite.Sprite):
    def __init__(self,img,speed,pos=(100,100)):
        pygame.sprite.Sprite.__init__(self)
        self.img=img
        self.image=self.img[0]
        self.rect=self.image.get_rect()
        self.rect.center=pos
        self.at=0
        self.speed=speed

class Spre(pygame.sprite.Sprite):
    def __init__(self,img,speed,pos=(100,100)):
        pygame.sprite.Sprite.__init__(self)
        self.img=img
        self.image=self.img[0]
        self.rect=self.image.get_rect()
        self.rect.center=pos
        self.speed=20
    
    def ch_spr(self):
        if self.image==self.img[0] and not(isinstance(self,Moon())): 
            self.image=self.img[1]

        else:
            self.image=self.img[0]

    def update(self):
        if self.rect.topright[0]<0:
            self.rect.x+=1000
        
        self.rect.x-=self.speed

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,img,noite,speed=20,pos=(100,100)):
        pygame.sprite.Sprite.__init__(self)  
        self.img=img
        self.noite=noite
        self.image=self.img[1] if self.noite else self.img[0]
        self.rect=self.image.get_rect()
        self.rect.center=pos
        self.mask=pygame.mask.from_surface(self.image)
        self.at=0
        self.speed=speed
    
    def ch_spr(self):
        if self.image==self.img[0]:
            self.image=self.img[1]
        else:
            self.image=self.img[0]

    def update(self):
        if self.rect.topright[0]<0:
            self.kill()

        self.rect.x-=self.speed
        



#Classes que herdam de Spra (Sprite Animado)

class Dino(Spra):
    def __init__(self,pos=(100,100)):
        super().__init__(self.loadimg(),0,pos)
        self.iml=self.img[:3]
        self.jump=False
        self.mask=pygame.mask.from_surface(self.image)
        self.speed=0

    def loadimg(self,n=0):
        img=[]
        for i in range(6):
            img.append(pygame.transform.scale(ss.subsurface((36*i+8,6),(20,20)),(20*3,20*3)))

        for i in range(25,27):
            img.append(pygame.transform.scale(ss.subsurface((36*i+8,6),(20,20)),(20*3,20*3)))

        return img
    
    def ch_spr(self):
        if self.iml==self.img[:3]:
            self.iml=self.img[3:6]
    
        else:
            self.iml=self.img[:3]

    def update(self):

        if self.jump:
            self.rect.y-=30
        
        if self.rect.y<200:
            self.jump=False

        if not(self.jump) and self.rect.y!=350:
            self.rect.y+=15

        if self.at>2:
            self.at=0

        self.image=self.iml[int(self.at)]
        self.at+=0.2

class Star(Spra):
    def __init__(self,speed,pos=(300,200)):
        super().__init__(self.loadimg(),speed,pos)
        self._layer=5
        
    def loadimg(self):
        img=[]
        for i in range(20,24):
            img.append(pygame.transform.scale(ss.subsurface((36*i+14,10),(8,10)),(8*3,10*3)))
        
        return img
    
    def update(self):
        if self.at > 4:
            self.at=0
        
        self.image=self.img[int(self.at)]
        self.at+=0.2

        if self.rect.topright[0]<0:
            self.rect.x+=664
            self.rect.y=c([20,50,100,150,200])
        
        self.rect.x-=self.speed



#Classes que Herdam de Spre(Sprite Estático)

class Floor(Spre):
    def __init__(self,speed,pos=(100,416)):
        super().__init__(self.loadimg(),speed,pos)

    def loadimg(self):
        img=[]
        for i in range(16,18):
            img.append(pygame.transform.scale(ss.subsurface((36*i,14),(36,4)),(36*3,4*3)))
        
        return img

    def update(self):
        if self.rect.topright[0]<0:
            self.rect.x+=748

        self.rect.x-=20
    
    def ch_spr(self):
        if self.image==self.img[0]:
            self.image=self.img[1]
        else:
            self.image=self.img[0]
        
class Cloud(Spre):
    def __init__(self,speed,pos=(200,200)):
        super().__init__(self.loadimg(),speed,pos)
        self._layer=10
        self.speed=10

    def loadimg(self):
        img=[]

        for i in range(18,20):
            img.append(pygame.transform.scale(ss.subsurface((36*i+5,11),(25,10)),(25*3,10*3)))
        
        return img
    
    def update(self):
        if self.rect.topright[0]<0:
            self.rect.x+=715+80*c([1,2,3,4,5])
            self.rect.y=50+40*c([1,2,3])

        self.rect.x-=self.speed

    def ch_spr(self):
        if self.image==self.img[0]:
            self.image=self.img[1]
        else:
            self.image=self.img[0]

class Moon(Spre):
    def __init__(self,speed,pos=(400,200)):
        super().__init__(self.loadimg(),speed,pos)
        self._layer=4
        self.speed=4

    def loadimg(self):
        return [pygame.transform.scale(ss.subsurface((36*24+11,3),(13,25)),(13*3,25*3))]
    
    def update(self):
        if self.rect.topright[0]<0:
            self.rect.x+=679
        
        self.rect.x-=self.speed

#Classes que herdam de Obstacle

class Cacto1(Obstacle):
    def __init__(self,noite,speed,pos):
        super().__init__(self.loadimg(),noite,speed,pos)

    def loadimg(self):
        img=[]
        for i in range(10,12):
            img.append(pygame.transform.scale(ss.subsurface((36*i+9,2),(18,28)),(18*3,28*3)))

        return img

class Cacto2(Obstacle):
    def __init__(self,noite,speed,pos):
        super().__init__(self.loadimg(),noite,speed,pos)
    
    def loadimg(self):
        img=[]
        for i in range(12,14):
            img.append(pygame.transform.scale(ss.subsurface((36*i+3,1),(29,29)),(29*3,29*3)))

        return img

class Cacto3(Obstacle):
    def __init__(self,noite,speed,pos):
        super().__init__(self.loadimg(),noite,speed,pos)
   
    def loadimg(self):
        img=[]
        for i in range(14,16):
            img.append(pygame.transform.scale(ss.subsurface((36*i,3),(35,25)),(35*3,25*3)))

        return img

class Ptero(Obstacle):
    def __init__(self,noite,speed,pos):
        super().__init__(self.loadimg(),noite,speed,pos)
        if self.noite:
            self.iml=self.img[2:5]
        else:
            self.iml=self.img[:2]
    
    def loadimg(self):
        img=[]
        for i in range(6,10):
            img.append(pygame.transform.scale(ss.subsurface((36*i+5,7),(24,18)),(24*3,18*3)))

        return img
    
    def ch_spr(self):
        if self.iml==self.img[:2]:
            self.iml=self.img[2:5]

        else:
            self.iml=self.img[:2]
    
    def update(self):
        if self.at>2:
            self.at=0
        
        self.image=self.iml[int(self.at)]
        self.at+=0.1

        if self.rect.topright[0]<0:
            self.kill()
        
        self.rect.x-=self.speed


#Exibe uma preview das sprites caso o arquivo seja executado como principal

if __name__=='__main__':
    from sys import exit

    n=False
    tela=pygame.display.set_mode((640,480))
    gp=pygame.sprite.Group(Dino(n),Ptero(n),Cacto1(n),Cacto2(n),Cacto3(n),Floor(n),Cloud(n),Star(),Moon())
    relogio=pygame.time.Clock()

    while True:
        tela.fill((0,0,0))
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                exit()

        gp.draw(tela) ; gp.update()
        relogio.tick(30)
        pygame.display.flip()

