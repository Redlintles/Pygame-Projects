import pygame
from pygame.locals import *
from sys import exit
import os
from SI_Sprites import *
from random import choice as c
from Gamelib import Sound_group
import pickle

pygame.init()
pygame.mixer.init()

som=pygame.mixer.Sound

with open('./Config.pck','rb') as arq:
    vol=pickle.load(arq)
    if vol<0.1:
        mute=True
    else:
        mute=False

Sons=Sound_group(vol,
    Death=som('./Sons/Death.wav'),
    Kill=som('./Sons/Kill.wav'),
    Powercube=som('./Sons/Powercube.wav'),
    TA=som('./Sons/TA.wav'),
    Tiro=som('./Sons/Tiro.wav'),
    TP=som('./Sons/TP.wav')
)

def ch_mute():
    global mute
    mute=not(mute)
    return mute

def colisão(player,va,tela,te,morreu,pontos,*gps):

    global Sons,mute
    #Checa as possíveis colisões causadas pelo player(P>E,P>A)
    for i in gps[5]:#Colisão P>E
        col_pe=pygame.sprite.spritecollide(i,gps[1],False,pygame.sprite.collide_mask)
        col_pa=pygame.sprite.spritecollide(i,gps[0],False,pygame.sprite.collide_mask)
        if col_pe:
            i.kill()
            col_pe[0].life-=1

        elif col_pa:#Colisão P>A
            if i.pws==False:#o tiro não será deletado ao atingir um alien caso esse tiro seja perfurante
                i.kill()

            gps[2].add(Explosion((col_pa[0].rect.center)))
            col_pa[0].kill()
            Sons.sounds['Kill'].play() if not(mute) else None
            pontos+=1
            if len(gps[0])<=10:#toda vez que o número de aliens for menor que 10 e o jogador matar um,a velocidade dos restantes aumenta
                va[0]+=1
            #caso o player mate um alien,ele tem 3% de chance de dropar um powercube
            if c([1,1,1]+[0 for x in range(97)]) and len(gps[3])==0:
                gps[3].add(Powercube(col_pa[0].rect.center))

    #Colisões causadas pelos Aliens(A>E,A>P)
    for i in gps[4]:#colisão A>E
        col_ae=pygame.sprite.spritecollide(i,gps[1],False,pygame.sprite.collide_mask)
        col_ap=pygame.sprite.spritecollide(player,gps[4],False,pygame.sprite.collide_mask)
        if col_ae:
            i.kill()
            col_ae[0].life-=len(col_ae)

        elif col_ap:#colisão A>P
            i.kill()
            gps[2].add(Explosion((player.rect.center)))
            player.kill()
            Sons.sounds['Death'].play() if not(mute) else None
            morreu=True

    #Caso o jogador pegue um powercube,seu tiro se torna perfurante
    if pygame.sprite.spritecollide(player,gps[3],True,pygame.sprite.collide_mask):
        te=True
        player.image=player.img[1]
        Sons.sounds['Powercube'].play() if not(mute) else None

    return morreu,pontos,te

def Atirar_p(coord_tiro,te,player,gp_tp):
    '''
    Responsável por fazer o player atirar
    '''

    global Sons,mute
    if len(gp_tp)<3:
        tiro=T_p(coord_tiro)

        if not(te):
            Sons.sounds['Tiro'].play() if not(mute) else None

        if te:
            tiro.pws=True
            te=False
            player.image=player.img[0]
            Sons.sounds['TP'].play() if not(mute) else None
        
        gp_tp.add(tiro)
    
    return gp_tp,te

def mal(gp_aliens,direct,va,nexty):
    '''
    Responsável por mover os aliens pela tela
    a abreviação siginifica move aliens
    '''

    #Movimentação Lateral
    if direct[0] == 'E' and all((x.rect.topright[0]<640 for x in gp_aliens)):
        for i in gp_aliens:
            i.rect.x+=va[0]

    else :
        direct[0]='W'
    
    if direct[0] == 'W' and all((x.rect.topleft[0]>0 for x in gp_aliens)):
        for i in gp_aliens:
            i.rect.x-=va[0]

    else:
        direct[0]='E'

    #Movimentação Vertical
    def movey(x,gp_aliens):
        if x:
            for i in gp_aliens:
                i.rect.y+=va[1]
        else:
            for i in gp_aliens:
                i.rect.y-=va[1]
    
    if any((x.rect.topleft[0]<=0 for x in gp_aliens)) or any((x.rect.topright[0]>=640 for x in gp_aliens)):
        if direct[1]=='S' and all((x.rect.bottom<=320 for x in gp_aliens)):
            movey(1,gp_aliens)
            if any((x.rect.topright[0]>=640 for x in gp_aliens)):
                movey(1,gp_aliens)

        elif direct[1]=='N' and all((x.rect.top>=0 for x in gp_aliens)):
            movey(0,gp_aliens)
            if any((x.rect.topright[0]>=640 for x in gp_aliens)):
                movey(0,gp_aliens)

        elif any((x.rect.top <=0 for x in gp_aliens)):
            direct[1]='S'

        elif any((x.rect.bottom >=320 for x in gp_aliens)):
            direct[1]='N'
    
    #Aumenta A Velocidade Dos Aliens Conforme o Player Os Mata
    if len(gp_aliens)==nexty and nexty!=10:
        nexty-=5
        va[0]+=1

    return direct,va,nexty

