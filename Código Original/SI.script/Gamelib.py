import pickle
import pygame
from pygame.locals import *
from sys import exit

pygame.init()
pygame.mixer.init()

#criar uma propriedade na classe sounds

def reverseColor(color):
    '''
    inverte uma cor escrita em rgb ou rgba
    inverts a color in RGB or RGBA format
    '''

    rcor=[]
    for i in color: rcor.append((i-255)*-1)
    return tuple(rcor)

def groupCall(method=('method','(args)'),*gps):
    '''
    Chama um método para todos os grupos passados como argumento,atualmente só está configurado para chamar o método update e o draw
    Calls a method for all groups passed as an argument, currently it is only configured to call the update method and the draw method
    '''

    for group in gps:
        if method=='update':
            group.update()

        elif method[0]=='draw' and isinstance(method[1],pygame.Surface):
            group.draw(method[1])

def checkMax():
    '''
    verifica uma possível pontuação máxima existente,atribuí o valor a maxpt caso exista, caso contrário atribuí 0 a maxpt para que um novo recorde seja estabelecido
    checks for a possible existing maximum score, assigns the value to maxpt if it exists, otherwise assigns 0 to maxpt so that a new record is established
    '''

    try:
        aq=open('Maxpt.pck','rb')
        maxpt=pickle.load(aq)
        aq.close()
    
    except:
        maxpt=0
    
    return maxpt

def updateMax(pontos,maxpt):
    '''
    Atualiza a pontuação máxima caso o jogador ultrapasse a pontuação máxima atual e guarda o novo valor num arquivo chamado maxpt
    Updates the maximum score if the player exceeds the current maximum score and saves the new value in a file called maxpt
    '''

    if pontos>maxpt:
        maxpt=pontos
        aq=open('Maxpt.pck','wb')
        pickle.dump(maxpt,aq)
        aq.close()
    
    return maxpt

def pause(tela,fonte,msgs,mute,cfg=((260,450),(20,300),(255,255,255),None,False,()),*gps):
    '''
    responsável por pausar o jogo criando um loop paralelo
    os argumentos são para configurar a tela de pause de acordo com o jogo que você está a fazer.

    o argumento cfg(config) deve ser uma tupla de três elementos,o primeira sendo a posição do texto de pause,o segundo sendo a posição do texto de mute e o terceiro sendo a cor.

    responsible for pausing the game by creating a parallel loop
    the arguments are to configure the pause screen according to the game you are creating

    the parameter cfg(config) must be a tuple of three elements, the first being the position of the pause text, the second being the position of the mute text and the third being the color
    
    '''

    while True:
        tela.fill((cfg[2]))
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                exit()

            if event.type==KEYDOWN:
                if event.key==K_p:
                    return

        groupCall(('draw',tela),*gps)

        for fc in cfg[5]:
            try:
                fc()
            except:
                pass

        for msg in msgs: tela.blit(fonte.render(msg,cfg[4],reverseColor(cfg[2])),msgs[msg])
            
        if mute: tela.blit(fonte.render('Mutado!',False,reverseColor(cfg[2])),cfg[0])
        
        try:
            tela.blit(cfg[3].render('Pausado!',False,reverseColor(cfg[2])),cfg[1]) 
        
        except:
            tela.blit(fonte.render('Pausado!',False,reverseColor(cfg[2])),cfg[1]) 

        pygame.display.flip()
     

class Sound_group(object):
    def __init__(self,vol=0.5,**sons):
        '''
        Um contâiner simples para lidar com sons oriundos da classe pygame.mixer.Sound da biblioteca pygame
        A simple container for handling sounds from the pygame.mixer.Sound class of the pygame library
        '''

        self._sounds=sons
        self.set_volume(vol)
    
    def set_volume(self,vol,sound=None):
        '''       
        Recebe um volume e ajusta todos os sons da coleção para aquele volume,se sound for instância de pygame.mixer.Sound,ajusta o volume apenas daquele item da coleção
        Receive a volume and adjust all sounds in the collection for that volume, if sound is an instance of pygame.mixer.sound, adjust the volume only for that item in the collection
        '''
        if sound==None:
            for s in self.sounds:
                self.sounds[s].set_volume(vol)

        elif isinstance(sound, str):
            self.sounds[sound].set_volume(vol)
    
    def play(self,sound,mute=False):
        '''
        Recebe um som presente na coleção e o reproduz caso mute seja False
        Receives a sound present in the collection and plays it if the mute is False
        '''

        if not(mute): 
            self.sounds[sound].play()

    def add(self,**sounds):
        '''
        recebe um dicionário de sons e os adiciona a coleção
        receive's a dictionary of sounds and add them to the collection
        '''

        for sound in sounds:
            if isinstance(sounds[sound],pygame.mixer.Sound):
                self._sounds[sound]=sounds[sound]

            else:
                raise TypeError('sound items must be instance of pygame.mixer.Sound')

    def remove(self,key):
        '''
        recebe uma chave que corresponde a um som da coleção,e o remove
        receive's a key that match's a sound of the collection,and then delete it    
        thats different of the deleter of self._sounds,which resets the collection
        '''

        del self._sounds[str(key)]
    
    @property
    def sounds(self):
        return self._sounds

    @sounds.setter
    def sounds(self,sons):
        for sound in sons:
            if isinstance(sons[sound],pygame.mixer.Sound):
                self.sounds[sound]=sons[sound]

            else:
                raise TypeError('sound items must be instance of pygame.mixer.Sound')

    @sounds.deleter
    def sounds(self):
        self.sounds={}


def Funcall(funcargs,functions):
    '''
    recebe um grupo de funções e outro de argumentos, e os chama

    '''

    for i in range(len(functions)):
        functions[i](*funcargs[i])


def mainLoop(**kwargs):

    '''
    Loop Principal Genérico de um jogo feito em pygame
    Generic mainloop in a pygame made game
    '''

    for key in kwargs:#Verificação de argumentos válidos
        if key not in ['Screen','Functions','Funcargs','Tick','Gps','Color']:
            raise TypeError('%s not allowed!'%key)

    clock=pygame.time.Clock(kwargs['Tick'])

    while True:
        kwargs['Screen'].fill((kwargs['Color']))

        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                exit()

        Funcall(kwargs['Funcargs'], ['Functions'])

        groupCall(['draw',kwargs['Screen']],kwargs['Gps'])
        groupCall('update',kwargs['Gps'])

        clock.tick()

        pygame.display.flip()

            



'''
1-fazer com que a função mainloop trabalhe com um dicionário de argumentos
2-permitir manipulação de eventos pela função, tanto eventos contínuos como eventos individuais
3-


        
mainLoop(
    Func='bcd',
    Screen='abc'

)

'''