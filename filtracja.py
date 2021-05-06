from tkinter import *
from tkinter.messagebox import showinfo

from tkinter import filedialog as fd
import math
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageTk, Image


class Filtracja:

    def __init__(self, window, imaddr):
        self.button = Button(window, text="check")
        self.window = window
        # self.filename = ""
        self.imaddr = imaddr
        # self.box = Entry(window)

        self.button2 = Button(window, text="Open file", command=self.select_file)
        self.dropLab = Label(root, text="Wybór maski")
        self.drop2Lab = Label(root, text="Wybór kształtu")

        self.clicked = StringVar()
        self.clicked2 = StringVar()
        self.options = ("Dolnoprzepustowa", "Górnoprzepustowa", "Gaussian LP",
                        "Gaussian HP",
                        "Butterworth LP", "Butterworth HP")
        self.drop = OptionMenu(window, self.clicked, *self.options, command=lambda e: self.switch())
        self.drop2 = OptionMenu(window, self.clicked2, "Okrągły", "Kwadratowy")
        self.dropLab.grid(row=1, column=0)
        self.drop.grid(row=1, column=1)
        self.drop2Lab.grid(row=2, column=0)
        self.drop2.grid(row=2, column=1)
        # self.box.pack()
        self.button2.grid(row=0, column=0)
        self.button.grid(row=0, column=1)
        # self.button3 = Button(root, text="Show selection", command=self.show).grid(row=3, column=0)

    def switch(self):
        """Metoda służy do przypisywania metod z odpowiednimi maskami do odpowiadających im wyborów z OptionMenu"""
        option = self.clicked.get()

        if option == "Dolnoprzepustowa":
            print("HMM")
            self.button.grid_forget()
            self.button = Button(root, text="check", command=self.plotLP)
            self.button.grid(row=0, column=1)
        else:
            self.button.grid_forget()



    def show(self):
        myLabel = Label(root, text=self.clicked.get()).grid(row=3, column=1)

    def plotLP(self):
        plt.figure(figsize=(6.4 * 5, 4.8 * 5), constrained_layout=False)

        img = cv2.imread(self.imaddr, 0)
        plt.subplot(161), plt.imshow(img, "gray"), plt.title("Oryginalny obraz")

        original = np.fft.fft2(img)
        plt.subplot(162), plt.imshow(np.log(1 + np.abs(original)), "gray"), plt.title("Spektrum")

        center = np.fft.fftshift(original)
        plt.subplot(163), plt.imshow(np.log(1 + np.abs(center)), "gray"), plt.title("Spektrum w centrum")

        LowPassCenter = center * self.idealFilterLP(50, img.shape)
        plt.subplot(164), plt.imshow(np.log(1 + np.abs(LowPassCenter)), "gray"), plt.title(
            "Centrum * filtr dolnoprzepustowy")

        LowPass = np.fft.ifftshift(LowPassCenter)
        plt.subplot(165), plt.imshow(np.log(1 + np.abs(LowPass)), "gray"), plt.title("Decentralizacja")

        inverse_LowPass = np.fft.ifft2(LowPass)
        plt.subplot(166), plt.imshow(np.abs(inverse_LowPass), "gray"), plt.title("Processed Image")

        plt.show()

    # def plotHP(self):

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
        photo = Image.open(self.imaddr)
        ph = ImageTk.PhotoImage(photo)

        label = Label(self.window, image=ph)
        label.image = ph
        label.grid(rowspan=2)


root = Tk()

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
# plt.subplot(151), plt.imshow(img_c1, "gray"), plt.title("Original Image")
# plt.subplot(152), plt.imshow(np.log(1+np.abs(img_c2)), "gray"), plt.title("Spectrum")
# plt.subplot(153), plt.imshow(np.log(1+np.abs(img_c3)), "gray"), plt.title("Centered Spectrum")
# plt.subplot(154), plt.imshow(np.log(1+np.abs(img_c4)), "gray"), plt.title("Decentralized")
# plt.subplot(155), plt.imshow(np.abs(img_c5), "gray"), plt.title("Processed Image")
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
