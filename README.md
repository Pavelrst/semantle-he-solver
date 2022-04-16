# semantle-he-solver
### Helper tool to solve the Hebrew version of the Semantle game. 

### Hebrew Word2Vec model
Download the model from here: https://github.com/Iddoyadlin/hebrew-w2v
Or from a direct link to a drive: https://drive.google.com/drive/folders/1RDj6Gaa5t4jtd-VtsAqyZWyk6e7o2Xux

Unzip the both files. The files we need are:
1. 'model.mdl'
2. 'model.mdl.wv.vectors.npy'
Place them at the same directory as the main_he.py file.

### What it does
It helps to find a solution in the Hebrew version of Semantle game.
As I use a slightly different Hebrew Word2Vec model, 
this tool can't find the exact solution.
It can rate all words in the corpus and show the words with the highest rating.

### How to use
1. Use the 'word.csv' file as the input of the program.
2. Enter the words in 'word' column and the scores in the 'score' column.
3. You need to enter 10-15 guesses at least.
4. Play with the triangulation_margin=0.08 argument to change the top-k list.
5. If you can't a legit word in the output, add more guesses to the words.csv file.

### Useful links
Play Semantle-eng: https://semantle.novalis.org/
Play סמנטעל @ https://semantle-he.herokuapp.com/
English version of Semantle triangulation: https://gist.github.com/davidhaas6/b36b0ce55d1993cae243145c68d30f9d
