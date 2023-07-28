from random import choice as c
import pygame
from pygame.locals import *
from sys import exit
from Snake_Sprites import *
import pickle
pygame.init()

def Pause(pontos,tela,fonte,corpo,gpc,gpw,mute):
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit() 
                exit()

            if event.type==KEYDOWN:
                if event.key==K_p:
                    return

        tela.blit(fonte.render('Pontos:%i'%pontos,False,(0,0,0)),(0,0))
        tela.blit(fonte.render('Pausado!',False,(0,0,0)),(520,450))
        if mute:
            tela.blit(fonte.render('Mutado!',False,(0,0,0)),(0,450))

        gpc.draw(tela)
        gpw.draw(tela)
        newseg(corpo,tela)
        pygame.display.flip()


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

def youredead(morte,Death,pcobra,pcomida,lencobra,pc,corpo,pontos,tela,fonte,mute):
    '''
    Cuida das ações a serem tomadas quando o jogador morrer
    '''
    morte=True
    Death.play() if not(mute) else None
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


def checkmax():
    try:
        aq=open('Maxpt.pck','rb')
        maxpt=pickle.load(aq)
        aq.close()

    except:
        maxpt=0
    
    return maxpt

def updatemax(maxpt,pontos):

    if pontos>maxpt:
        maxpt=pontos
        aq=open('Maxpt.pck','wb')
        pickle.dump(maxpt,aq)
        aq.close()
    
    return maxpt