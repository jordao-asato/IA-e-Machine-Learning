import pygame, random
from pygame.locals import *
from random import uniform
import asyncio
from threading import Thread

PRETO = (0,0,0)
BRANCO = (255,255,255)
VERDE = (0,255,0)
VERMELHO = (255,0,0)

gameOver = False
TAMANHO = (800, 600)

tela = pygame.display.set_mode(TAMANHO)
tela_retangulo = tela.get_rect()

pygame.display.set_caption("rede neural jogando pong")

posicaoYraquete = 0

class Raquete:
    def __init__(self, tamanho):
        self.imagem = pygame.Surface(tamanho)
        self.imagem.fill(VERDE)
        self.imagem_retangulo = self.imagem.get_rect()
        self.imagem_retangulo[0] = 0 # lado esquerdo da tela

    def move(self, y):
        self.imagem_retangulo[1] += y * 6 # move 10 pixels para cima ou pra baixo

        global posicaoYraquete
        posicaoYraquete = self.imagem_retangulo.centery # atualiza a posição global da raquete

    def atualiza(self, tecla):
        if tecla > 0.5:
            self.move(-1) # sobe
        elif tecla < 0.5:
            self.move(1) # desce
        self.imagem_retangulo.clamp_ip(tela_retangulo) # impedir que a raquete saia da tela

    def realiza(self):
        tela.blit(self.imagem, self.imagem_retangulo) # desenha a raquete na tela

posicaoYbola = 0

posicaoXbola = 0

erro = 0

class Bola:
    def __init__(self, tamanho):
        self.altura, self.largura = tamanho
        self.imagem = pygame.Surface(tamanho)
        self.imagem.fill(VERMELHO)
        self.imagem_retangulo = self.imagem.get_rect()
        self.setBola() # posição e velocidade inicial
        global erro
        self.erro = 0 # será usado no aprendizado da rede neural


    # valores fora da faixa 0.5 e -0.5 para evitar movimentos lentos
    def aleatorio(self):
        while True:
            num = random.uniform(-1,1)
            if num > -0.5 and num < 0.5:
                continue
            else:
                return num

    # começa no centro da tela
    def setBola(self):
        x = self.aleatorio()
        y = self.aleatorio()
        self.imagem_retangulo.x = tela_retangulo.centerx
        self.imagem_retangulo.y = tela_retangulo.centery
        self.velo = [x, y]
        self.pos = list(tela_retangulo.center)

    def colideParede(self):
        if self.imagem_retangulo.y <= 0 or self.imagem_retangulo.y > tela_retangulo.bottom - self.altura:
            self.velo[1] *= -1 # Inverte a direção no eixo Y (rebate nas bordas superiores e inferiores)

        if self.imagem_retangulo.x <= 0 or self.imagem_retangulo.x > tela_retangulo.right - self.largura:
            self.velo[0] *= -1 # inverte a direção no X
            if self.imagem_retangulo.x <= 0:
                placar1.pontos -= 1 # perde um ponto se tocar na parede esquerda
                print("bateu na parede !")

                #self.erro = (posicaoYraquete - posicaoYbola)/10
                #rede.atualizaPesos(self.erro)


    def move(self): #movimento vertical e horizontal da bola
        self.pos[0] += self.velo[0] * 2 # x

        self.pos[1] += self.velo[1] * 2 # y
        self.imagem_retangulo.center = self.pos #atualiza a posicao grafica da bola

    def colideRaquete(self, raqueteRect):
        if self.imagem_retangulo.colliderect(raqueteRect): # colidiu com a raquete?
            self.velo[0] *= -1 # inverte a direção horizontal (rebote)
            placar1.pontos += 1
            print('voce defendeu')
            #self.erro = 0

            global erro
            erro = 0 # zera o erro para a NN entender que a defesa foi bem sucedida



    # verifica colisão com a parede, att as posições da bola, verifica a posição com a raquete e move a bola
    def atualiza(self, raqueteRect): #chamada em cada frame
        self.colideParede()
        global posicaoYbola, posicaoXbola
        posicaoYbola = self.imagem_retangulo.y
        posicaoXbola = self.imagem_retangulo.x
        self.colideRaquete(raqueteRect=raqueteRect)
        self.move() #mover bola no eixo X e Y 

    def realiza(self):
        tela.blit(self.imagem, self.imagem_retangulo) # renderizar a bola na tela



