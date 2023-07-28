import pygame
from pygame.locals import *
from sys import exit
from Breakout_Sprites import *
from random import choice as c
import os

pygame.init()
pygame.mixer.init()

fonte=pygame.font.SysFont('arial',27,True,True)

dirp=os.getcwd()

Sons=dict(

    ColPar=pygame.mixer.Sound(os.path.join(dirp,'ColPar.wav')),
    ColPlayer=pygame.mixer.Sound(os.path.join(dirp,'ColPlayer.wav')),
    ColRect=pygame.mixer.Sound(os.path.join(dirp,'ColRect.wav'))

)

for i in Sons:
    Sons[i].set_volume(0.5)

def pausar(pause,tela,pontos,maxpt,mute,*gps):

    global fonte

    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                exit()
            if event.type==KEYDOWN:
                if event.key==K_p:
                    pause=not(pause)
                    return pause
        
        for i in gps: i.draw(tela)

        tela.blit(fonte.render('Pausado!',False,(255,255,255)),(260,240))
        tela.blit(fonte.render('Pontos:%i'%pontos,False,(255,255,255)),(0,450))
        tela.blit(fonte.render('Maxpt:%i'%maxpt,False,(255,255,255)),(520,450))

        if mute:
            tela.blit(fonte.render('Mutado!',False,(255,255,255)),(260,450))

        pygame.display.flip()

def colisão(nexty,pontos,va,mute,ball,*gps):

    global Sons

    col_br=pygame.sprite.spritecollide(ball,gps[0],False,pygame.sprite.collide_circle)
    col_bp=pygame.sprite.spritecollide(ball,gps[1],False,pygame.sprite.collide_rect)

    if col_br:
        pontos+=len(col_br)
        Sons['ColRect'].play() if not(mute) else None
        col_br[0].kill()
        va[1]*=-1

        for i in va:
            if i<0 and len(gps[0])==nexty:
                i-=1
                nexty-=9
            elif i>0 and len(gps[1])==nexty:
                i+=1
                nexty-=9



    elif col_bp and ball.rect.bottom<480:

        va[1]*=-1
        Sons['ColPlayer'].play() if not(mute) else None

        for i in range(3):        
            ball.rect.center=(ball.rect.center[0]+va[0],ball.rect.center[1]+va[1])

    return nexty,pontos,va

def criarect(gp_rect):
    lcores=[x for x in range(8)]
    for i in range(7):
        cor=c(lcores)
        lcores.remove(cor)

        for j in range(9):
            gp_rect.add(Rectangle((71*j,30*i),cor))

def define(x):
    gp_rect=pygame.sprite.Group()
    criarect(gp_rect)
    ball=Ball((320,300))
    player=Player((320,450))
    gp_ball=pygame.sprite.Group() ; gp_ball.add(ball)
    gp_player=pygame.sprite.Group() ; gp_player.add(player)
    va=[c([2,-2]),c([2,-2])]
    nexty=54
    if x:        
        return gp_rect,ball,player,gp_ball,gp_player,va,nexty
    
    pontos=0   
    return gp_rect,ball,player,gp_ball,gp_player,va,nexty,pontos


def move_player(player):
    #49,592
    pm=pygame.mouse.get_pos()[0]
    if pm>=48 and pm <=592:
        player.rect.center=(pm,450)

def move_ball(ball,va,mute):

    global Sons

    if ball.rect.left<=0 or ball.rect.right>=640:
        va[0]*=-1
        Sons['ColPar'].play() if not(mute) else None
        for i in range(3):        
            ball.rect.center=(ball.rect.center[0]+va[0],ball.rect.center[1]+va[1])
        
    if ball.rect.top<=0:
        va[1]*=-1
        Sons['ColPar'].play() if not(mute) else None
        for i in range(3):        
            ball.rect.center=(ball.rect.center[0]+va[0],ball.rect.center[1]+va[1])
    

    ball.rect.center=(ball.rect.center[0]+va[0],ball.rect.center[1]+va[1])