import pygame
from pygame.locals import *
from Pong_sprites import *
import os
from random import choice as c

pygame.init()
pygame.mixer.init()

fonte=pygame.font.SysFont('arial',50,True,True)
fonte1=pygame.font.SysFont('arial',20,True,True)

CJ=pygame.mixer.Sound(os.path.join(os.getcwd(),'CJ.wav')) ; CJ.set_volume(0.5)
CP=pygame.mixer.Sound(os.path.join(os.getcwd(),'CP.wav')) ; CP.set_volume(0.5)
MP=pygame.mixer.Sound(os.path.join(os.getcwd(),'MP.wav')) ; MP.set_volume(0.5)

def pausar(pause,mute,gp,tela,pontos):
    '''
    Responsável por pausar o jogo
    '''

    global fonte,fonte1

    from sys import exit

    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                exit()

            if event.type==KEYDOWN:
                
                if event.key==K_p:
                    pause=not(pause)
                    return pause

        gp.draw(tela)

        if mute:
            tela.blit(fonte1.render('Mutado!',True,(255,255,255)),(200,430))

        tela.blit(fonte.render('%i'%pontos[0],True,(255,255,255)),(200,240))
        tela.blit(fonte.render('%i'%pontos[1],True,(255,255,255)),(400,240))

        tela.blit(fonte1.render('Pausado!',True,(255,255,255)),(360,430))

        pygame.display.flip()

def colisão(b,gp1,mute,va):
    '''
    Responsável pela detecção de colisão do jogo
    '''

    global CP,CJ

    col=pygame.sprite.spritecollide(b,gp1,False,pygame.sprite.collide_rect)

    if isinstance(col[0],Wall):
        va[1]*=-1
        CP.play() if not(mute) else None
    
    if isinstance(col[0],Player):
        va[0]*=-1
        
        CJ.play() if not(mute) else None

    return va

def move_ball(b,pontos,va,mute):
    '''
    Responsável por mover a bola no jogo
    '''

    global MP

    if b.rect.right>635:            
        pontos[0]+=1

    if b.rect.left<5:
        pontos[1]+=1

    if any((b.rect.right>635,b.rect.left<5)):
        b.rect.center=[320,240]
        va=[c([2,-2]),c([2,-2])]
        MP.play() if not(mute) else None
   
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