import pygame
from pygame.locals import *
from sys import exit
import os
from SI_Sprites import *
from SI_Functions import *
from random import choice as c
from Gamelib import *

#Configurações básicas

pygame.init()
pygame.mixer.init()

tela=pygame.display.set_mode((640,480))
pygame.display.set_caption('Space Invaders')

fonte=pygame.font.SysFont('Helvetica',20,True,True)

maxpt=checkMax()

#Funções utilizadas durante o jogo

gp_explosion=pygame.sprite.Group()

gp_aliens,gp_escudos,va,direct,nexty,gp_ta,gp_tp,gp1,coord_tiro,player,gp_pc,pontos,pws,te,morreu=define(1)#definição das variáveis

relogio=pygame.time.Clock()#usado para definir o framerate do jogo
#preparação dos dois grupos criados anteriormente para o loop principal

while True:#Loop Principal
    tela.fill((0,0,0))#recolorização da tela
    keys=pygame.key.get_pressed()#checagem das teclas pressionadas a cada iteração do loop

    for event in pygame.event.get():#Checagem de eventos
        if event.type==QUIT:#Saída do jogo
            pygame.quit()
            exit()

        if event.type==KEYDOWN:#Checagem de botões
            if event.key==K_UP or event.key==K_w and len(gp_tp)<3:           
                gp_tp,te=Atirar_p(coord_tiro,te,player,gp_tp)

            if event.key==K_m:#mute
                mute=ch_mute()
                Sons.set_volume(0.1) if not(mute) else None

            if event.key==K_p:#pausa
                pause(tela,fonte,{'Pontos:%i'%pontos:(0,0),'Maxpt:%i'%maxpt:(540,0)},mute,[(0,450),(550,450),(0,0,0)],gp_tp,gp1,gp_escudos,gp_aliens,gp_ta,gp_explosion,gp_pc)

    maxpt=updateMax(pontos,maxpt)
               
    if keys[K_a] or keys[K_LEFT] and player.rect.bottomleft[0]>0:#Move o player para a esquerda
        player.rect.x-=5
        coord_tiro[0]-=5

    if keys[K_d] or keys[K_RIGHT] and player.rect.bottomright[0]<640:#Move o player para a direita
        player.rect.x+=5
        coord_tiro[0]+=5

    if len(gp_aliens)>0:#Faz um alien aleatório atirar a cada iteração do loop
        Atirar_a(gp_aliens,gp_ta)
    
    if len(gp_aliens)<=0 and not(morreu):#verifica se o player ganhou e inicializa o modo de sobrevivência caso ele queira jogar mais
        while True:
            tela.fill((0,0,0))
            keys=pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    exit()

            for i in range(3):
                gp_explosion.draw(tela)
                gp_explosion.update()

            tela.blit(fonte.render('Você Ganhou,Aperte S ou para baixo para chamar uma nova onda',False,(255,255,255)),(5,240))

            if keys[K_s] or keys[K_DOWN]:
                gp_aliens,va,direct,nexty,gp_ta,gp_tp,gp1,coord_tiro,player,gp_pc,pws,te,morreu=define()
                morreu=False
                break

            pygame.display.flip()

    if morreu:#cuida de reiniciar o jogo caso o player morra
        for i in (gp_tp,gp_escudos,gp_aliens,gp_ta,gp_explosion):
            for j in i:
                j.kill()

        while True:
            tela.fill((0,0,0))
            keys=pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    exit()
            
            if any([keys[K_s],keys[K_DOWN]]):
                morreu=False
                gp_aliens,gp_escudos,va,direct,nexty,gp_ta,gp_tp,gp1,coord_tiro,player,gp_pc,pontos,pws,te,morreu=define(1)
                pontos=0
                break
                        
            tela.blit(fonte.render('Você Perdeu,Aperte S ou para baixo para começar um novo jogo',False,(255,0,0)),(7,240))
            pygame.display.flip()
        
    else:
        direct,va,nexty=mal(gp_aliens,direct,va,nexty)#move os aliens pela tela
        relogio.tick(30)#regula o framerate do jogo para 30 frames por segundo
        groupCall(('draw',tela),gp_tp,gp1,gp_escudos,gp_aliens,gp_ta,gp_explosion,gp_pc)#Desenho dos elementos na tela
        groupCall('update',gp1,gp_tp,gp_escudos,gp_aliens,gp_ta,gp_explosion,gp_pc)#Atualização dos elementos na tela
        morreu,pontos,te=colisão(player,va,tela,te,morreu,pontos,gp_aliens,gp_escudos,gp_explosion,gp_pc,gp_ta,gp_tp)#checagem de colisão
        tela.blit(fonte.render('Pontos:%i'%pontos,False,(255,255,255)),(0,0))#Imprime a quantidade de pontos do jogador
        tela.blit(fonte.render('Maxpt:%i'%maxpt,False,(255,255,255)),(0,20))#Imprime a quantidade máxima de pontos do jogador

    if mute:
        tela.blit(fonte.render('Mutado!',False,(255,255,255)),(0,450))#Imprime a mensagem mutado para indicar ao jogador que o jogo está sem som

    pygame.display.flip()#Atualize a tela
    
    


