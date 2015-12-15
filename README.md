##DESCRIPTION
This script is my attempt of a simple sudoku solver (CLI). In order to
work properly, a sudoku must be translated into a simple text file, where each
line represents a row and "*" represents an unkown field of the sudoku.
Thus a sudoku file should look similar to the following:

    4***7***3
    **9***6**
    *8*5*6*1*
    **17*95**
    6*******2
    **86*43**
    *9*2*3*8*
    **6***4**
    7***5***6

##INSTALLATION

    git clone https://github.com/g-murzik/sudoku-solver

##USAGE

    cd sudoku-solver
    python3 sudoku.py sample.txt

##FILES

    o sudoku.py     the program
    o sample.txt    sample sudoku
