from .Tela import Tela
from .hud import HUD
from objetos.foguete import Foguete
from objetos.localPouso import LocalPouso
from objetos.coletavel import Coletavel
from lib.Input import Input


class Gameplay(Tela):
    def __init__(self, altura=0, largura=0, titulo="Gameplay"):
        super().__init__(
            titulo=titulo,
            altura=altura,
            largura=largura
        )

        self.foguete = Foguete(
            self.IsLargura // 2,
            self.IsAltura // 2
        )

        self.local_pouso = LocalPouso(
            self.IsLargura // 2 - 75,
            self.IsAltura - 100
        )

        self.coletaveis = [
            Coletavel(200, 200),
            Coletavel(500, 300),
            Coletavel(800, 200)
        ]

        self.input = Input(self.janela)
        self.hud = HUD(self.canvas)

    def atualizar(self):
        self.foguete.atualizar(
            self.input,
            1 / 60,
            self.IsLargura,
            self.IsAltura,
            self.local_pouso
        )

        for coletavel in self.coletaveis:
            self.foguete.verificar_coleta(coletavel)

        self.hud.atualizar({
            "x": self.foguete.x,
            "y": self.foguete.y,
            "vx": self.foguete.velocidade_x,
            "vy": self.foguete.velocidade_y,
            "massa": self.foguete.massa,
            "energia": self.foguete.energia,
            "pontos": self.foguete.pontos
        })

    def desenhar(self):
        super().desenhar()

        self.canvas.create_rectangle(
            self.foguete.x,
            self.foguete.y,
            self.foguete.x + self.foguete.largura,
            self.foguete.y + self.foguete.altura,
            fill="white"
        )

        self.canvas.create_rectangle(
            self.local_pouso.x,
            self.local_pouso.y,
            self.local_pouso.x + self.local_pouso.largura,
            self.local_pouso.y + self.local_pouso.altura,
            fill="gray"
        )

        for coletavel in self.coletaveis:
            if coletavel.destruido:
                continue

            self.canvas.create_rectangle(
                coletavel.x,
                coletavel.y,
                coletavel.x + coletavel.largura,
                coletavel.y + coletavel.altura,
                fill="yellow"
            )

        self.hud.desenhar()
