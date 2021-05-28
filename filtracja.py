from tkinter import *
from tkinter.messagebox import showinfo

from tkinter import filedialog as fd, font
from tkinter import font as tkFont
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

import math
import cv2
import numpy as np
import matplotlib.pyplot as plt

from PIL import ImageTk, Image


class Filtracja:

    def __init__(self, window, imaddr):

        """Metoda init w tym wypadku służy do budowania całego GUI"""
        self.optionVal = None
        self.center = None
        self.rozmiarm = 50
        self.window = window
        # self.drop2 = None
        self.plotframe = Frame(self.window)
        self.plotframe.pack(side="top")

        frame = LabelFrame(window, text="Przyciski kontrolne", padx=5, pady=10)

        frame.pack(padx=10, pady=10, side="bottom")
        self.runBtn = Button(frame, text="Pokaż wynik", font="Calibri 20")

        # self.filename = ""
        self.imaddr = imaddr
        # self.box = Entry(window)

        self.fileBtn = Button(frame, text="Otwórz plik", font="Calibri 20", command=self.select_file)
        self.dropLab = Label(frame, font="Calibri 20", text="Wybór maski")

        self.maskSlider = Scale(frame, from_=0, to=100, tickinterval=25, length=300, orient=HORIZONTAL, font="Calibri 16")
        maskLab = Label(frame, font="Calibri 20", text="Rozmiar maski")
        self.maskSlider.set(50)
        self.clicked = StringVar()
        self.clicked2 = StringVar()
        self.options = ("Dolnoprzepustowa Okrągła", "Górnoprzepustowa Okrągła", "Dolnoprzepustowa Kwadratowa",
                        "Górnoprzepustowa Kwadratowa", "Gaussian LP",
                        "Gaussian HP", "Butterworth LP", "Butterworth HP",
                        "Środkowo-p kwadrat LP", "Środkowo-p kwadrat HP", "Środkowo-p pierścień LP",
                        "Środkowo-p pierścień HP")
        self.drop = OptionMenu(frame, self.clicked, *self.options, command=self.switch)
        # self.drop2 = OptionMenu(window, self.clicked2, "Okrągły", "Kwadratowy")
        helv20 = tkFont.Font(family='Helvetica', size=20)
        menu = root.nametowidget(self.drop.menuname)
        menu.config(font=helv20)  # Set the dropdown menu's font

        self.drop.config(font="Calibri 20")
        self.dropLab.grid(row=0, column=2, padx=2)
        self.drop.grid(row=1, column=2, padx=2)
        maskLab.grid(row=0, column=3 )
        self.maskSlider.grid(row=1, column=3, padx=2)
        self.fileBtn.grid(row=1, column=0, padx=2)
        self.runBtn.grid(row=1, column=1, padx=2)


        self.canvas = None

        self.n = 0
        self.textfield = None
        self.img = None

    def show_values(self):
        self.rozmiarm = self.maskSlider.get()

    def switch(self, value):
        """Metoda służy do przypisywania metod z odpowiednimi maskami do odpowiadających im wyborów z OptionMenu"""
        option = self.clicked.get()
        print(value)
        if option == "Dolnoprzepustowa Okrągła":
            self.optionVal = option
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text="CHECK/REZULTAT", command=self.drawplot,
                                 font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        elif option == "Górnoprzepustowa Okrągła":
            self.optionVal = option
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text="CHECK/REZULTAT", command=self.drawplot,
                                 font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        elif option == "Dolnoprzepustowa Kwadratowa":
            self.optionVal = option
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text="CHECK/REZULTAT", command=self.drawplot,
                                 font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        elif option == "Górnoprzepustowa Kwadratowa":
            self.optionVal = option
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text="CHECK/REZULTAT", command=self.drawplot,
                                 font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        elif option == "Gaussian LP":
            self.optionVal = option
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text="CHECK/REZULTAT", command=self.drawplot,
                                 font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        elif option == "Gaussian HP":
            self.optionVal = option
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text="CHECK/REZULTAT", command=self.drawplot,
                                 font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        elif option == "Butterworth LP":
            self.optionVal = option
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text="CHECK/REZULTAT", command=self.drawplot,
                                 font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        elif option == "Butterworth HP":
            self.optionVal = option
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text="CHECK/REZULTAT", command=self.drawplot,
                                 font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        elif option == "Środkowo-p kwadrat LP":
            self.optionVal = option
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text="CHECK/REZULTAT", command=self.drawplot,
                                 font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        elif option == "Środkowo-p kwadrat HP":
            self.optionVal = option
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text="CHECK/REZULTAT", command=self.drawplot,
                                 font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        elif option == "Środkowo-p pierścień LP":
            self.optionVal = option
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text="CHECK/REZULTAT", command=self.drawplot,
                                 font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        elif option == "Środkowo-p pierścień HP":
            self.optionVal = option
            self.runBtn.grid_forget()  # usuwa istniejący przycisk
            self.runBtn.config(text="CHECK/REZULTAT", command=self.drawplot,
                                 font="Calibri 20")  # tworzy nowy przycisk
            self.runBtn.grid(row=1, column=1)  # ustawia nowy przycisk
        else:
            """Jeżeli wybrana opcja z menu nie została jeszcze zaimplementowana, usuń przycisk"""
            print("Błąd w option")
            # self.button.grid_forget()

    def show(self):
        myLabel = Label(root, text=self.clicked.get()).grid(row=3, column=1)

    def chooseMask(self, test):
        print("Hi Honey! " + test)
        if test == "Dolnoprzepustowa Okrągła":
            return self.center * self.idealFilterLP(self.rozmiarm, self.img.shape)
        elif test == "Górnoprzepustowa Okrągła":
            return self.center * self.idealFilterHP(self.rozmiarm, self.img.shape)
        elif test == "Dolnoprzepustowa Kwadratowa":
            return self.center * self.squareLP(self.rozmiarm, self.img.shape)
        elif test == "Górnoprzepustowa Kwadratowa":
            return self.center * self.squareHP(self.rozmiarm, self.img.shape)
        elif test == "Gaussian LP":
            return self.center * self.gaussianLP(self.rozmiarm, self.img.shape)
        elif test == "Gaussian HP":
            return self.center * self.gaussianHP(self.rozmiarm, self.img.shape)
        elif test == "Butterworth LP":
            return self.center * self.butterworthLP(self.rozmiarm, self.img.shape, 20)
        elif test == "Butterworth HP":
            return self.center * self.butterworthHP(self.rozmiarm, self.img.shape, 20)
        elif test == "Środkowo-p kwadrat LP":
            return self.center * self.mediumLP1(self.rozmiarm, self.img.shape, 20)
        elif test == "Środkowo-p kwadrat HP":
            return self.center * self.mediumHP1(self.rozmiarm, self.img.shape, 20)
        elif test == "Środkowo-p pierścień LP":
            return self.center * self.mediumLP2(self.rozmiarm, self.img.shape, 20)
        elif test == "Środkowo-p pierścień HP":
            return self.center * self.mediumHP2(self.rozmiarm, self.img.shape, 20)


    def drawplot(self):
        if self.canvas is not None:
            self.plotframe.destroy()
            self.plotframe = Frame(self.window)
            self.plotframe.pack(side="top")

        self.rozmiarm = self.maskSlider.get()
        fig = plt.figure(figsize=(7, 7), dpi=120)
        # fig.canvas.manager.full_screen_toggle()  # ustawia na fullscreen


        self.img = cv2.imread(self.imaddr, 0)
        plt.subplot2grid((2, 2), (0, 0)), plt.imshow(self.img, "gray"), plt.title("Oryg. obraz")
        self.tick_remover()
        # plot1 = fig.add_subplot(161)
        # plot1.imshow(img, "gray")

        original = np.fft.fft2(self.img)
        # plt.subplot(162), plt.imshow(np.log(1 + np.abs(original)), "gray"), plt.title("Spektrum")

        self.center = np.fft.fftshift(original)
        plt.subplot2grid((3, 3), (2, 0), colspan=1), plt.imshow(np.log(1 + np.abs(self.center)), "gray"), plt.title(
            "Amplituda")
        self.tick_remover()

        angle = np.angle(self.center)
        plt.subplot2grid((3, 3), (2, 1), colspan=1), plt.imshow(np.log(1 + np.abs(angle)), "gray"), plt.title("Faza")
        self.tick_remover()

        LowPassCenter = self.chooseMask(self.optionVal)
        plt.subplot2grid((3, 3), (2, 2), colspan=1), plt.imshow(np.log(1 + np.abs(LowPassCenter)), "gray"), plt.title(
            "Filtr")
        self.tick_remover()

        LowPass = np.fft.ifftshift(LowPassCenter)
        # plt.subplot(155), plt.imshow(np.log(1 + np.abs(LowPass)), "gray"), plt.title("Decentralizacja")

        inverse_LowPass = np.fft.ifft2(LowPass)
        plt.subplot2grid((2, 2), (0, 1), colspan=1), plt.imshow(np.abs(inverse_LowPass), "gray"), plt.title(
            "Obraz wynik.")
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
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                base[y, x] = 1 / (1 + (self.distance((y, x), center) / D0) ** (2 * n))
        return base

    def butterworthHP(self, D0, imgShape, n):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                base[y, x] = 1 - 1 / (1 + (self.distance((y, x), center) / D0) ** (2 * n))
        return base

    def gaussianLP(self, D0, imgShape):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for x in range(cols):
            for y in range(rows):
                base[y, x] = math.exp(((-self.distance((y, x), center) ** 2) / (2 * (D0 ** 2))))
        return base

    def gaussianHP(self, D0, imgShape):
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



root = Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))
root.title("Transformator Fouriera")

b = Filtracja(root, "kosc.bmp")

root.mainloop()

# from tkinter import ttk
# from tkinter import filedialog as fd
# from tkinter.messagebox import showinfo
#
#
# class MarButtons:
#
#     def __init__(self, master):
#
#
#         self.__nazwa = ""
#     def set_nazwa(self, value):
#         print("Co się dzieje w set: " + value)
#         self.__nazwa = value
#         print("Co się dzieje w set: " + self.__nazwa)
#
#     def get_nazwa(self):
#         return self.__nazwa
#
#     def select_file(self):
#         filetypes = (
#             ('text files', '*.txt'),
#             ('BMP files', '*.*')
#         )
#         filename = fd.askopenfilename(
#             title='Open a file',
#             initialdir='/',
#             filetypes=filetypes)
#
#         showinfo(
#             title='Selected File',
#             message=filename
#         )
#         self.set_nazwa(filename)
#         self.buttons()
#
#     def buttons(self):
#
#
#         print("HMM: " + self.get_nazwa())
#         photo = PhotoImage(file=self.get_nazwa())
#         label = Label(root, image=photo)
#         label.grid(row=1)
#
#
#
#
#
# import tk as tk
#
# root = Tk()
#                                                                                                       #CANVAS, czyste płótno
# b = MarButtons(root)
# frame1 = Frame(root)
# frame2 = Frame(root)
# frame1.grid(row=0, column=0)
# frame2.grid(row=0, column=1)
# quitButton = Button(frame1, text="Quit", command=frame2.quit)
# printButton = Button(frame1, text='Open a File', command=b.select_file)
# printButton.pack(side=LEFT)
# quitButton.pack(side=LEFT)
# root.title('Tkinter Open File Dialog')
# root.resizable(False, False)
# root.geometry('300x150')


