from tkinter import *
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
from tkinter import font as tkFont
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from lang.Lang import Lang_EN, Lang_PL

import math
import cv2
import numpy as np
import matplotlib.pyplot as plt


class Filtracja:

    def __init__(self, window, imaddr, lang):
        try:
            """Metoda init w tym wypadku służy do budowania całego GUI"""
            if lang == "en":
                self.lang = Lang_EN()
            else:
                self.lang = Lang_PL()

            # Inicjalizacja zmiennych
            self.option = None
            self.optionVal = None
            self.center = None
            self.rozmiarm = 50
            self.maskwidth = 20
            self.window = window
            self.canvas = None
            self.n = 0
            self.textfield = None
            self.img = None

            # Ustawienie Frameów (coś w rodzaju div z HTML, wydzielony obszar)
            self.plotframe = Frame(self.window)
            self.plotframe.pack(side="top")
            self.frame = Frame(window, padx=5, pady=10)
            self.frame.pack(padx=10, pady=10, side="bottom")

            self.imaddr = imaddr

            # Tworzenie i rozmieszczanie przycisków
            self.runBtn = Button(
                self.frame, text=self.lang.runBt, font="Calibri 20")
            self.fileBtn = Button(self.frame, text=self.lang.fileBtn,
                                  font="Calibri 20", command=self.select_file)
            exit = Button(self.frame, text=self.lang.exit,
                          font="Calibri 20", command=self.quit_me)
            self.dropLab = Label(self.frame, font="Calibri 20",
                                 text=self.lang.dropLab)
            self.maskSlider = Scale(self.frame, from_=0, to=100, tickinterval=25, length=300, orient=HORIZONTAL,
                                    font="Calibri 16")
            self.maskwidthSlider = Scale(self.frame, from_=0, to=100, tickinterval=25, length=300, orient=HORIZONTAL,
                                         font="Calibri 16")
            maskLab = Label(self.frame, font="Calibri 20",
                            text=self.lang.maskSlider)
            self.maskwidthLab = Label(
                self.frame, font="Calibri 20", text=self.lang.maskwidthLab)

            # Ustawianie wartości domyślnych dla niektórych przycisków
            self.maskSlider.set(50)
            self.maskwidthSlider.set(20)
            self.clicked = StringVar()
            self.clicked2 = StringVar()

            if lang == "en":
                self.options = {"Lowpass Round":
                                self.roundLPcon, "Highpass Round": self.roundHPcon, "Lowpass square": self.squareLPcon,
                                "Highpass square": self.squareHPcon, "Gauss LP": self.gaussLPcon,
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

            self.drop = OptionMenu(self.frame, self.clicked,
                                   *self.options, command=self.switch)
            # self.drop2 = OptionMenu(window, self.clicked2, "Okrągły", "Kwadratowy")
            helv20 = tkFont.Font(family='Helvetica', size=20)
            menu = window.nametowidget(self.drop.menuname)
            menu.config(font=helv20)

            # Ustawianie rozmieszczenia elementów wewnątrz Frame'a
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
        except Exception as e:
            print(e)

    def show_values(self):
        try:
            self.rozmiarm = self.maskSlider.get()
        except Exception as e:
            print(e)

    def roundLPcon(self):
        try:
            # Tworzę listę z kluczy w słowniku
            key_list = list(self.options.keys())
            # Tworzę listę z wartości w słowniku
            val_list = list(self.options.values())
            # Znajduję indeks pod jakim znajduje się wartość (nazwa metody)
            position = val_list.index(self.roundLPcon)
            # Ustawiana jest wartość (nazwa tej metody)
            self.optionVal = key_list[position]
            print(self.optionVal)
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                               font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        except Exception as e:
            print(e)

    def roundHPcon(self):
        try:
            key_list = list(self.options.keys())
            val_list = list(self.options.values())
            position = val_list.index(self.roundHPcon)
            self.optionVal = key_list[position]
            print(self.optionVal)
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                               font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        except Exception as e:
            print(e)

    def squareLPcon(self):
        try:
            key_list = list(self.options.keys())
            val_list = list(self.options.values())
            position = val_list.index(self.squareLPcon)
            self.optionVal = key_list[position]
            print(self.optionVal)
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                               font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        except Exception as e:
            print(e)

    def squareHPcon(self):
        try:
            key_list = list(self.options.keys())
            val_list = list(self.options.values())
            position = val_list.index(self.squareHPcon)
            self.optionVal = key_list[position]
            print(self.optionVal)
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                               font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        except Exception as e:
            print(e)

    def gaussLPcon(self):
        try:
            key_list = list(self.options.keys())
            val_list = list(self.options.values())
            position = val_list.index(self.gaussLPcon)
            self.optionVal = key_list[position]
            print(self.optionVal)
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                               font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        except Exception as e:
            print(e)

    def gaussHPcon(self):
        try:
            key_list = list(self.options.keys())
            val_list = list(self.options.values())
            position = val_list.index(self.gaussHPcon)
            self.optionVal = key_list[position]
            print(self.optionVal)
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                               font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        except Exception as e:
            print(e)

    def butterLPcon(self):
        try:
            key_list = list(self.options.keys())
            val_list = list(self.options.values())
            position = val_list.index(self.butterLPcon)
            self.optionVal = key_list[position]
            print(self.optionVal)
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                               font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        except Exception as e:
            print(e)

    def butterHPcon(self):
        try:
            key_list = list(self.options.keys())
            val_list = list(self.options.values())
            position = val_list.index(self.butterHPcon)
            self.optionVal = key_list[position]
            print(self.optionVal)
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                               font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        except Exception as e:
            print(e)

    def middlesqLPcon(self):
        try:
            key_list = list(self.options.keys())
            val_list = list(self.options.values())
            position = val_list.index(self.middlesqLPcon)
            self.optionVal = key_list[position]
            print(self.optionVal)
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                               font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        except Exception as e:
            print(e)

    def middlesqHPcon(self):
        try:
            key_list = list(self.options.keys())
            val_list = list(self.options.values())
            position = val_list.index(self.middlesqHPcon)
            self.optionVal = key_list[position]
            print(self.optionVal)
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                               font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        except Exception as e:
            print(e)

    def middlerinLPcon(self):
        try:
            key_list = list(self.options.keys())
            val_list = list(self.options.values())
            position = val_list.index(self.middlerinLPcon)
            self.optionVal = key_list[position]
            print(self.optionVal)
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                               font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        except Exception as e:
            print(e)

    def middlerinHPcon(self):
        try:
            key_list = list(self.options.keys())
            val_list = list(self.options.values())
            position = val_list.index(self.middlerinHPcon)
            self.optionVal = key_list[position]
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text=self.lang.runBt, command=self.drawplot,
                               font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        except Exception as e:
            print(e)

    def switch(self, value):
        try:
            """Metoda służy do przypisywania metod z odpowiednimi maskami do odpowiadających im wyborów z OptionMenu"""
            self.options[self.clicked.get()]()
        except Exception as e:
            print(e)

    def chooseMask(self, test):
        try:
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
        except Exception as e:
            print(e)

    def drawplot(self):
        try:
            if self.canvas is not None:
                self.plotframe.destroy()
                self.plotframe = Frame(self.window)
                self.plotframe.pack(side="top")

            self.rozmiarm = self.maskSlider.get()
            self.maskwidth = self.maskwidthSlider.get()
            fig = plt.figure(figsize=(7, 7), dpi=120)
            # fig.canvas.manager.full_screen_toggle()  # ustawia na fullscreen

            self.img = cv2.imread(self.imaddr, 0)
            plt.subplot2grid((2, 2), (0, 0)), plt.imshow(
                self.img, "gray"), plt.title(self.lang.orgplot)
            self.tick_remover()  # Usuwa elementy takie jak skala z plotów
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

            # Ustawianie widoku plotów wewnątrz Frame'a
            self.canvas.get_tk_widget().pack()

            plt.close()
        except Exception as e:
            print(e)

    def tick_remover(self):
        try:
            plt.tick_params(left=False,
                            bottom=False,
                            labelleft=False,
                            labelbottom=False)
        except Exception as e:
            print(e)

    def distance(self, point1, point2):
        try:
            return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
        except Exception as e:
            print(e)

    def idealFilterLP(self, D0, imgShape):
        try:
            base = np.zeros(imgShape[:2])
            rows, cols = imgShape[:2]
            center = (rows / 2, cols / 2)
            for x in range(cols):
                for y in range(rows):
                    if self.distance((y, x), center) < D0:
                        base[y, x] = 1
            return base
        except Exception as e:
            print(e)

    def idealFilterHP(self, D0, imgShape):
        try:
            base = np.ones(imgShape[:2])
            rows, cols = imgShape[:2]
            center = (rows / 2, cols / 2)
            for x in range(cols):
                for y in range(rows):
                    if self.distance((y, x), center) < D0:
                        base[y, x] = 0
            return base
        except Exception as e:
            print(e)

    def butterworthLP(self, D0, imgShape, n):
        try:
            if D0 == 0:
                D0 = 1
            base = np.zeros(imgShape[:2])
            rows, cols = imgShape[:2]
            center = (rows / 2, cols / 2)
            for x in range(cols):
                for y in range(rows):
                    base[y, x] = 1 / \
                        (1 + (self.distance((y, x), center) / D0) ** (2 * n))
            return base
        except Exception as e:
            print(e)

    def butterworthHP(self, D0, imgShape, n):
        try:
            if D0 == 0:
                D0 = 1
            base = np.zeros(imgShape[:2])
            rows, cols = imgShape[:2]
            center = (rows / 2, cols / 2)
            for x in range(cols):
                for y in range(rows):
                    base[y, x] = 1 - 1 / \
                        (1 + (self.distance((y, x), center) / D0) ** (2 * n))
            return base
        except Exception as e:
            print(e)

    def gaussianLP(self, D0, imgShape):
        try:
            if D0 == 0:
                D0 = 1
            base = np.zeros(imgShape[:2])
            rows, cols = imgShape[:2]
            center = (rows / 2, cols / 2)
            for x in range(cols):
                for y in range(rows):
                    base[y, x] = math.exp(
                        ((-self.distance((y, x), center) ** 2) / (2 * (D0 ** 2))))
            return base
        except Exception as e:
            print(e)

    def gaussianHP(self, D0, imgShape):
        try:
            if D0 == 0:
                D0 = 1
            base = np.zeros(imgShape[:2])
            rows, cols = imgShape[:2]
            center = (rows / 2, cols / 2)
            for x in range(cols):
                for y in range(rows):
                    base[y, x] = 1 - \
                        math.exp(
                            ((-self.distance((y, x), center) ** 2) / (2 * (D0 ** 2))))
            return base
        except Exception as e:
            print(e)

    def mediumLP1(self, D0, imgShape, width):
        try:
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
        except Exception as e:
            print(e)

    def mediumHP1(self, D0, imgShape, width):
        try:
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
        except Exception as e:
            print(e)

    def mediumLP2(self, D0, imgShape, width):
        try:
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
        except Exception as e:
            print(e)

    def mediumHP2(self, D0, imgShape, width):
        try:
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
        except Exception as e:
            print(e)

    def squareLP(self, D0, imgShape):
        try:
            base = np.zeros(imgShape[:2])
            rows, cols = imgShape[:2]
            center = (rows / 2, cols / 2)
            for x in range(cols):
                for y in range(rows):
                    if x >= center[0] - D0 and x <= center[0] + D0 and y >= center[1] - D0 and y <= center[1] + D0:
                        base[y, x] = 1
            return base
        except Exception as e:
            print(e)

    def squareHP(self, D0, imgShape):
        try:
            base = np.ones(imgShape[:2])
            rows, cols = imgShape[:2]
            center = (rows / 2, cols / 2)
            for x in range(cols):
                for y in range(rows):
                    if x >= center[0] - D0 and x <= center[0] + D0 and y >= center[1] - D0 and y <= center[1] + D0:
                        base[y, x] = 0
            return base
        except Exception as e:
            print(e)

    def select_file(self):
        try:
            filetypes = (
                ('BMP files', '*.bmp'),
                ('All files', '*.*')

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
        except Exception as e:
            print(e)

    def quit_me(self):
        try:
            print('quit')
            self.window.quit()
            self.window.destroy()
        except Exception as e:
            print(e)


def quit_me():
    try:
        print('quit')
        root.quit()
        root.destroy()
    except Exception as e:
        print(e)


def change_lang(getlang):
    try:
        quit_me()
        top = Tk()
        top.geometry("1800x1000")

        # Zapewnia fullscreen całej aplikacji
        # top.attributes('-fullscreen', True)
        if getlang == "pl":
            top.title("Transformacja Fouriera")
        else:
            top.title("Fourier transform")

        Filtracja(top, "kosc.bmp", getlang)

        top.mainloop()
    except Exception as e:
        print(e)


def en():
    try:
        change_lang("en")
    except Exception as e:
        print(e)


def pl():
    try:
        change_lang("pl")
    except Exception as e:
        print(e)


try:
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", quit_me)
    root.title("Wybierz język/Pick language")
    polish = Button(text="Język polski", command=pl)
    polish.pack()
    english = Button(text="English language", command=en)
    english.pack()
    root.mainloop()
except Exception as e:
    print(e)
