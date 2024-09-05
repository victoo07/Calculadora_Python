import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from functools import partial
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Calculadora:
    def __init__(self):
        self.janela = ttk.Window(themename="darkly")
        self.janela.geometry('400x750')
        self.janela.title('Calculadora SENAI')

        self.cor_fundo = 'black'
        self.cor_botao = 'secondary'
        self.cor_texto = 'white'
        self.cor_operador = 'warning'
        self.fonte_padrao = ('Roboto', 18)
        self.fonte_display = ('Roboto', 36)

        icon_path = resource_path("calc.ico")
        self.janela.iconbitmap(icon_path)

        self.frame_display = ttk.Frame(self.janela)
        self.frame_display.pack(fill='both', expand=True)

        self.display = ttk.Label(
            self.frame_display,
            text='',
            font=self.fonte_display,
            anchor='e',
            padding=(20,10)
        )

        self.display.pack(fill='both', expand=True)

        self.frame_botoes = ttk.Frame(self.janela)
        self.frame_botoes.pack(fill='both', expand=True)

        self.botoes = [
            ['C', 'Del', '^', '/'],
            ['7', '8', '9', 'x'],
            ['4', '5', '6', '+'],
            ['1', '2', '3', '-'],
            ['.', '0', '()', '=']
        ]

        for i, linha in enumerate(self.botoes):
            for j, texto in enumerate(linha):
                estilo = 'warning.TButton' if texto in ['C', 'Del', '^', '/', 'x', '+', '-'] else 'secondary.TButton'
                botao = ttk.Button(
                    self.frame_botoes,
                    text=texto,
                    style=estilo,
                    width=10,
                    command=partial(self.interpretar_botao, texto)
                )
                botao.grid(row=i, column=j, padx=1, pady=1, sticky='nsew')
        for i in range(5):
            self.frame_botoes.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.frame_botoes.grid_columnconfigure(j, weight=1)

        self.frame_imagem = ttk.Frame(self.janela)
        self.frame_imagem.pack(fill='both', expand=True, pady=10)

        imagem_path = resource_path("Senai.png")
        imagem = Image.open(imagem_path)
        imagem = imagem.resize((300, 100), Image.LANCZOS)
        imagem_tk = ImageTk.PhotoImage(imagem)

        label_imagem = ttk.Label(self.frame_imagem, image=imagem_tk, text="")
        label_imagem.image = imagem_tk
        label_imagem.pack()

        self.frame_tema = ttk.Frame(self.janela)
        self.frame_tema.pack(fill='x', padx=10, pady=10)

        self.label_tema = ttk.Label(self.frame_tema, text="Escolher tema:", font=('Roboto', 12))
        self.label_tema.pack(side='top', pady=(0, 5))

        self.temas = ['darkly', 'cosmo', 'flatly', 'journal', 'liters', 'lumen', 'minty', 'pulse', 'sandstone', 'united', 'yeti', 'corculean']
        self.seletor_tema = ttk.Combobox(self.frame_tema,values=self.temas, state='readonly')
        self.seletor_tema.set('darkly')
        self.seletor_tema.pack(side='top', fill='x')
        self.seletor_tema.bind('<<ComboboxSelected>>', self.mudar_tema)
            # Victor Oliveira Rodrigues
        self.janela.mainloop()

    def mudar_tema(self, evento):
        novo_tema = self.seletor_tema.get()
        self.janela.style.theme_use(novo_tema)

    def interpretar_botao(self, valor):
        texto_atual = self.display.cget("text")

        if (valor == 'C'):
            self.display.configure(text='')
        elif (valor == 'Del'):
            self.display.configure(text=texto_atual[:-1])

        elif (valor == '='):
            self.calcular()

        elif (valor =='()'):
            if not texto_atual or texto_atual[-1] in '+-/x':
                self.display.configure(text=texto_atual + '(')
            elif texto_atual[-1] in '0123456789':
                self.display.configure(text=texto_atual + ')')
        else:
            self.display.configure(text=texto_atual + valor)

    def calcular(self):
        expressao = self.display.cget("text")
        expressao = expressao.replace('x', '*').replace('^', '**')

        try:
            resultado = eval(expressao)
            self.display.configure(text=str(resultado))
        except:
            self.display.configure(text="Erro")

if __name__ == "__main__":
    Calculadora()

            