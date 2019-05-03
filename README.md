# GraphML To Tikz Converter

[![Issues](https://img.shields.io/github/issues/ckevuru/GraphML-To-Tikz.svg)](https://github.com/ckevuru/GraphML-To-Tikz/issues)
[![Stars](https://img.shields.io/github/stars/ckevuru/GraphML-To-Tikz.svg)](https://github.com/ckevuru/GraphML-To-Tikz/stargazers)
[![Csontributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/ckevuru/GraphML-To-Tikz/issues)
[![License](https://img.shields.io/github/license/ckevuru/GraphML-To-Tikz.svg)](https://github.com/ckevuru/GraphML-To-Tikz/issues)

The purpose of this module is to convert Yed-GraphML to Tikz format.We provide a simple gui interface to preview the Tikz image and provide productive options for both advanced and simple conversions. A .graphml file generated by Yed editor is given as an input and Tikz code is generated.

## Getting Started

The following instructions will allow any user to run our module on their local machine.

### Prerequisites

### For Windows

Python 3.7+ : Install and check the option to add PATH variable.

```
https://www.python.org/downloads/
```

PyQt5 5.12 : This library is required for gui of our module.

```
pip install PyQt5
```

MikTex : This latex distribution is required to view the preview of Tikz code generated by our module.

```
https://miktex.org/download
```

In MikTex the following packages should be installed by using the MikTex console : 

```
pdflatex
pdfcrop
```

Pdf2Image 1.5.4 : This python library is required for converting the pdf generated by MikTex into an image.

```
pip install pdf2image
```

QDarkGraystyle 1.0.2 : This python library is used to set the dark theme for our module.

```
pip install qdarkgraystyle
```

### For Ubuntu

PyQt5 5.12 :

```
pip install PyQt5
```

TexLive : This latex distribution is used for Ubuntu.

```
sudo apt-get install texlive-latex-base
```

Pdf2Image 1.5.4 : 
```
pip install pdf2image
```

QDarkGraystyle 1.0.2 :
```
pip install qdarkgraystyle
```

## Runnnig the program

### General

After installing all the dependencies one way to operate the module is cloning the repositiory and using the terminal to change directory to the 'Source' directory and running the following command on both Windows and Ubuntu.

```python
python GrapML2Tikz.py
```
Another way of execution is using an executable. Below we provide links for executables for both Windows and Ubuntu.

### Windows

Download Windows executable [here](https://github.com/ckevuru/GraphML-To-Tikz/master/Executables/).
After extracting from Windows_Gr-To-Tik.zip open GraphML-To-Tikz directory and click on GraphML-To-Tikz.exe to run a standalone executable.

```text
Windows_Gr-To-Tik -> GraphML-To-Tikz -> GraphML-To-Tikz.exe
```

### Ubuntu

Download Ubuntu executable [here](https://github.com/ckevuru/GraphML-To-Tikz/master/Executables/).

Follow the same instructions as Windows executable to run the file.

## How to use?

![alt text](https://github.com/ckevuru/GraphML-To-Tikz/raw/master/Images/gui.png)

To generate Tikz using this module :

1. Click on browse button and choose a graphml file or drag-drop a file into the box besides browse.
2. Tikz code is generated and shown in the Tikz poreview box.
3. GraphML code is shown in the right box.
4. The preview of Tikz image is shown in a new window.
5. If changes are made to the same file in yed and the file saved, hit the reload button besides the browse button and the changes will be incorporated.
6. Choose between Simple-Tikz and Adv-Tikz by clicking the respective buttons. 
7. Refresh button is used when the changes are made to the code generated in Tikz box and user wants to preview the image.
8. Save button is used to save the generated Tikz code in a .tex file.
9. Double click on any Tab to create a new tab.

## Authors

* [**Chandra Kiran Evuru**](https://github.com/ckevuru) - (CS15BTECH11012)
* [**Nisaanth Natarajan**](https://github.com/nissy321) - (CS15BTECH11027)
* [**Ram Nagesh**](https://github.com/ram-98) - (CS15BTECH11002)
* [**Akhil Naik**](https://github.com/cs15btech11014) - (CS15BTECH11014)

## License

This project is licensed under the [MIT License](LICENSE).