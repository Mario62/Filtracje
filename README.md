# Fourier transform - GUI app
*Instrukcja w języku polskim: [README](https://github.com/MarioShatterhand/fourier-transform-example/blob/master/README_PL.md)*

The program is for educational purposes. It allows you to observe the changes
taking place during the digital image processing using the Fourier transform.

Most of the main calculations come from the following source:
https://hicraigchen.medium.com/digital-image-processing-using-fourier-transform-in-python-bcb49424fd82

## Used technologies
- Python 3.9
- Tkinter
- matplotlib

## How to use
The first thing to do to run the example is to choose the type of mask 
you want to apply.

To do this, select the appropriate option from the drop-down list when 
selecting the mask. Optionally, you can also change
the size of the mask applied using the slider, as well as the width of 
this mask (Note,
mask width only applies to Gauss, Butterford and Middle mask types).

After selecting the appropriate settings, press "Show result" to view
transformations made.

It is also possible to load your own files in BMP format, for which it is used
"Load image" button. It's recommended to use grayscale images
