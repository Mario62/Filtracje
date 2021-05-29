# Transformata Fouriera
Program służy co celów dydaktycznych. Umożliwia obserwowanie zmian zachodzących 
podczas cyfrowej transformacji obrazów przy wykorzystatniu transformaty Fouriera.

Większość głównych obliczeń pochodzi z następującego źródła:
https://hicraigchen.medium.com/digital-image-processing-using-fourier-transform-in-python-bcb49424fd82

## Technologie/biblioteki
- Python 3.9
- Tkinter
- matplotlib

## Instrukcja obsługi
![alt text](https://github.com/MarioShatterhand/fourier-transform-example/blob/master/overview1.jpg?raw=true)

Pierwszym co należy zrobić, aby uruchomić przykład, to wybranie rodzaju maski, jaka ma zostać zastosowana. 

W tym celu należy wybrać odpowiednią opcję z listy rozwijanej przy wyborze maski. Opcjonalnie można też zmienić
rozmiar zastosowanej maski przy użyciu suwaka, a także szerokość tej maski (Uwaga,
szerokość maski dotyczy wyłącznie masek rodzaju: Gauss, Butterford oraz Środkowoprzepustowej).

Po wybraniu odpowiednich ustawień należy wcisnąć "Pokaż wynik", aby wyświetlić
wykonane przekształcenia.

Możliwe jest również wczytanie własnych plików w formacie BMP, do czego służy
przycisk "Wczytaj obraz". Zaleca się używanie obrazów w skali odcieni szarości
