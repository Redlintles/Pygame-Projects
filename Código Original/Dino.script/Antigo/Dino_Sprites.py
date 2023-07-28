import pygame
from pygame.locals import *



class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loadimg()
        self.at=0
        self.image=self.img[self.at]
        self.rect=self.image.get_rect()
        self.rect.center=100,416
        self.jump=False
        self.J=pygame.mixer.Sound(os.path.join(dir_som,'Jump.wav')) ; self.J.set_volume(0.5)
        self.mask=pygame.mask.from_surface(self.image)
      
    def loadimg(self):
        self.img=[]
        for i in range(3):
            self.img.append(pygame.transform.scale(ss.subsurface((i*32,0),(32,32)),(32*3,32*3)))

    def update(self):
        if self.jump:
            self.rect.y-=3

            if self.rect.y<200:
                self.jump=False
                       
        elif not(self.jump) and self.rect.y<366:
            self.rect.y+=3

        if self.at>=2:
            self.at=0

        self.at+=0.05
        self.image=self.img[int(self.at)]

    def pular(self):
        self.jump=True
        self.J.play()

class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(ss.subsurface((224,0),(32,32)),(32*3,32*3))
        self.rect=self.image.get_rect()
        self.rect.y=randrange(50,200,50)
        self.rect.x=640-randrange(30,300,90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x=640
            self.rect.y=randrange(0,110,10)
            
        self.rect.x-=2
    def reset(self):
        self.rect.x=640
        self.rect.y=randrange(50,200,50)
    
class Chão(pygame.sprite.Sprite):
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(ss.subsurface((32*6,0),(32,32)),(32*2,32*2))
        self.rect=self.image.get_rect()
        self.rect.y=416
        self.x=x
        self.rect.x=self.x*64

    def update(self):
        if self.rect.topright[0]<0:
            self.rect.x=640
        self.rect.x-=2
            
class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(ss.subsurface((32*5,0),(32,32)),(32*2,32*2))
        self.rect=self.image.get_rect()
        self.rect.center=(640,416)
        self.mask=pygame.mask.from_surface(self.image)

    def update(self):
        if self.rect.topright[0]<0:
            self.rect.center=(randrange(640,640*3,320),416)
        self.rect.x-=2

    def reset(self):
        self.rect.center=(640,416)

class Ptero(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loadimg()
        self.at=0
        self.image=self.img[self.at]
        self.rect=self.image.get_rect()
        self.rect.center=(randrange(640,640*5,320),416-32)
        self.mask=pygame.mask.from_surface(self.image)
  
    def loadimg(self):
        self.img=[]
        for i in range(3,5):
            self.img.append(pygame.transform.scale(ss.subsurface((32*i,0),(32,32)),(32*2,32*2)))
    
    def update(self):
        if self.at>=2:
            self.at=0

        self.image=self.img[int(self.at)]
        self.at+=0.02
     
        if self.rect.topright[0]<0:
            self.rect.center=640,416-32

        self.rect.x-=2
    
    def reset(self):
        self.rect.center=1040,416-32