from .Tela import Tela
from .hud import HUD
from objetos.foguete import Foguete


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

        self.teclas = set()

        self.hud = HUD(self.canvas)

        self.janela.bind("<KeyPress>", self.tecla_pressionada)
        self.janela.bind("<KeyRelease>", self.tecla_liberada)

    def tecla_pressionada(self, evento):
        self.teclas.add(evento.keysym)

    def tecla_liberada(self, evento):
        self.teclas.discard(evento.keysym)

    def atualizar(self):
        if "Left" in self.teclas:
            self.foguete.x -= self.foguete.velocidade_x

        if "Right" in self.teclas:
            self.foguete.x += self.foguete.velocidade_x

        if "Up" in self.teclas:
            self.foguete.y -= self.foguete.velocidade_y

        if "Down" in self.teclas:
            self.foguete.y += self.foguete.velocidade_y

        self.foguete.atualizar(
            self.IsLargura,
            self.IsAltura
        )

        self.hud.atualizar({
            "x": self.foguete.x,
            "y": self.foguete.y,
            "vx": self.foguete.velocidade_x,
            "vy": self.foguete.velocidade_y,
            "massa": self.foguete.massa,
            "energia": self.foguete.energia
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

        self.hud.desenhar()