# photo = PhotoImage(file=)


# topFrame = Frame(root)                                                                                                  #Tworzenie KONTENERU wewnątrz roota
# topFrame.pack()
# bottomFrame = Frame(root)
# bottomFrame.pack(side=BOTTOM)                                                                                           #PACK - wyświetlanie elementów
#
# button1 = Button(topFrame, text="Button 1", fg="red")                                                                   #DEFINIOWANIE elementów
# button2 = Button(topFrame, text="Button 1", fg="blue")
# button3 = Button(topFrame, text="Button 1", fg="green")
# button4 = Button(bottomFrame, text="Button 1", fg="purple")
#
# button1.pack(side=LEFT)                                                                                                 #PACK - wyświetlanie elementów
# button2.pack(side=LEFT)
# button3.pack(side=LEFT)
# button4.pack(side=BOTTOM)


# one = Label(root, text="One", bg="red", fg="white")                                                                     #Rozmieszczenie elementu na ekranie oraz jego granice
# one.pack()
# two = Label(root, text="Two", bg="green", fg="black")
# two.pack(fill=X)
# three = Label(root, text="Three", bg="blue", fg="white")
# three.pack(side=LEFT, fill=Y)

# PONIŻEJ: Wyświetlanie tekstu, textboxów i checkboxa w GRIDzie

