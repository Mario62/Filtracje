from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
from tkinter import font as tkFont
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from lang.Lang_EN import Lang_EN, Lang_PL

import math
import cv2
import numpy as np
import matplotlib.pyplot as plt


class Filtracja:

    def __init__(self, window, imaddr, lang):
        """Metoda init w tym wypadku służy do budowania całego GUI"""
        if lang == "en":
            self.lang = Lang_EN()
        else:
            self.lang = Lang_PL()

        self.option = None
        self.optionVal = None
        self.center = None
        self.rozmiarm = 50
        self.maskwidth = 20
        self.window = window
        # self.drop2 = None
        self.plotframe = Frame(self.window)
        self.plotframe.pack(side="top")

        self.frame = LabelFrame(window, text=self.lang.LabelFrame, padx=5, pady=10)

        self.frame.pack(padx=10, pady=10, side="bottom")
        self.runBtn = Button(self.frame, text=self.lang.runBt, font="Calibri 20")

        # self.filename = ""
        self.imaddr = imaddr
        # self.box = Entry(window)

        self.fileBtn = Button(self.frame, text=self.lang.fileBtn, font="Calibri 20", command=self.select_file)
        exit = Button(self.frame, text=self.lang.exit, command=self.quit_me)
        self.dropLab = Label(self.frame, font="Calibri 20", text=self.lang.dropLab)

        self.maskSlider = Scale(self.frame, from_=0, to=100, tickinterval=25, length=300, orient=HORIZONTAL,
                                font="Calibri 16")
        self.maskwidthSlider = Scale(self.frame, from_=0, to=100, tickinterval=25, length=300, orient=HORIZONTAL,
                                     font="Calibri 16")
        maskLab = Label(self.frame, font="Calibri 20", text=self.lang.maskSlider)
        self.maskwidthLab = Label(self.frame, font="Calibri 20", text=self.lang.maskwidthLab)
        # langBtn = Button(self.frame, text="zmień język", command=self.change_lang)
        # langBtn.grid(row=0, column=0)
        self.maskSlider.set(50)
        self.maskwidthSlider.set(20)
        self.clicked = StringVar()
        self.clicked2 = StringVar()
        if lang == "en":
            self.options = {"Low pass Round":
                                self.roundLPcon, "High pass Round": self.roundHPcon, "Low pass square": self.squareLPcon,
                            "High pass square": self.squareHPcon, "Gauss LP": self.gaussLPcon,
                            "Gauss HP": self.gaussHPcon, "Butterworth LP": self.butterLPcon,
                            "Butterworth HP": self.butterHPcon,
                            "Middle square LP": self.middlesqLPcon, "Middle square HP": self.middlesqHPcon,
                            "Middle ring LP": self.middlerinLPcon,
                            "Middle ring HP": self.middlerinHPcon}
        else:
            self.options = {"Dolnoprzepustowa Okrągła":
                                self.roundLPcon, "Górnoprzepustowa Okrągła": self.roundHPcon,
                            "Dolnoprzepustowa Kwadratowa": self.squareLPcon,
                            "Górnoprzepustowa Kwadratowa": self.squareHPcon, "Gaussian LP": self.gaussLPcon,
                            "Gaussian HP": self.gaussHPcon, "Butterworth LP": self.butterLPcon,
                            "Butterworth HP": self.butterHPcon,
                            "Środkowo-p kwadrat LP": self.middlesqLPcon, "Środkowo-p kwadrat HP": self.middlesqHPcon,
                            "Środkowo-p pierścień LP": self.middlerinLPcon,
                            "Środkowo-p pierścień HP": self.middlerinHPcon}
        self.drop = OptionMenu(self.frame, self.clicked, *self.options, command=self.switch)
        # self.drop2 = OptionMenu(window, self.clicked2, "Okrągły", "Kwadratowy")
        helv20 = tkFont.Font(family='Helvetica', size=20)
        menu = window.nametowidget(self.drop.menuname)
        menu.config(font=helv20)  # Set the dropdown menu's font

        self.drop.config(font="Calibri 20")
        self.dropLab.grid(row=0, column=2, padx=2)
        self.drop.grid(row=1, column=2, padx=2)
        maskLab.grid(row=0, column=3)
        self.maskSlider.grid(row=1, column=3, padx=2)
        self.fileBtn.grid(row=1, column=0, padx=2)
        self.runBtn.grid(row=1, column=1, padx=2)
        self.maskwidthLab.grid(row=0, column=4)
        self.maskwidthSlider.grid(row=1, column=4, padx=2)
        exit.grid(row=1, column=5)

        self.canvas = None

        self.n = 0
        self.textfield = None
        self.img = None

    def show_values(self):
        self.rozmiarm = self.maskSlider.get()

    def roundLPcon(self):
        key_list = list(self.options.keys())
        val_list = list(self.options.values())
        position = val_list.index(self.roundLPcon)
        self.optionVal = key_list[position]
        print(self.optionVal)
        self.runBtn.grid_forget()  # usuwa istniejący przycisk
        self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                           font="Calibri 20")  # tworzy nowy przycisk
        self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk

    def roundHPcon(self):
        key_list = list(self.options.keys())
        val_list = list(self.options.values())
        position = val_list.index(self.roundHPcon)
        self.optionVal = key_list[position]
        print(self.optionVal)
        self.runBtn.grid_forget()  # usuwa istniejący przycisk
        self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                           font="Calibri 20")  # tworzy nowy przycisk
        self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk

    def squareLPcon(self):
        key_list = list(self.options.keys())
        val_list = list(self.options.values())
        position = val_list.index(self.squareLPcon)
        self.optionVal = key_list[position]
        print(self.optionVal)
        self.runBtn.grid_forget()  # usuwa istniejący przycisk
        self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                           font="Calibri 20")  # tworzy nowy przycisk
        self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk

    def squareHPcon(self):
        key_list = list(self.options.keys())
        val_list = list(self.options.values())
        position = val_list.index(self.squareHPcon)
        self.optionVal = key_list[position]
        print(self.optionVal)
        self.runBtn.grid_forget()  # usuwa istniejący przycisk
        self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                           font="Calibri 20")  # tworzy nowy przycisk
        self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk

    def gaussLPcon(self):
        key_list = list(self.options.keys())
        val_list = list(self.options.values())
        position = val_list.index(self.gaussLPcon)
        self.optionVal = key_list[position]
        print(self.optionVal)
        self.runBtn.grid_forget()  # usuwa istniejący przycisk
        self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                           font="Calibri 20")  # tworzy nowy przycisk
        self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk

    def gaussHPcon(self):
        key_list = list(self.options.keys())
        val_list = list(self.options.values())
        position = val_list.index(self.gaussHPcon)
        self.optionVal = key_list[position]
        print(self.optionVal)
        self.runBtn.grid_forget()  # usuwa istniejący przycisk
        self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                           font="Calibri 20")  # tworzy nowy przycisk
        self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk

    def butterLPcon(self):
        key_list = list(self.options.keys())
        val_list = list(self.options.values())
        position = val_list.index(self.butterLPcon)
        self.optionVal = key_list[position]
        print(self.optionVal)
        self.runBtn.grid_forget()  # usuwa istniejący przycisk
        self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                           font="Calibri 20")  # tworzy nowy przycisk
        self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk

    def butterHPcon(self):
        key_list = list(self.options.keys())
        val_list = list(self.options.values())
        position = val_list.index(self.butterHPcon)
        self.optionVal = key_list[position]
        print(self.optionVal)
        self.runBtn.grid_forget()  # usuwa istniejący przycisk
        self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                           font="Calibri 20")  # tworzy nowy przycisk
        self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk

    def middlesqLPcon(self):
        key_list = list(self.options.keys())
        val_list = list(self.options.values())
        position = val_list.index(self.middlesqLPcon)
        self.optionVal = key_list[position]
        print(self.optionVal)
        self.runBtn.grid_forget()  # usuwa istniejący przycisk
        self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                           font="Calibri 20")  # tworzy nowy przycisk
        self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk

    def middlesqHPcon(self):
        key_list = list(self.options.keys())
        val_list = list(self.options.values())
        position = val_list.index(self.middlesqHPcon)
        self.optionVal = key_list[position]
        print(self.optionVal)
        self.runBtn.grid_forget()  # usuwa istniejący przycisk
        self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                           font="Calibri 20")  # tworzy nowy przycisk
        self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk

    def middlerinLPcon(self):
        key_list = list(self.options.keys())
        val_list = list(self.options.values())
        position = val_list.index(self.middlerinLPcon)
        self.optionVal = key_list[position]
        print(self.optionVal)
        self.runBtn.grid_forget()  # usuwa istniejący przycisk
        self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                           font="Calibri 20")  # tworzy nowy przycisk
        self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk

    def middlerinHPcon(self):
        key_list = list(self.options.keys())
        val_list = list(self.options.values())
        position = val_list.index(self.middlerinHPcon)
        self.optionVal = key_list[position]
        self.runBtn.grid_forget()  # usuwa istniejący przycisk
        self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                           font="Calibri 20")  # tworzy nowy przycisk
        self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk

    def switch(self, value):
        """Metoda służy do przypisywania metod z odpowiednimi maskami do odpowiadających im wyborów z OptionMenu"""
        self.options[self.clicked.get()]()

    def chooseMask(self, test):
        if test == self.lang.test1:
            return self.center * self.idealFilterLP(self.rozmiarm, self.img.shape)
        elif test == self.lang.test2:
            return self.center * self.idealFilterHP(self.rozmiarm, self.img.shape)
        elif test == self.lang.test3:
            return self.center * self.squareLP(self.rozmiarm, self.img.shape)
        elif test == self.lang.test4:
            return self.center * self.squareHP(self.rozmiarm, self.img.shape)
        elif test == self.lang.test5:
            return self.center * self.gaussianLP(self.rozmiarm, self.img.shape)
        elif test == self.lang.test6:
            return self.center * self.gaussianHP(self.rozmiarm, self.img.shape)
        elif test == self.lang.test7:
            return self.center * self.butterworthLP(self.rozmiarm, self.img.shape, self.maskwidth)
        elif test == self.lang.test8:
            return self.center * self.butterworthHP(self.rozmiarm, self.img.shape, self.maskwidth)
        elif test == self.lang.test9:
            return self.center * self.mediumLP2(self.rozmiarm, self.img.shape, self.maskwidth)
        elif test == self.lang.test10:
            return self.center * self.mediumHP2(self.rozmiarm, self.img.shape, self.maskwidth)
        elif test == self.lang.test11:
            return self.center * self.mediumLP1(self.rozmiarm, self.img.shape, self.maskwidth)
        elif test == self.lang.test12:
            return self.center * self.mediumHP1(self.rozmiarm, self.img.shape, self.maskwidth)

    def drawplot(self):
        if self.canvas is not None:
            self.plotframe.destroy()
            self.plotframe = Frame(self.window)
            self.plotframe.pack(side="top")

        self.rozmiarm = self.maskSlider.get()
        self.maskwidth = self.maskwidthSlider.get()
        fig = plt.figure(figsize=(7, 7), dpi=120)
        # fig.canvas.manager.full_screen_toggle()  # ustawia na fullscreen

        self.img = cv2.imread(self.imaddr, 0)
        plt.subplot2grid((2, 2), (0, 0)), plt.imshow(self.img, "gray"), plt.title(self.lang.orgplot)
        self.tick_remover()
        # plot1 = fig.add_subplot(161)
        # plot1.imshow(img, "gray")

        original = np.fft.fft2(self.img)
        # plt.subplot(162), plt.imshow(np.log(1 + np.abs(original)), "gray"), plt.title("Spektrum")

        self.center = np.fft.fftshift(original)
        plt.subplot2grid((3, 3), (2, 0), colspan=1), plt.imshow(np.log(1 + np.abs(self.center)), "gray"), plt.title(
            self.lang.ampl)
        self.tick_remover()

        angle = np.angle(self.center)
        plt.subplot2grid((3, 3), (2, 1), colspan=1), plt.imshow(np.log(1 + np.abs(angle)), "gray"), plt.title(
            self.lang.angle)
        self.tick_remover()

        LowPassCenter = self.chooseMask(self.optionVal)

        plt.subplot2grid((3, 3), (2, 2), colspan=1), plt.imshow(np.log(1 + np.abs(LowPassCenter)), "gray"), plt.title(
            self.lang.filtr)
        self.tick_remover()

        LowPass = np.fft.ifftshift(LowPassCenter)
        # plt.subplot(155), plt.imshow(np.log(1 + np.abs(LowPass)), "gray"), plt.title("Decentralizacja")

        inverse_LowPass = np.fft.ifft2(LowPass)
        plt.subplot2grid((2, 2), (0, 1), colspan=1), plt.imshow(np.abs(inverse_LowPass), "gray"), plt.title(
            self.lang.result)
        self.tick_remover()

        # plt.tight_layout()

        self.canvas = FigureCanvasTkAgg(fig,
                                        master=self.plotframe)
        self.canvas.draw()

        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().pack()

    def tick_remover(self):
        plt.tick_params(left=False,
                        bottom=False,
                        labelleft=False,
                        labelbottom=False)

    def distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    def idealFilterLP(self, D0, imgShape):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                if self.distance((y, x), center) < D0:
                    base[y, x] = 1
        return base

    def idealFilterHP(self, D0, imgShape):
        base = np.ones(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                if self.distance((y, x), center) < D0:
                    base[y, x] = 0
        return base

    def butterworthLP(self, D0, imgShape, n):
        if D0 == 0:
            D0 = 1
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                base[y, x] = 1 / (1 + (self.distance((y, x), center) / D0) ** (2 * n))
        return base

    def butterworthHP(self, D0, imgShape, n):
        if D0 == 0:
            D0 = 1
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                base[y, x] = 1 - 1 / (1 + (self.distance((y, x), center) / D0) ** (2 * n))
        return base

    def gaussianLP(self, D0, imgShape):
        if D0 == 0:
            D0 = 1
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                base[y, x] = math.exp(((-self.distance((y, x), center) ** 2) / (2 * (D0 ** 2))))
        return base

    def gaussianHP(self, D0, imgShape):
        if D0 == 0:
            D0 = 1
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                base[y, x] = 1 - math.exp(((-self.distance((y, x), center) ** 2) / (2 * (D0 ** 2))))
        return base

    def mediumLP1(self, D0, imgShape, width):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                if self.distance((y, x), center) < D0 + width:
                    base[y, x] = 1
        for x in range(cols):
            for y in range(rows):
                if self.distance((y, x), center) < D0:
                    base[y, x] = 0
        return base

    def mediumHP1(self, D0, imgShape, width):
        base = np.ones(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                if self.distance((y, x), center) < D0 + width:
                    base[y, x] = 0
        for x in range(cols):
            for y in range(rows):
                if self.distance((y, x), center) < D0:
                    base[y, x] = 1
        return base

    def mediumLP2(self, D0, imgShape, width):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                if x >= center[0] - D0 - width and x <= center[0] + D0 + width and y >= center[1] - D0 - width and y <= \
                        center[1] + D0 + width:
                    base[y, x] = 1
        for x in range(cols):
            for y in range(rows):
                if x >= center[0] - D0 and x <= center[0] + D0 and y >= center[1] - D0 and y <= center[1] + D0:
                    base[y, x] = 0
        return base

    def mediumHP2(self, D0, imgShape, width):
        base = np.ones(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                if x >= center[0] - D0 - width and x <= center[0] + D0 + width and y >= center[1] - D0 - width and y <= \
                        center[1] + D0 + width:
                    base[y, x] = 0
        for x in range(cols):
            for y in range(rows):
                if x >= center[0] - D0 and x <= center[0] + D0 and y >= center[1] - D0 and y <= center[1] + D0:
                    base[y, x] = 1
        return base

    def squareLP(self, D0, imgShape):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                if x >= center[0] - D0 and x <= center[0] + D0 and y >= center[1] - D0 and y <= center[1] + D0:
                    base[y, x] = 1
        return base

    def squareHP(self, D0, imgShape):
        base = np.ones(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                if x >= center[0] - D0 and x <= center[0] + D0 and y >= center[1] - D0 and y <= center[1] + D0:
                    base[y, x] = 0
        return base

    def select_file(self):
        filetypes = (
            ('BMP files', '*.bmp'),
            ('text files', '*.txt')

        )
        self.imaddr = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        self.imaddr.encode('unicode_escape')
        print(self.imaddr)
        showinfo(
            title='Selected File',
            message=self.imaddr
        )
        # photo = Image.open(self.imaddr)
        # ph = ImageTk.PhotoImage(photo)
        #
        # label = Label(self.window, image=ph)
        # label.image = ph
        # label.grid(rowspan=2)

        self.rozmiarm = self.rozmiarm

    def quit_me(self):
        print('quit')
        self.window.quit()
        self.window.destroy()


def quit_me():
    print('quit')
    root.quit()
    root.destroy()


def change_lang(getlang):
    quit_me()
    top = Tk()

    top.attributes('-fullscreen', True)
    if getlang == "pl":
        top.title("Transformacja Fouriera")
    else:
        top.title("Fourier transform")

    b = Filtracja(top, "kosc.bmp", getlang)

    top.mainloop()


def en():
    change_lang("en")


def pl():
    change_lang("pl")


root = Tk()
root.protocol("WM_DELETE_WINDOW", quit_me)
root.title("Wybierz język/Pick language")
polish = Button(text="Język polski", command=pl)
polish.pack()
english = Button(text="English language", command=en)
english.pack()
root.mainloop()
