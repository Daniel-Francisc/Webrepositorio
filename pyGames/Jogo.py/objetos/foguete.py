import math
import tkinter as tk

from lib.Colisao import place_meeting

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None


class Foguete:
    # Constantes físicas (SI)
    GRAVIDADE = 9.8  # m/s²
    PIXELS_POR_METRO = 50
    VELOCIDADE_VERTICAL_MAX = 600  # px/s; limite para a queda no jogo
    MASSA_SECA_KG = 100_000  # 100 toneladas
    COMBUSTIVEL_INICIAL_KG = 100_000  # 100 toneladas
    FORCA_PROPULSAO_N = 2_000_000  # 2 x 10^6 N
    FRACAO_COMBUSTIVEL_POR_FRAME = 0.001  # 0,1% do combustível inicial
    ANGULO_INCLINACAO_GRAUS = 30

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 50
        self.altura = 50
        self.largura_original = 50
        self.altura_original = 50

        self.velocidade_x = 0.0  # px/s
        self.velocidade_y = 0.0  # px/s; positivo = para baixo
        self.aceleracao_x = 0.0  # m/s²
        self.aceleracao_y = self.GRAVIDADE  # m/s²

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

        # Preserva o centro de massa enquanto muda a imagem/caixa delimitadora.
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
        if not self.esta_no_ar:
            return

        self.tempo_no_ar += dT
        x_anterior, y_anterior = self.x, self.y

        if input.pressionada("Left"):
            self.angulo = -self.ANGULO_INCLINACAO_GRAUS
        elif input.pressionada("Right"):
            self.angulo = self.ANGULO_INCLINACAO_GRAUS
        else:
            self.angulo = 0
        self._atualizar_rotacao_sprite()

        # O peso é uma FORÇA: P = m*g. Não somamos g diretamente a uma força.
        self.massa = self.massa_seca + self.combustivel
        forca_gravidade = self.massa * self.GRAVIDADE  # N, para baixo
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
            # Empuxo aponta para o nariz: vertical para cima quando angulo=0.
            forca_empuxo_x = self.FORCA_PROPULSAO_N * math.sin(angulo_rad)
            forca_empuxo_y = self.FORCA_PROPULSAO_N * math.cos(angulo_rad)
            forca_x = forca_empuxo_x
            forca_y_resultante = self.massa * self.GRAVIDADE - forca_empuxo_y

        # F = m*a. Calculamos aceleração a partir da força resultante.
        self.aceleracao_x = forca_x / self.massa
        self.aceleracao_y = forca_y_resultante / self.massa

        # Converte m/s² para px/s²; Y positivo na tela aponta para baixo.
        self.velocidade_x += self.aceleracao_x * self.PIXELS_POR_METRO * dT
        self.velocidade_y += self.aceleracao_y * self.PIXELS_POR_METRO * dT

        # Limita a velocidade nos dois eixos para impedir valores sem controle.
        self.velocidade_x = max(-self.VELOCIDADE_VERTICAL_MAX, min(
            self.velocidade_x, self.VELOCIDADE_VERTICAL_MAX
        ))
        self.velocidade_y = max(-self.VELOCIDADE_VERTICAL_MAX, min(
            self.velocidade_y, self.VELOCIDADE_VERTICAL_MAX
        ))

        self.x += self.velocidade_x * dT
        self.y += self.velocidade_y * dT

        if self.x + self.largura < 0:
            self.x = largura_tela
        elif self.x > largura_tela:
            self.x = -self.largura

        self.colidindo = False
        if local_pouso is not None and place_meeting(
            self, self.x, self.y, local_pouso
        ):
            self.x, self.y = x_anterior, y_anterior
            self.velocidade_x = self.velocidade_y = 0.0
            self.colidindo = True
            self.esta_no_ar = False
            self.pontos = int(self.tempo_no_ar)
            return

        if self.y >= altura_tela:
            self.y = altura_tela - self.altura
            self.velocidade_y = 0.0
            self.esta_no_ar = False
            self.pontos = int(self.tempo_no_ar)