# label_1 = Label(root, text="Name")
# label_2 = Label(root, text="Password")
# entry_1 = Entry(root)
# entry_2 = Entry(root)
# #STICKY - przylepia do kierunku świata - EAST - E
# label_1.grid(row=0, sticky=E)
# label_2.grid(row=1, sticky=E)
# entry_1.grid(row=0, column=1)
# entry_2.grid(row=1, column=1)
#
# c = Checkbutton(root, text="Keep me logged in")
# c.grid(columnspan=2)                                    #COLUMNSPAN - OZNACZA ŻE ELEMENT ZAJMUJE DWIE KOLUMNY

# SPOSÓB PIERWSZY NA POWIĄZANIE FUNKCJI Z PRZYCISKIEM
# def printName():
#     print("Chello my name is Mariusz!")
#
# button_1 = Button(root, text="Print name", command=printName)
# button_1.pack()

# SPOSÓB DRUGI NA POWIĄZANIE FUNKCJI Z PRZYCISKIEM
# def printName(event):
#     print("Chello my name is Mariusz!")
#
# button_1 = Button(root, text="Print name")
# button_1.bind("<Button-1>", printName)
# button_1.pack()


# def leftClick(event):
#     print("Left")
#
# def middleClick(event):
#     print("Middle")
#
# def rightClick(event):
#     print("Right")
#
# frame = Frame(root, width=300, height=250)
# frame.bind("<Button-1>", leftClick)
# frame.bind("<Button-2>", middleClick)
# frame.bind("<Button-3>", rightClick)
# frame.pack()

# plt.figure(figsize=(6.4*5, 4.8*5), constrained_layout=False)
#
# img_c1 = cv2.imread(r"C:\Users\mario\Documents\MATLAB\POC\Morfologia\ertka.bmp", 0)
# img_c2 = np.fft.fft2(img_c1)
# img_c3 = np.fft.fftshift(img_c2)
# img_c4 = np.fft.ifftshift(img_c3)
# img_c5 = np.fft.ifft2(img_c4)
#
# plt.subplot(151), plt.imshow(img_c1, "gray"), plt.title("Oryginalny obraz")
# plt.subplot(152), plt.imshow(np.log(1+np.abs(img_c2)), "gray"), plt.title("Spectrum")
# plt.subplot(153), plt.imshow(np.log(1+np.abs(img_c3)), "gray"), plt.title("Spektrum w centrum")
# plt.subplot(154), plt.imshow(np.log(1+np.abs(img_c4)), "gray"), plt.title("Decentralized")
# plt.subplot(155), plt.imshow(np.abs(img_c5), "gray"), plt.title("Przetworzony obraz")
#
# plt.show()


# frame1 = Frame(root)
# frame2 = Frame(root)
# frame1.grid(row=0, column=0)
# frame2.grid(row=1, column=0)
# quitButton = Button(frame1, text="Quit", command=frame2.quit)
# # printButton = Button(frame1, text='Open a File', command=select_file)
# # printButton.pack(side=LEFT)
# quitButton.pack(side=LEFT)
#
# photo = Image.open(r"C:\Users\mario\Documents\MATLAB\POC\Morfologia\ertka.bmp")
# ph = ImageTk.PhotoImage(photo)
#
# label = Label(frame2, image=ph)
# label.image=ph
# label.pack()


# Zapobieganie wyłączeniu aplikacji po wykonaniu kodu
