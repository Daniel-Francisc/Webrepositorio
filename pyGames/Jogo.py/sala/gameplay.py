from Tela import Tela
from hud import HUD
from foguete import Foguete

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
            self.x -= self.velocidade_x

        if "Right" in self.teclas:
            self.x += self.velocidade_x

        if "Up" in self.teclas:
            self.y -= self.velocidade_y

        if "Down" in self.teclas:
            self.y += self.velocidade_y

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
            self.x - 25,
            self.y - 25,
            self.x + 25,
            self.y + 25,
            fill="white"
        )

        self.hud.desenhar()