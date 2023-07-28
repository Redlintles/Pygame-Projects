import pygame
from pygame.locals import *
from sys import exit
from Pong_sprites import *
from Pong_functions import *
from Gamelib import pause
from collections import OrderedDict

pygame.init()

tela=pygame.display.set_mode((640,480))
pygame.display.set_caption("Pong")

b,gp1,p1,p2,va,pontos=desenhar()

while True:
    tela.fill((0,0,0))
    keys=pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            exit()

        if event.type==KEYDOWN:
            if event.key==K_m:
                mute=ch_mute()
                Sons.set_volume(0.1) if not mute else None

            if event.key==K_p:
                pause(tela,fonte,{'%i'%pontos[0]:(200,240),'%i'%pontos[1]:(400,240)},mute,[(200,430),(360,430),(0,0,0),fonte1,True],gp1)
                

    if keys[K_w] and p1.rect.top>15:
        p1.rect.y-=5

    elif keys[K_s] and p1.rect.bottom<460:
        p1.rect.y+=5

    if keys[K_UP] and p2.rect.top>15:
        p2.rect.y-=5
        
    elif keys[K_DOWN] and p2.rect.bottom<460:
        p2.rect.y+=5

    if any((x==10 for x in pontos)):
        for i in gp1:
            i.kill()

        while True:
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    exit()

            if pygame.key.get_pressed()[K_SPACE]:
                b,gp1,p1,p2,va,pontos=desenhar()
                break
            
            if pontos[0]==10:
                tela.blit(fonte1.render('Player 1 Ganhou!,Aperte Espaço Para Um Novo Jogo!',True,(255,255,255)),(60,240))

            elif pontos[1]==10:
                tela.blit(fonte1.render('Player 2 Ganhou!,Aperte Espaço Para Um Novo Jogo!',True,(255,255,255)),(60,240))

            pygame.display.flip()
            
    gp1.draw(tela)
    gp1.update()

    va=colisão(b,gp1,va)

    pontos,va=move_ball(b,pontos,va)

    if mute:
        tela.blit(fonte1.render('Mutado!',True,(255,255,255)),(200,430))

    tela.blit(fonte.render('%i'%pontos[0],True,(255,255,255)),(200,240))
    tela.blit(fonte.render('%i'%pontos[1],True,(255,255,255)),(400,240))

    pygame.display.flip()
    
