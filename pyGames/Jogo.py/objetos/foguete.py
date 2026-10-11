import math
import tkinter as tk

from lib.Colisao import place_meeting

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None


class Foguete:
    GRAVIDADE = 9.8
    PIXELS_POR_METRO = 50
    VELOCIDADE_MAXIMA = 600  # pixels por segundo
    MASSA_SECA_KG = 100_000  # 100 toneladas
    COMBUSTIVEL_INICIAL_KG = 100_000  # 100 toneladas
    FORCA_PROPULSAO_N = 2_000_000  # 2 x 10^6 N
    FRACAO_COMBUSTIVEL_POR_FRAME = 0.001
    ANGULO_INCLINACAO_GRAUS = 30

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 50
        self.altura = 50

        self.velocidade_x = 0.0  # pixels/s
        self.velocidade_y = 0.0  # pixels/s
        self.aceleracao_x = 0.0
        self.aceleracao_y = 0.0

        self.massa_seca = self.MASSA_SECA_KG
        self.combustivel_inicial = self.COMBUSTIVEL_INICIAL_KG
        self.combustivel = self.combustivel_inicial
        self.massa = self.massa_seca + self.combustivel
        self.energia = 0.0
        self.pontos = 0
        self.tempo_no_ar = 0.0
        self.esta_no_ar = True
        self.colidindo = False

        self.angulo = 0
        self.sprite = None
        self._sprite_original = None
        self._sprite_rotacionado = None

    def carregar_sprite(self, janela, caminho):
        self.sprite = tk.PhotoImage(master=janela, file=caminho)
        self.largura = self.sprite.width()
        self.altura = self.sprite.height()

        if Image is not None and ImageTk is not None:
            self._sprite_original = Image.open(caminho).convert("RGBA")
            self._sprite_rotacionado = ImageTk.PhotoImage(
                self._sprite_original,
                master=janela
            )

    def _atualizar_rotacao_sprite(self):
        if self._sprite_original is None or ImageTk is None:
            return
        imagem = self._sprite_original.rotate(
            -self.angulo,
            resample=Image.Resampling.BICUBIC,
            expand=True
        )
        self._sprite_rotacionado = ImageTk.PhotoImage(
            imagem,
            master=self.sprite.master
        )
        self.largura = imagem.width
        self.altura = imagem.height

    def verificar_coleta(self, coletavel):
        if coletavel.destruido:
            return

        if place_meeting(self, self.x, self.y, coletavel):
            self.pontos += coletavel.valor
            coletavel.destruido = True

    def atualizar(self, input, dT, largura_tela, altura_tela, local_pouso=None):
        if not self.esta_no_ar:
            return

        self.tempo_no_ar += dT
        x_anterior = self.x
        y_anterior = self.y

        # Inclinar para a esquerda/direita muda o ângulo do foguete
        # e a direção do vetor de empuxo, sem teletransporte lateral.
        if input.pressionada("Left"):
            self.angulo = -self.ANGULO_INCLINACAO_GRAUS
        elif input.pressionada("Right"):
            self.angulo = self.ANGULO_INCLINACAO_GRAUS
        else:
            self.angulo = 0
        self._atualizar_rotacao_sprite()

        massa_anterior = self.massa_seca + self.combustivel
        forca_x = 0.0
        forca_y = massa_anterior * self.GRAVIDADE

        if input.pressionada("space") and self.combustivel > 0:
            consumo = min(
                self.combustivel,
                self.combustivel_inicial * self.FRACAO_COMBUSTIVEL_POR_FRAME
            )
            self.combustivel -= consumo
            massa_atual = self.massa_seca + self.combustivel

            angulo_rad = math.radians(self.angulo)
            forca_x = self.FORCA_PROPULSAO_N * math.sin(angulo_rad)
            # Tkinter tem Y positivo para baixo; empuxo vertical aponta para cima.
            forca_y = (
                massa_atual * self.GRAVIDADE
                - self.FORCA_PROPULSAO_N * math.cos(angulo_rad)
            )
            self.massa = massa_atual
            self.aceleracao_x = forca_x / massa_atual
            self.aceleracao_y = forca_y / massa_atual
        else:
            self.massa = massa_anterior
            self.aceleracao_x = 0.0
            self.aceleracao_y = self.GRAVIDADE

        # Conversão de aceleração física (m/s²) para pixels/s².
        self.velocidade_x += self.aceleracao_x * self.PIXELS_POR_METRO * dT
        self.velocidade_y += self.aceleracao_y * self.PIXELS_POR_METRO * dT
        self.velocidade_x = max(-self.VELOCIDADE_MAXIMA, min(self.velocidade_x, self.VELOCIDADE_MAXIMA))
        self.velocidade_y = max(-self.VELOCIDADE_MAXIMA, min(self.velocidade_y, self.VELOCIDADE_MAXIMA))

        self.x += self.velocidade_x * dT
        self.y += self.velocidade_y * dT

        if self.x + self.largura < 0:
            self.x = largura_tela
        elif self.x > largura_tela:
            self.x = -self.largura

        # O foguete não reaparece por cima ao cruzar o limite inferior:
        # tocar a área de pouso encerra o tempo de voo.
        if local_pouso is not None and place_meeting(
            self, self.x, self.y, local_pouso
        ):
            self.x = x_anterior
            self.y = y_anterior
            self.velocidade_x = 0.0
            self.velocidade_y = 0.0
            self.colidindo = True
            self.esta_no_ar = False
            self.pontos = int(self.tempo_no_ar)
            return

        self.colidindo = False
        if self.y > altura_tela:
            self.y = altura_tela - self.altura
            self.velocidade_y = 0.0
            self.esta_no_ar = False
            self.pontos = int(self.tempo_no_ar)
