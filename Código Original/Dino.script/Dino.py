import pygame
from pygame.locals import *
from sys import exit
from Dino_Functions import *
from Dino_Sprites import *
from random import choice as c
from Gamelib import *

pygame.init()
pygame.mixer.init()

tela=pygame.display.set_mode((640,480))
pygame.display.set_caption('Dino Game')
relogio=pygame.time.Clock()

maxpt=checkMax()  

fonte=pygame.font.SysFont('Arial',20,True,True)
mute=False

pontos,noite,chcor,cor,gpc,gpn,ob,gpobs,gps,gpd,ctexto,nexty,d,speed=define()

while True:
    tela.fill(tuple(cor))

    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            exit()
        
        if event.type==KEYDOWN:
            if any((event.key==K_UP,event.key==K_w)) and d.rect.y==350:
                d.jump=True
                d.image=d.img[5] if noite else d.img[2]
                Sons.sounds['Jump'].play()
            
            if event.key==K_m:
                mute=ch_mute()
                Sons.set_volume(0.1) if not mute else None

    relogio.tick(30)

    chcor,noite,nexty,speed=mudafundo(speed,d,pontos,chcor,noite,nexty,gpn,gpd,gpobs,gpc)
    cor,ctexto=color_controller(chcor,ctexto,cor)
    gpobs,ob=choose(gpobs,ob,noite,speed)
    maxpt=updateMax(pontos,maxpt)

    if col(maxpt,pontos,d,noite,gpobs,tela,fonte,ctexto,gpc,gpn,gpd):
        pontos,noite,chcor,cor,gpc,gpn,ob,gpobs,gps,gpd,ctexto,nexty,d,speed=define()

    pontos+=0.2

    tela.blit(fonte.render('Pontos:%i'%int(pontos),False,ctexto),(0,460))
    tela.blit(fonte.render('Maxpt:%i'%maxpt,False,ctexto),(500,460))
    tela.blit(fonte.render('Mutado!',False,ctexto),(280,460)) if mute else None

    groupCall(('draw',tela),gpc,gpd,gpn,gpobs)
    groupCall('update',gpc,gpd,gpn,gpobs)

    pygame.display.flip()
    