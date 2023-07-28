from random import choice as c
import pygame
from pygame.locals import *
from sys import exit
from Snake_Sprites import *
import pickle
from Gamelib import *
pygame.init()

som=pygame.mixer.Sound

with open('./Config.pck','rb') as arq:
    vol=pickle.load(arq)
    if vol<0.1:
        mute=True
    else:
        mute=False

Sons=Sound_group(vol,
    Eat=som('./Sons/Comer.wav'),
    Death=som('./Sons/Death.wav')
)

def ch_mute():
    global mute
    mute=not(mute)
    return mute

def newall(gpw):
    '''
    cria as paredes em posições completamente aleatórias
    '''

    for i in range(9):
        n=(c([x for x in range(42,598,42)]),c([x for x in range(42,438,42)]))

        while n[0] in ((x for x in range(210,420,42))) or n[1] in ((x for x in range(168,294,42))):
            n=(c([x for x in range(42,598,42)]),c([x for x in range(42,438,42)]))
        
        gpw.add(Wall(n))

    return gpw

def newseg(corpo,tela):
    '''
    Cuida da adição de novos segmentos ao jogador
    '''
    rects=[]
    for coords in corpo:
        rects.append(pygame.draw.rect(tela,(0,255,0),(coords[0],coords[1],20,20)))
    return rects

def define():
    '''
    Cuida da inicialização e reinicialização das variáveis
    '''

    pcobra=[310,230]
    pcomida=[c([x for x in range(40,600,10)]),c([x for x in range(0,470,10)])]
    lencobra=5
    morte=False
    pc=[c((-10,10)),0]
    corpo=[]
    pontos=0
    gpc,gpw=pygame.sprite.Group(),pygame.sprite.Group()
    gpw=newall(gpw)

    return pcobra,pcomida,lencobra,morte,pc,corpo,pontos,gpc,gpw

def youredead(morte,pcobra,pcomida,lencobra,pc,corpo,pontos,tela,fonte):
    '''
    Cuida das ações a serem tomadas quando o jogador morrer
    '''

    global Sons,mute

    morte=True
    Sons.sounds['Death'].play() if not(mute) else None
    while morte:
        tela.blit(fonte.render('Você Perdeu,Aperte Espaço para jogar de novo!',False,(0,0,0)),(30,240))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                exit()

            if event.type==KEYDOWN:
                if event.key==K_SPACE:
                    return define()



def WallCollide(head,gp):
    '''
    Verifica exclusivamente a colisão com as paredes azuis
    '''

    for i in gp:
        if head.colliderect(i.rect):
            return True

    return False
