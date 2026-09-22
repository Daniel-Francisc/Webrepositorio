import tkinter as tk

class Tela:
    def __init__(
        self,
        debug = True, 
        titulo = "pygames",
        altura = 0,
        largura = 0
    ):
        self.debug = debug
        self.janela = tk.Tk()
        self.janela.title(titulo)
        
        self.largura = largura
        self.altura = altura
        self.IsLargura = self.__Largura()
        self.IsAltura = self.__Altura()
        
        self.janela.geometry(f"{self.IsLargura}x{self.IsAltura}")
        
        self.canvas = tk.Canvas( 
            self.janela, 
            width=self.IsLargura,
            height=self.IsAltura, 
            bg="black", 
            highlightthickness=0 
        )
        self.canvas.pack()
        
    def __Largura(self):
        if self.largura == 0: 
            return self.janela.winfo_screenwidth()
        else: return self.largura
    def __Altura(self):
        if self.altura == 0: 
            return self.janela.winfo_screenheight()
        else: return self.altura
        
    def atualizar(self): pass
    def desenhar(self): self.canvas.delete("all")
    
    def executar(self): 
        self.atualizar()
        self.desenhar()
        
        self.janela.after(16, self.executar) 
        self.janela.mainloop()