def Atirar_a(gp_aliens,gp_ta):
    '''
    Responsável por fazer os aliens atirarem
    '''

    at=c(list(gp_aliens))
    if len(gp_ta)<15:
        #Tiro Triplo Paralelo
        if isinstance(at,A1):
            for i in range(0,9,4):
                gp_ta.add(T_a((at.rect.center[0]-i-8,at.rect.center[1]+10)))
        #Tiro Paralelo
        elif isinstance(at,A2):
            gp_ta.add(T_a((at.rect.center[0]-4,at.rect.center[1]+10)))
            gp_ta.add(T_a((at.rect.center[0]+4,at.rect.center[1]+10)))
        #Tiro Triplo Sequencial
        elif isinstance(at,A3):
            for i in range(10,70,20):
                gp_ta.add(T_a((at.rect.center[0],at.rect.center[1]+i)))
        #Tiro Paralelo Duplo
        elif isinstance(at,A4):
            for i in range(10,31,20):
                gp_ta.add(T_a((at.rect.center[0]-4,at.rect.center[1]+i)))
                gp_ta.add(T_a((at.rect.center[0]+4,at.rect.center[1]+i)))

def CA(gp_aliens):
    '''
    Cria os aliens Na Tela
    '''

    l=(A1,A2,A3,A4)

    for i in range(1,6):
        if i < 5:
            obj=l[i-1] 

        else:
            obj=l[0]  
             
        for j in range(1,13):
            al=obj((52*j,45*i))
            if i < 5:
                gp_aliens.add(al)

            else:
                gp_aliens.add(al)


def CE(gp_escudos):
    '''
    Cria os escudos na tela
    '''

    for i in range(1,6):
        gp_escudos.add(Shield((105*i,370)))

def define(x=0):
    '''
    Responsável por definir e reiniciar as varíaveis
    '''
    gp_aliens=pygame.sprite.Group()#grupo que armazenará os aliens
    gp_escudos=pygame.sprite.Group()#grupo que armazenará os escudos
    gp_pc=pygame.sprite.Group()#grupo que armazenará os powercubes
    va=[1,5]#velocidade de movimento dos aliens
    direct=['E','S']#direção de movimento dos aliens
    nexty=50#quando a quantidade de aliens for igual a nexty,a velocidade deles será aumentada
    CA(gp_aliens)#adiciona os aliens ao grupo
    gp_tp=pygame.sprite.Group()#grupo que armazenará os tiros do player
    gp_ta=pygame.sprite.Group()#grupo que armazenará os tiros dos aliens
    player=Player()#player
    gp1=pygame.sprite.Group();gp1.add(player)#grupo que armazenará o player
    coord_tiro=[320,400]#posição de onde o tiro do player irá sair
    pontos=0#pontos
    pws=False#indica se o player está com o super-tiro ativo
    te=False#indica se o player pegou o powercube,e consequentemente,está com o super-tiro ativo
    morreu=False#indica se o player morreu

    if x:#se o player tiver morrido todas as váriáveis redefinidas acimas serão retornadas
        gp_escudos=pygame.sprite.Group()
        CE(gp_escudos)
        return gp_aliens,gp_escudos,va,direct,nexty,gp_ta,gp_tp,gp1,coord_tiro,player,gp_pc,pontos,pws,te,morreu
    else:#se o player tiver ganho uma partida,ele entra no modo de sobrevivência onde os escudos não recuperam vida entre os rounds,e a pontuação também não será reiniciada
        return gp_aliens,va,direct,nexty,gp_ta,gp_tp,gp1,coord_tiro,player,gp_pc,pws,te,morreu

