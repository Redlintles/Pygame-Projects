import pygame
from pygame.locals import *
from sys import exit
from random import choice as c
from Snake_Functions import *
from Gamelib import *
from functools import partial

pygame.init()
#Configurações da Tela
tela=pygame.display.set_mode((640,480))
pygame.display.set_caption('Snake Game')
relogio=pygame.time.Clock()



fonte=pygame.font.SysFont('arial',25,True,True)#Fonte

pcobra,pcomida,lencobra,morte,pc,corpo,pontos,gpc,gpw=define()

maxpt=checkMax()

while True:
    tela.fill((255,255,255))
    keys=pygame.key.get_pressed()

    tela.blit(fonte.render('Pontos:%i'%pontos,False,(0,0,0)),(0,0))
    tela.blit(fonte.render('Maxpt:%i'%maxpt,False,(0,0,0)),(520,0))

    if mute:
        tela.blit(fonte.render('Mutado!',False,(0,0,0)),(0,450))

    #Verificação de Eventos
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            exit()

        if event.type==KEYDOWN:
            if event.key == K_a or event.key == K_LEFT and pc[0]!=10:
                pc[0]=-10
                pc[1]=0

            elif event.key == K_d or event.key == K_RIGHT and pc[0]!=-10:
                pc[0]=10
                pc[1]=0

            elif event.key == K_w or event.key == K_UP and pc[1]!=10:
                pc[0]=0
                pc[1]=-10

            elif event.key == K_s or event.key == K_DOWN and pc[1]!=-10:
                pc[0]=0
                pc[1]=10
            
            if event.key==K_p:
                pause(tela,fonte,{'Pontos:%i'%pontos:(0,0),'Maxpt:%i'%maxpt:(520,0)},mute,[(0,450),(520,450),(255,255,255),None,False,[partial(newseg,corpo,tela),None]],gpw,gpc)
            
            if event.key==K_m:
                mute=ch_mute()
                Sons.set_volume(0.1) if not mute else None

    #Movimentação do Jogador

    pcobra[0]+=pc[0]
    pcobra[1]+=pc[1]

    cabeça=pygame.draw.rect(tela,(0,255,0),(pcobra[0],pcobra[1],20,20))

    #Geração da comida

    comida=Apple((pcomida[0],pcomida[1]))
    gpc.add(comida)

    rects=newseg(corpo,tela)

    while pygame.sprite.spritecollide(comida,gpw,False) or any((x.colliderect(comida.rect) for x in rects)):
        pcomida=[c([x for x in range(40,600,10)]),c([x for x in range(40,440,10)])]
        comida=Apple((pcomida[0],pcomida[1]))
        gpc=pygame.sprite.Group(comida)

    #Sistema de Colisão

    if cabeça.colliderect(comida.rect):
        pcomida=[c([x for x in range(40,600,10)]),c([x for x in range(40,440,10)])]
        lencobra+=1;pontos+=1
        Sons.sounds['Eat'].play() if not(mute) else None
        gpc=pygame.sprite.Group()

    if WallCollide(cabeça,gpw):
        pcobra,pcomida,lencobra,morte,pc,corpo,pontos,gpc,gpw=youredead(morte,pcobra,pcomida,lencobra,pc,corpo,pontos,tela,fonte)
    
    head=[]
    head+=list((pcobra[0],pcobra[1]))

    if head not in corpo:
        corpo.append(head)

    else:
        pcobra,pcomida,lencobra,morte,pc,corpo,pontos,gpc,gpw=youredead(morte,pcobra,pcomida,lencobra,pc,corpo,pontos,tela,fonte)
    
    if any((pcobra[0]>620,pcobra[0]<0,pcobra[1]>460,pcobra[1]<0)):
        pcobra,pcomida,lencobra,morte,pc,corpo,pontos,gpc,gpw=youredead(morte,pcobra,pcomida,lencobra,pc,corpo,pontos,tela,fonte)
        
    if len(corpo)>lencobra: 
        del corpo[0]

    groupCall(('draw',tela),gpw,gpc)

    maxpt=updateMax(maxpt,pontos)

    relogio.tick(30)
    pygame.display.update()