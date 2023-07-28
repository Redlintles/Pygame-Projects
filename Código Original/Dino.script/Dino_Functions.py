import pygame
from pygame.locals import *
from Dino_Sprites import *
from random import choice as c
from sys import exit
import pickle
from Gamelib import *

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
    Jump=som('./Sons/Jump.wav'),
    Score=som('./Sons/Score.wav')
)
def ch_mute():
    global mute
    mute=not(mute)
    return mute

def add(gpc,gpn,speed):
    for i in range(10):
        gpc.add(Floor(speed[0],(i*108,416)))

    for i in range(4):
        nuvem=Cloud(speed[1],(715+75*c([1,2,3,4,5]),100+30*c([1,2,3])))
        gpn.add(nuvem)

    m=Moon(speed[1],(550,84))
    gpn.add(m)
    gpn.add(Star(speed[2],(664,20)),Star(speed[2],(700,100)),Star(speed[2],(784,120)),Star(speed[2],(822,50)),Star(speed[2],(951,85)))

    return gpc,gpn

def define():
    noite=False
    chcor=True
    ctexto=[41,38,38]
    pontos=0
    nexty=100
    speed=[20,2,1]
    cor=[214,217,217]
    gpc,gpn=add(pygame.sprite.Group(),pygame.sprite.LayeredUpdates(),speed)
    ob=Cacto1(noite,speed[0],(700,380))
    gpobs=pygame.sprite.Group(ob)
    gps=pygame.sprite.Group()
    d=Dino((100,380))
    gpd=pygame.sprite.Group(d)

    return pontos,noite,chcor,cor,gpc,gpn,ob,gpobs,gps,gpd,ctexto,nexty,d,speed

def mcor(cor,ctexto,mode):

    if not(mode): 
        if cor[0]!=41:
            cor[0]-=1

        if cor[1]!=38:
            cor[1]-=1 ; cor[2]-=1
        
        if ctexto[0]!=214:
            ctexto[0]+=1
        
        if ctexto[1]!=217:
            ctexto[1]+=1;ctexto[2]+=1
    
    else:
        if cor[0]!=214:
            cor[0]+=1

        if cor[1]!=217:
            cor[1]+=1 ; cor[2]+=1
        
        if ctexto[0]!=41:
            ctexto[0]-=1
        
        if ctexto[1]!=38:
            ctexto[1]-=1;ctexto[2]-=1

    return cor,ctexto

def glow_notglow(*gps):
    for gp in gps:
        for spr in gp:
            try:
                spr.ch_spr()
            except:
                pass



def color_controller(chcor,ctexto,cor):
    if not(chcor):
        for i in range(8): cor,ctexto=mcor(cor,ctexto,0)

    else:
        for i in range(8): cor,ctexto=mcor(cor,ctexto,1)

    

    return cor,ctexto

def choose(gpobs,ob,noite,speed):
    newob=c([Cacto1,Cacto2,Cacto3,Ptero])
    if gpobs.has(ob):
        return gpobs,ob
    
    else:
        if newob==Ptero:
            ob=newob(noite,speed[0],(700,c([300,350,370])))
        else:
            ob=newob(noite,speed[0],(700,380))
        gpobs.add(ob)
        return gpobs,ob


def col(maxpt,pontos,d,noite,gpobs,tela,fonte,ctexto,*gps):

    global mute

    if pygame.sprite.spritecollide(d,gpobs,False,pygame.sprite.collide_mask):
        Sons.sounds['Death'].play() if not(mute) else None
        updatemax(pontos,maxpt)

        d.image=d.img[6] if noite else d.img[7]

        while True:
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    exit()
                
                if event.type==KEYDOWN:
                        return True

            for i in gps:
                i.draw(tela)

            gpobs.draw(tela)

            tela.blit(fonte.render('Mutado!',False,ctexto),(280,460)) if mute else None
            tela.blit(fonte.render('Você Perdeu! Aperte Qualquer tecla para começar de novo!',False,ctexto),(30,230))
            tela.blit(fonte.render('Maxpt:%i'%maxpt,False,ctexto),(500,460))
            tela.blit(fonte.render('Pontos:%i'%int(pontos),False,ctexto),(0,460))
            pygame.display.flip()

    return False

def mudafundo(speed,d,pontos,chcor,noite,nexty,*gps):

    global mute

    if int(pontos)==nexty:
        chcor=not(chcor)
        glow_notglow(*gps)
        noite=not(noite)
        speed=increasespeed(speed,*gps)
        nexty+=100
        Sons.sounds['Score'].play() if not(mute) else None

    return chcor,noite,nexty,speed
    
def increasespeed(speed,*gps):
    speed[0]+=5
    for group in gps:
        for spr in group:
            if isinstance(spr,Star):
                spr.speed+=speed[2]
            elif isinstance(spr,(Cloud,Moon)):
                spr.speed+=speed[1]
            else:
                spr.speed+=5
    
    return speed

