import pygame
from pygame.locals import *
from sys import exit
from Breakout_Sprites import *
from random import choice as c
import os
from Gamelib import Sound_group
import pickle
from itertools import repeat as r

pygame.init()
pygame.mixer.init()

if '.script' not in os.getcwd():
    os.chdir('Breakout.script')

fonte=pygame.font.SysFont('arial',27,True,True)

dirp=os.getcwd()

Som=pygame.mixer.Sound

with open('./Config.pck','rb') as arq:
    vol=pickle.load(arq)
    if vol<0.1:
        mute=True
    else:
        mute=False
    try:
        dif=pickle.load(arq)

        if dif==1:
            difficult={'va':list(r(c([2,-2]),2)),'aumento':1}
        
        elif dif==2:
            difficult={'va':list(r(c([2,-2]),2)),'aumento':2}

        elif dif==3:
            difficult={'va':list(r(c([2,-2]),2)),'aumento':3}

        del dif

    except EOFError:
        print('a')

Sons=Sound_group(vol,
    Colpar=Som('./Sons/ColPar.wav'),
    Colplayer=Som('./Sons/ColPlayer.wav'),
    Colrect=Som('./Sons/ColRect.wav'),
)

def ch_mute():
    global mute
    mute=not(mute)
    return mute

def colisão(nexty,pontos,va,ball,*gps):

    global Sons,mute,difficult

    col_br=pygame.sprite.spritecollide(ball,gps[0],False,pygame.sprite.collide_circle)
    col_bp=pygame.sprite.spritecollide(ball,gps[1],False,pygame.sprite.collide_rect)

    if col_br:
        pontos+=len(col_br)
        Sons.sounds['Colrect'].play() if not(mute) else None
        col_br[0].kill()
        va[1]*=-1
        if len(gps[0])==nexty:
            for i in va:
                if i<0:
                    i-=difficult['aumento']
                    nexty-=9

                elif i>0:
                    i+=difficult['aumento']
                    nexty-=9

    elif col_bp and ball.rect.bottom<480:

        va[1]*=-1
        Sons.sounds['Colplayer'].play() if not(mute) else None

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

    global difficult

    gp_rect=pygame.sprite.Group()
    criarect(gp_rect)
    ball=Ball((320,300))
    player=Player((320,450))
    gp_ball=pygame.sprite.Group() ; gp_ball.add(ball)
    gp_player=pygame.sprite.Group() ; gp_player.add(player)
    va=difficult['va']
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

def move_ball(ball,va):

    global Sons,mute

    if ball.rect.left<=0 or ball.rect.right>=640:
        va[0]*=-1
        Sons.sounds['Colpar'].play() if not(mute) else None
        for i in range(3):        
            ball.rect.center=(ball.rect.center[0]+va[0],ball.rect.center[1]+va[1])
        
    if ball.rect.top<=0:
        va[1]*=-1
        Sons.sounds['Colpar'].play() if not(mute) else None
        for i in range(3):        
            ball.rect.center=(ball.rect.center[0]+va[0],ball.rect.center[1]+va[1])
    
    
    ball.rect.center=(ball.rect.center[0]+va[0],ball.rect.center[1]+va[1])

def delete(*gps):
    for gp in gps:
        for sprite in gp:
            sprite.kill()