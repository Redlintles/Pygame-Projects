import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange,randint as r
from Dino_Sprites import *

pygame.init()
pygame.mixer.init()

dir=os.path.dirname(__file__)
dir_img=os.path.join(dir,'Imagens')
dir_som=os.path.join(dir,'Sons')

fonte=pygame.font.SysFont('arial',30,True,True)

tela=pygame.display.set_mode((640,480))
pygame.display.set_caption('Dino')
ss=pygame.image.load(os.path.join(dir_img,'SpriteSheet.png'))

Death=pygame.mixer.Sound(os.path.join(dir_som,'Death.wav')) ; Death.set_volume(1)
Score=pygame.mixer.Sound(os.path.join(dir_som,'Score.wav')) ; Score.set_volume(1)
Reset=False

Pontos=0


        
dino=Dino()

gp=pygame.sprite.Group()
gp.add(dino)

c=Cacto() ; p=Ptero()
gp2=pygame.sprite.Group()
gp2.add(c,p)
lnuvem=[]
for i in range(1,4):
    n=Nuvens()   
    lnuvem.append(n)
    gp.add(n)

for i in range(20):
    gp.add(Chão(i))

while True:
    tela.fill((255,255,255))
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            exit()
        
        if event.type==KEYDOWN:
            if any((event.key==K_SPACE,event.key==K_w,event.key==K_UP)) and dino.rect.center[1]==380:
                dino.pular()

    gp.draw(tela) ; gp2.draw(tela)
    gp.update() ; gp2.update()

    tela.blit(fonte.render('Pontos:%i'%int(Pontos),True,(0,0,0)),(480,20))
    Pontos+=0.02

    if int(Pontos)%100==0 and Pontos>=100:
        Score.play()
        Pontos+=1

    col=pygame.sprite.spritecollide(dino,gp2,False,pygame.sprite.collide_mask)

    if col:
        Pontos=0
        Death.play()
        while True:
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    exit()

                if event.type==KEYDOWN:
                    if any((event.key==K_SPACE,event.key==K_UP,event.key==K_w)):
                        Reset=True
            if Reset:
                c.reset()
                for i in lnuvem:
                    i.reset()

                Reset=False
                p.reset()
                break

    pygame.display.flip()


    




        





