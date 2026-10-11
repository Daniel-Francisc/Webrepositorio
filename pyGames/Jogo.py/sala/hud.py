class HUD:
    def __init__(self, canvas):
        self.canvas = canvas
        self.dados = {
            "x": 0,
            "y": 0,
            "vx": 0,
            "vy": 0,
            "massa": 200_000,
            "combustivel": 100_000,
            "energia": 0,
            "pontos": 0,
            "tempo": 0.0,
            "voando": True
        }
        self.texto = None

    def atualizar(self, dados):
        self.dados.update(dados)

    def desenhar(self):
        estado = "EM VOO" if self.dados["voando"] else "VOO ENCERRADO"
        texto = (
            f"FOGUETE - {estado}\n"
            f"Tempo no ar: {self.dados['tempo']:.2f} s\n"
            f"Score: {int(self.dados['tempo'])} s\n"
            f"X: {self.dados['x']:.1f} px | Y: {self.dados['y']:.1f} px\n"
            f"Vx: {self.dados['vx']:.1f} px/s | Vy: {self.dados['vy']:.1f} px/s\n"
            f"Massa total: {self.dados['massa'] / 1000:.1f} t\n"
            f"Combustível: {self.dados['combustivel'] / 1000:.1f} t\n"
            f"Propulsão: barra de espaço | Inclinação: ← / →"
        )

        if self.texto is None:
            self.texto = self.canvas.create_text(
                20, 20, anchor="nw", text=texto, fill="white",
                font=("Consolas", 12)
            )
        else:
            self.canvas.itemconfig(self.texto, text=texto)
