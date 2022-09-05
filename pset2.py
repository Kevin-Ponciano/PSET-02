#!/usr/bin/env python3

# ATENÇÃO: NENHUM IMPORT ADICIONAL É PERMITIDO!
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage


def vetor_em_matriz(vetor, largura, altura):
    """
    Recebe um vetor e o retorna uma Matriz
    com a largura (x) e altura (y) definidos

    :param vetor: list
    :param largura: int
    :param altura: int
    :return: list of list (MATRIZ)
    """
    count = 0
    matriz = []
    for i in range(altura):
        # Para cada linha percorrida é criado uma lista
        n = []
        for j in range(largura):
            # Para cada coluna percorrida adiciono 1 no contador, pecorrendo o vetor j vezes e salvando na lista n
            count += 1
            n += [vetor[count - 1]]
        # Quando os dados da coluna j é inseridos na lista n, a lista n é salva na lista matriz
        matriz += [n]
    return matriz


def matriz_em_vetor(matriz, largura, altura):
    """
    Recebe uma lista de lista (matriz) e retorna um vetor do tipo list

    :param matriz: list of list
    :param largura: int
    :param altura: int
    :return: list
    """
    vetor = []
    # É pecorrido toda matriz salvando cada posição no vetor
    for i in range(altura):
        for j in range(largura):
            vetor.append(matriz[i][j])
    return vetor


def pixel_delimitador(pixel):
    """
    Recebe um pixel e verifica se o mesmo esta entre 0 a 255 e o arredonda caso esteja "quebrado"
    :param pixel: int or float
    :return: pixel: N{0-255}
    """
    if pixel < 0:
        return 0
    elif pixel > 255:
        return 255
    else:
        return round(pixel)



class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels
        # Inicio os pixels da imagen como matriz, para facilitar a manipulação
        self.pixels = vetor_em_matriz(self.pixels, self.largura, self.altura)

    def get_pixel(self, x, y):
        # Implementação de versão estendida da imagem solicitado no item 4.2
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x >= self.largura:
            x = self.largura - 1
        if y >= self.altura:
            y = self.altura - 1
        # As dimensões largura e altura são invertidos na hora de localidar uma posição na Matriz
        # Pois no python uma lista de lista a altura (y) vem antes da largura (x)
        return self.pixels[y][x]

    def set_pixel(self, x, y, c):
        # As dimensões largura e altura são invertidos na hora de localidar uma posição na Matriz
        # Pois no python uma lista de lista a altura (y) vem antes da largura (x)
        self.pixels[y][x] = c

    def aplicar_por_pixel(self, func):
        resultado = Imagem.new(self.largura, self.altura)
        for y in range(resultado.altura):
            for x in range(resultado.largura):
                cor = self.get_pixel(x, y)
                nova_cor = func(cor)
                self.set_pixel(x, y, nova_cor)

        return self

    def invertido(self):
        return self.aplicar_por_pixel(lambda c: 256 - c)

    def borrado(self, n):
        # Não compreendi como funciona a aplicação dos Kernels e com isso não consegui implementar
        # os seguintes codigos que necessita de aplicação Kernel.
        # Consegui aplicar o kernel 3 x 3 de Identidade, mas não entendi como funciona kernels maiores.
        raise NotImplementedError

    def focado(self, n):
        raise NotImplementedError

    def bordas(self):
        raise NotImplementedError

    # Abaixo deste ponto estão utilitários para carregar, salvar,
    # mostrar e testar imagens.

    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, arquivo):
        """
        Carrega uma imagem a partir de um arquivo e retorna uma instância
        da classe representando essa imagem. Também realiza a conversão
        para escala de cinza.

        Modo de usar:
           i = Imagem.carregar('imagens_teste/gato.png')
        """
        with open(arquivo, 'rb') as img_handle:
            img = PILImage.open(img_handle)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            w, h = img.size
            return cls(w, h, pixels)

    @classmethod
    def new(cls, largura, altura):
        """
        Cria uma nova imagem em branco (tudo 0) para uma dada largura e altura.

        Modo de uso:
            i = Imagem.new(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, arquivo, modo='PNG'):
        """
        Salva uma dada imagem no disco ou para um objeto semelhante a um
        arquivo. Se "arquivo" é dado como uma string, o tipo de arquivo
        será inferido do próprio nome. Se "arquivo" for dado como um
        objeto semelhante a um arquivo, o tipo de arquivo será determinaddo
        pelo parâmetro "modo".
        """
        # transformo de novo o pixel de matriz para vetor para evitar erro durante o salvamento
        self.pixels = matriz_em_vetor(self.pixels, self.largura, self.altura)

        out = PILImage.new(mode='L', size=(self.largura, self.altura))
        out.putdata(self.pixels)
        if isinstance(arquivo, str):
            out.save(arquivo)
        else:
            out.save(arquivo, modo)
        out.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo
        a imagem como um GIF. É um utilitário para fazer a função
        mostrar ficar mais limpa.
        """
        buff = BytesIO()
        self.salvar(buff, modo='GIF')
        return base64.b64encode(buff.getvalue())

    def mostrar(self):
        """
        Mostra a imagem em uma janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se o Tk não está inicializado de forma apropriada, não faz nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evendo de redimensionamento (causando um loop infinito). Veja
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        canvas = tkinter.Canvas(toplevel, altura=self.altura,
                                largura=self.largura, highlightthickness=0)
        canvas.pack()
        canvas.img = tkinter.PhotoImage(data=self.gif_data())
        canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)

        def on_resize(event):
            # Realiza o redimensionamento da imagem quando a janela é redimensionada.
            # O procedimento é:
            #  * Converter para uma imagem PIL
            #  * Redimensionar essa imagem
            #  * Obter o GIF codificado em base64 a partir da imagem redimensionada
            #  * Colocar essa imagem em um label tkinter
            #  * Mostrar essa imagem no canvas
            new_img = PILImage.new(mode='L', size=(self.largura, self.altura))
            new_img.putdata(self.pixels)
            new_img = new_img.resize((event.largura, event.altura), PILImage.NEAREST)
            buff = BytesIO()
            new_img.save(buff, 'GIF')
            canvas.img = tkinter.PhotoImage(data=base64.b64encode(buff.getvalue()))
            canvas.configure(height=event.altura, width=event.largura)
            canvas.create_image(0, 0, image=canvas.img, anchor=tkinter.NW)

        # Finalmente, vincular essa função para que ela seja chamada
        # quando a janela for redimensionada.
        canvas.bind('<Configure>', on_resize)
        toplevel.bind('<Configure>', lambda e: canvas.configure(height=e.altura, width=e.largura))

        # when the window is closed, the program should stop
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()


    def reafter():
        tcl.after(500, reafter)


    tcl.after(500, reafter)
except:
    tk_root = None
WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco somente será rodado quando você, explicitamente,
    #  rodar seu script, e não quando os testes forem executados. Este é um
    #  bom lugar para gerar imagens, etc.

    # Imagem.carregar('imagens_teste/peixe.png').invertido().salvar('teste.png')
    # img = Imagem(3, 3, [80, 53, 99, 129, 32, 148, 175, 174, 193])
    # img.set_pixel(0, 1, 10)
    # img.salvar('teste.png')
    # print(img)

    pass

    # O código a seguir fará com que as janelas em Imagem.show
    # sejam mostradas de modo apropriado, se estivermos rodando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