class Placar:
    def __init__(self):
        pygame.font.init()
        self.fonte = pygame.font.Font(None, 36) # fonte do placar
        self.pontos = 0

    def contagem(self):
        self.text = self.fonte.render("Pontos = " + str(self.pontos), 1, (255,255,255))
        self.textpos = self.text.get_rect() # posicionar o texto
        self.textpos.centerx = tela.get_width() / 2 # centraliza no x
        tela.blit(self.text, self.textpos) # desenha o texto na tela
        tela.blit(tela, (0,0)) # atualiza a tela

#pixels da raquete e da bola e um placar zerado
raquete = Raquete((10,100))
bola = Bola((15,15))
placar1 = Placar()

#guarda a saida da rede neural para determinar se a raquete sobe ou desce
tecla = 0

import numpy as np

# cria um vetor de 4 pesos aleatórios entre -1 e 1, na primeira camada, um pra cada entrada do neurônio + bias
# 2 na entrada: combinar as informações das entradas e criar representações mais complexas
pesosPrimeiroNeuronioCamadaEntrada = np.array([uniform(-1, 1) for i in range(4)])
pesosSegundoNeuronioCamadaEntrada = np.array([uniform(-1, 1) for i in range(4)])

# aqui são 2 pesos pois chegam 2 pesos nesta camada
pesosPrimeiroNeuronioCamadaOculta = np.array([uniform(-1, 1) for i in range(2)])
pesosSegundoNeuronioCamadaOculta = np.array([uniform(-1, 1) for i in range(2)])

pesosNeuronioDeSaida = np.array([uniform(-1, 1) for i in range(2)])

