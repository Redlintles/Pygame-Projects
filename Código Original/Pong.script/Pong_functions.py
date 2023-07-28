import pygame
from pygame.locals import *
from Pong_sprites import *
import os
from random import choice as c
from Gamelib import *
from time import sleep

pygame.init()
pygame.mixer.init()

fonte=pygame.font.SysFont('arial',50,True,True)
fonte1=pygame.font.SysFont('arial',20,True,True)

som=pygame.mixer.Sound

with open('./Config.pck','rb') as arq:
    vol=pickle.load(arq)
    if vol<0.1:
        mute=True
    else:
        mute=False

Sons=Sound_group(vol,
    CJ=som('./Sons/CJ.wav'),
    CP=som('./Sons/CP.wav'),
    MP=som('./Sons/MP.wav')
)

def ch_mute():
    global mute
    mute=not(mute)
    return mute

def colisão(b,gp1,va):
    '''
    Responsável pela detecção de colisão do jogo
    '''

    global Sons,mute

    col=pygame.sprite.spritecollide(b,gp1,False,pygame.sprite.collide_rect)

    if isinstance(col[0],Wall):
        va[1]*=-1
        Sons.sounds['CP'].play() if not(mute) else None
    
    if isinstance(col[0],Player):
        va[0]*=-1
        
        Sons.sounds['CJ'].play() if not(mute) else None

    return va

def move_ball(b,pontos,va):
    '''
    Responsável por mover a bola no jogo
    '''

    global Sons,mute

    if b.rect.right>635:            
        pontos[0]+=1

    if b.rect.left<5:
        pontos[1]+=1

    if any((b.rect.right>635,b.rect.left<5)):
        b.rect.center=[320,240]
        va=[c([2,-2]),c([2,-2])]
        Sons.sounds['MP'].play() if not(mute) else None
        

   
    b.rect.x+=va[0]
    b.rect.y+=va[1]

    return pontos,va

def desenhar():
    '''
    Responsável por desenhar os elementos da tela numa posição fixa e definir algumas váriaveis básicas
    '''
    
    ball=Ball((320,240))
    p1,p2=Player((10,240)),Player((630,240))
    gp1=pygame.sprite.LayeredUpdates()

    gp1.add([ball,p1,p2,Wall((0,0)),Wall((0,460)),Center((320,238))])

    gp1.change_layer(ball,1)

    va=[c([2,-2]),c([2,-2])]
    pontos=[0,0]

    return ball,gp1,p1,p2,va,pontos