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
    VELOCIDADE_VERTICAL_MAX = 600
    VELOCIDADE_CONTROLE = 200  # px/s, comportamento preservado da main
    MASSA_SECA_KG = 100_000
    COMBUSTIVEL_INICIAL_KG = 100_000
    FORCA_PROPULSAO_N = 2_000_000
    FRACAO_COMBUSTIVEL_POR_FRAME = 0.001
    ANGULO_INCLINACAO_GRAUS = 30

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 50
        self.altura = 50
        self.largura_original = 50
        self.altura_original = 50

        self.velocidade_x = 0.0
        self.velocidade_y = 0.0
        self.aceleracao_x = 0.0
        self.aceleracao_y = self.GRAVIDADE

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
        self._janela = None

    def carregar_sprite(self, janela, caminho):
        self._janela = janela
        self.sprite = tk.PhotoImage(master=janela, file=caminho)
        self.largura_original = self.sprite.width()
        self.altura_original = self.sprite.height()
        self.largura = self.largura_original
        self.altura = self.altura_original

        if Image is not None and ImageTk is not None:
            self._sprite_original = Image.open(caminho).convert("RGBA")
            self._sprite_rotacionado = ImageTk.PhotoImage(
                self._sprite_original, master=janela
            )

    def _atualizar_rotacao_sprite(self):
        if self._sprite_original is None or ImageTk is None:
            self.largura = self.largura_original
            self.altura = self.altura_original
            return

        centro_x = self.x + self.largura / 2
        centro_y = self.y + self.altura / 2
        imagem = self._sprite_original.rotate(
            self.angulo,
            resample=Image.Resampling.BICUBIC,
            expand=True
        )
        self._sprite_rotacionado = ImageTk.PhotoImage(
            imagem, master=self._janela
        )
        self.largura = imagem.width
        self.altura = imagem.height
        self.x = centro_x - self.largura / 2
        self.y = centro_y - self.altura / 2

    def verificar_coleta(self, coletavel):
        if coletavel.destruido:
            return
        if place_meeting(self, self.x, self.y, coletavel):
            self.pontos += coletavel.valor
            coletavel.destruido = True

    def atualizar(self, input, dT, largura_tela, altura_tela, local_pouso=None):
        # A colisão com a plataforma bloqueia apenas o movimento contra ela.
        # Não desativamos a atualização: o jogador continua podendo se afastar.
        self.tempo_no_ar += dT
        x_anterior, y_anterior = self.x, self.y

        # Mantém o controle direto das setas que funcionava na main.
        # Esquerda/direita também inclinam o nariz para orientar o empuxo.
        if input.pressionada("Left"):
            self.x -= self.VELOCIDADE_CONTROLE * dT
            self.angulo = -self.ANGULO_INCLINACAO_GRAUS
        elif input.pressionada("Right"):
            self.x += self.VELOCIDADE_CONTROLE * dT
            self.angulo = self.ANGULO_INCLINACAO_GRAUS
        else:
            self.angulo = 0

        if input.pressionada("Up"):
            self.y -= self.VELOCIDADE_CONTROLE * dT
        if input.pressionada("Down"):
            self.y += self.VELOCIDADE_CONTROLE * dT

        self._atualizar_rotacao_sprite()

        # Calcula a gravidade como força (peso = massa * g).
        self.massa = self.massa_seca + self.combustivel
        forca_gravidade = self.massa * self.GRAVIDADE
        forca_x = 0.0
        forca_y_resultante = forca_gravidade

        if input.pressionada("space") and self.combustivel > 0:
            consumo = min(
                self.combustivel,
                self.combustivel_inicial * self.FRACAO_COMBUSTIVEL_POR_FRAME
            )
            self.combustivel = max(0.0, self.combustivel - consumo)
            self.massa = self.massa_seca + self.combustivel

            angulo_rad = math.radians(self.angulo)
            forca_x = self.FORCA_PROPULSAO_N * math.sin(angulo_rad)
            forca_empuxo_y = self.FORCA_PROPULSAO_N * math.cos(angulo_rad)
            forca_y_resultante = self.massa * self.GRAVIDADE - forca_empuxo_y

        self.aceleracao_x = forca_x / self.massa
        self.aceleracao_y = forca_y_resultante / self.massa

        self.velocidade_x += self.aceleracao_x * self.PIXELS_POR_METRO * dT
        self.velocidade_y += self.aceleracao_y * self.PIXELS_POR_METRO * dT

        limite = self.VELOCIDADE_VERTICAL_MAX
        self.velocidade_x = max(-limite, min(self.velocidade_x, limite))
        self.velocidade_y = max(-limite, min(self.velocidade_y, limite))

        self.x += self.velocidade_x * dT
        self.y += self.velocidade_y * dT

        # Mantém o wrap horizontal existente na main.
        if self.x + self.largura < 0:
            self.x = largura_tela
        elif self.x > largura_tela:
            self.x = -self.largura

        self.colidindo = False
        if local_pouso is not None and place_meeting(
            self, self.x, self.y, local_pouso
        ):
            # Resolve cada eixo separadamente. Se houver sobreposição, tenta
            # manter o movimento horizontal e bloquear só o vertical; se a
            # colisão veio do movimento horizontal, bloqueia só esse eixo.
            x_atual, y_atual = self.x, self.y

            self.x = x_atual
            self.y = y_anterior
            colisao_vertical = place_meeting(
                self, self.x, self.y, local_pouso
            )

            self.x = x_anterior
            self.y = y_atual
            colisao_horizontal = place_meeting(
                self, self.x, self.y, local_pouso
            )

            if colisao_vertical:
                self.y = y_anterior
                self.velocidade_y = 0.0
            elif colisao_horizontal:
                self.x = x_anterior
                self.velocidade_x = 0.0
            else:
                # Caso diagonal/ambíguo: bloqueia apenas o eixo de maior
                # deslocamento neste frame, em vez de zerar a posição toda.
                deslocamento_x = abs(x_atual - x_anterior)
                deslocamento_y = abs(y_atual - y_anterior)
                if deslocamento_x >= deslocamento_y:
                    self.x = x_anterior
                    self.velocidade_x = 0.0
                    self.y = y_atual
                else:
                    self.y = y_anterior
                    self.velocidade_y = 0.0

            self.colidindo = True

        if self.y + self.altura >= altura_tela:
            self.y = altura_tela - self.altura
            self.velocidade_y = 0.0
            self.esta_no_ar = False
            self.pontos = int(self.tempo_no_ar)