class RedeNeural(Thread):
    # 3 entradas e o bias
    def __init__(self, YRaquete, XBolinha, YBola, bias = -1):

        self.entradas = np.array([YRaquete, XBolinha, YBola, bias])
        global pesosPrimeiroNeuronioCamadaEntrada, pesosSegundoNeuronioCamadaEntrada, pesosPrimeiroNeuronioCamadaOculta, pesosSegundoNeuronioCamadaOculta

        # pegando os pesos globais da rede neural para os neurônios da camada de entrada, camada oculta e saída, pra nao ter que recria-los a cada chamada
        self.pesosPrimeiroNeuronioCamadaEntrada = pesosPrimeiroNeuronioCamadaEntrada
        self.pesosSegundoNeuronioCamadaEntrada = pesosSegundoNeuronioCamadaEntrada

        self.pesosPrimeiroNeuronioCamadaOculta = pesosPrimeiroNeuronioCamadaOculta
        self.pesosSegundoNeuronioCamadaOculta = pesosSegundoNeuronioCamadaOculta

        self.pesosNeuronioDeSaida = pesosNeuronioDeSaida

    # entrada -> saída
    def feedforward(self):

        # multiplica as entradas pelos pesos dos neurônios da camada de entrada -> função de ativação (tanh)
        self.saidaPrimeiroNeuronioCamadaEntrada = round(self.tangenteHiperbolica(np.sum(self.entradas * self.pesosPrimeiroNeuronioCamadaEntrada)), 6)

        self.saidaSegundoNeuronioCamadaEntrada = round(self.tangenteHiperbolica(np.sum(self.entradas * self.pesosSegundoNeuronioCamadaEntrada)), 6)

        # pega os resultados da camada de entrada e multiplica pelos pesos da camada oculta
        self.saidaPrimeiroNeuronioCamadaOculta = round(self.tangenteHiperbolica(np.sum(np.array([self.saidaPrimeiroNeuronioCamadaEntrada, self.saidaPrimeiroNeuronioCamadaEntrada])  * self.pesosPrimeiroNeuronioCamadaOculta )), 6)

        self.saidaSegundoNeuronioCamadaOculta = round(self.tangenteHiperbolica(np.sum(np.array([self.saidaPrimeiroNeuronioCamadaEntrada, self.saidaSegundoNeuronioCamadaEntrada]) * self.saidaSegundoNeuronioCamadaEntrada )), 6)

        # saída passa pela sigmoid, o que vai decidir se a raquete sobe ou desce
        self.resultado = round(self.sigmoid(np.sum(np.array([self.saidaPrimeiroNeuronioCamadaOculta, self.saidaSegundoNeuronioCamadaOculta]) * self.pesosNeuronioDeSaida)),6)

        return self.resultado





    # 1 e -1
    def tangenteHiperbolica(self, x):

        th = (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))
        return th


    # euler
    # converter os valores da camada oculta entre 0 e 1
    def sigmoid(self,x):
        return 1 / (1 + np.exp(-x))



    # atualiza de acordo com o erro
    # lembrando que erro = diferença entre posição da raquete e posição da bola
    # alpha = taxa de aprendizado
    def atualizaPesos(self, erro, alpha=0.01):

        for i in range(len(pesosNeuronioDeSaida)):
            if i == 0:
                entrada = self.saidaPrimeiroNeuronioCamadaOculta
            elif i ==1:
                entrada = self.saidaSegundoNeuronioCamadaOculta

            pesosNeuronioDeSaida[i] = pesosNeuronioDeSaida[i] + (alpha * entrada * erro)

        for i in range(len(pesosPrimeiroNeuronioCamadaOculta)):
            if i == 0:
                entrada1 = self.saidaPrimeiroNeuronioCamadaEntrada
            if i == 1:
                entrada1 = self.saidaSegundoNeuronioCamadaEntrada

            pesosPrimeiroNeuronioCamadaOculta[i] = pesosPrimeiroNeuronioCamadaOculta[i] + (alpha * entrada1 * erro)

        for i in range(len(pesosSegundoNeuronioCamadaOculta)):
            if i == 0:
                entrada2 = self.saidaPrimeiroNeuronioCamadaEntrada
            if i == 1:
                entrada2 = self.saidaSegundoNeuronioCamadaEntrada

            pesosSegundoNeuronioCamadaOculta[i] = pesosSegundoNeuronioCamadaOculta[i] + (alpha * entrada2 * erro)

        for i in range(len(pesosPrimeiroNeuronioCamadaEntrada)):
            pesosPrimeiroNeuronioCamadaEntrada[i] = pesosPrimeiroNeuronioCamadaEntrada[i] + (alpha * self.entradas[0] * erro)

        for i in range(len(pesosSegundoNeuronioCamadaEntrada)):
            pesosSegundoNeuronioCamadaEntrada[i] = pesosSegundoNeuronioCamadaEntrada[i] + (alpha * self.entradas[0] * erro)


        print(self.resultado)

while not gameOver:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            gameOver = True


    rede = RedeNeural(posicaoYraquete/600, posicaoXbola/800, posicaoYbola/600)
    tecla = rede.feedforward()

    with open('dadosTreinamento.txt', 'a') as arquivo:
        arquivo.write(str(posicaoYraquete) + " " + str(posicaoXbola) + " " + str(posicaoYbola) + " " + str(tecla) + "\n")

    tela.fill(PRETO)
    raquete.realiza()
    bola.realiza()
    raquete.atualiza(tecla) # raquete atualiza de acordo com a saída da NN
    bola.atualiza(raquete.imagem_retangulo) #move a bola e verifica colisões


    erro = (posicaoYraquete - posicaoYbola) / 100
    rede.atualizaPesos(erro)

    placar1.contagem()
    pygame.display.update()



