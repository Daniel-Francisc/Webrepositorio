import tkinter as tk


class HUD:
    def __init__(self, canvas):
        self.canvas = canvas

        self.dados = {
            "x": 0,
            "y": 0,
            "vx": 0,
            "vy": 0,
            "massa": 0,
            "energia": 0,
            "pontos": 0
        }

        self.texto = None

    def atualizar(self, dados):
        self.dados.update(dados)

    def desenhar(self):
        texto = (
            f"FOGUETE\n"
            f"X: {self.dados['x']:.2f}\n"
            f"Y: {self.dados['y']:.2f}\n"
            f"Vx: {self.dados['vx']:.2f}\n"
            f"Vy: {self.dados['vy']:.2f}\n"
            f"Massa: {self.dados['massa']:.2f} kg\n"
            f"Energia: {self.dados['energia']:.2f} J\n"
            f"Pontos: {self.dados['pontos']}"
        )

        if self.texto is None:
            self.texto = self.canvas.create_text(
                20,
                20,
                anchor="nw",
                text=texto,
                fill="white",
                font=("Consolas", 12)
            )
        else:
            self.canvas.itemconfig(
                self.texto,
                text=texto
            )
