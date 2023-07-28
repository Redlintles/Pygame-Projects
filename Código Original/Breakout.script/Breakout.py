import pygame,os,pickle
from pygame.locals import *
from sys import exit,path
from Breakout_Sprites import *
from Breakout_Functions import *
from random import choice as c
from Gamelib import *

pygame.init()

tela=pygame.display.set_mode((640,480))
pygame.display.set_caption('Breakout')

fonte=pygame.font.SysFont('arial',27,True,True)

maxpt=checkMax()
  
gp_rect,ball,player,gp_ball,gp_player,va,nexty,pontos=define(0)

while True:
    tela.fill((0,0,0))

    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            exit()

        if event.type==KEYDOWN:
            if event.key==K_m:
                mute=ch_mute()
                Sons.set_volume(0.1) if not mute else None

            if event.key==K_p:
                pause(tela,fonte,{'Pontos:%i'%pontos:(0,450),'Maxpt:%i'%maxpt:(520,450)},mute,[(260,450),(250,260),(0,0,0)],gp_rect,gp_ball,gp_player)

    maxpt=updateMax(pontos,maxpt)
    
    if ball.rect.bottom>player.rect.top+10:
        print(va)
        delete(gp_rect,gp_ball,gp_player)

        while True:
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    exit()
            tela.blit(fonte.render('Você Perdeu!,Aperte Espaço para jogar de novo',False,(255,255,255)),(4,240)) 
            pygame.display.flip() 

            if pygame.key.get_pressed()[K_SPACE]:
                gp_rect,ball,player,gp_ball,gp_player,va,nexty,pontos=define(0)
                break
    
    elif len(gp_rect)==0:
        delete(gp_rect,gp_ball,gp_player)

        updateMax(pontos,maxpt)

        while True:
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    exit()
        
            tela.blit(fonte.render('Você Ganhou!,Aperte Espaço para jogar de novo',False,(255,255,255)),(4,240)) 
            pygame.display.flip() 
            if pygame.key.get_pressed()[K_SPACE]:
                gp_rect,ball,player,gp_ball,gp_player,va,nexty=define(1)
                break
        
    move_player(player)
    move_ball(ball,va)
    nexty,pontos,va=colisão(nexty,pontos,va,ball,gp_rect,gp_player)

    groupCall(('draw',tela),gp_rect,gp_player,gp_ball)
    groupCall('update',gp_rect,gp_player,gp_ball)

    tela.blit(fonte.render('Pontos:%i'%pontos,False,(255,255,255)),(0,450))
    tela.blit(fonte.render('Maxpt:%i'%maxpt,False,(255,255,255)),(520,450))

    if mute: tela.blit(fonte.render('Mutado!',False,(255,255,255)),(260,450))

    pygame.display.flip()
    
    

