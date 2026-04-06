# Xenakizator

This project consists in a recoding of the original Fortran IV code used to generate the ST serie of Iannis Xenakis.
The original code has been published from Xenakis himself in _Formalized Music: Thought and Mathematics in Composition_.

This first version is based on the specific algorithm of _ST/10-1, 080262_ and it’s downloadable as a macOS application. The application has a simple GUI in which you can insert the desired number of sections and the average density and it gives as output a _.pdf_ file of tables filled with sound parameters that you can use to compose a new version of the piece.
The aim of this project is to maintain alive Xenakis’ conception of music made of sound masses and to experiment with the formalised process of this idea, so you are invited to download the source code and to modify it (it’s coded in Python!).

The source code is divided in three files:
1) _Xenakizator.py_ which is the main file;
2) _ST10.py_ which is the algorithm used to generate the output;
3) _pdf_generator.py_ in which the name is self-explanatory.
   
The suggestion is to modify the _ST10.py_ file in order to experiment with the algorithm, if you want to add some input fields in the application you need to modify also the Xenakizator.py file.
You can both compile the Xenakizator.py file or create a stand-alone application, for example you can use _pyinstaller_ with the following command:
```
pyinstaller --onedir --windowed \
  --add-data "ST10.py:." \
  --add-data "pdf_generator.py:." \
  --hidden-import numpy \
  --hidden-import fpdf \
  --exclude-module matplotlib \
  --exclude-module pandas \
  --exclude-module scipy \
  --exclude-module PIL \
  Xenakizator.py
```
IMPORTANT: Note that this is an unofficial project without any profit-making purpose, completely unrelated from official associations or foundations related to Iannis Xenakis.
