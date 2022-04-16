# Helps to find the סמנטעל word of the day.
# Play semantle @ https://semantle.novalis.org/
# Play סמנטעל @ https://semantle-he.herokuapp.com/
# Based on a code of David Haas ~ 04/08/22
# Different scoring algorithm for Hebrew Semantle by Pavel Larionov ~ 14 Apr 2022

import pandas as pd
import gensim.models.keyedvectors as word2vec
from sklearn.preprocessing import normalize
import numpy as np


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def possible_matches(word, sim, corpus_vecs, model, margin):
    """ Finds all the vectors in a corpus that are within `sim` + or - `margin` cosine similarity of `word`
    word (str) - Input word
    sim (float) - cosine similarity of `word` and the target
    corpus_vecs (ndarray) - matrix of normalized word vectors for the corpus. shape = (n components) x (n words)
    model (keyedvectors) - gensim word2vec model
    margin (float) - accounts for uncertainty due to rounding / limited precision
    """
    vec = model.get_vector(word, norm=True)
    corpus_sims = vec.dot(corpus_vecs)  # cosine similarity of vec with all of corpus
    matches = np.where(((sim - margin) < corpus_sims) & ((sim + margin) > corpus_sims))[0]
    return set(matches)


def guess(model, corpus, corpus_vecs, test_words, test_scores, triangulation_margin, topk):

    candidates_dict = {candidate: 0 for candidate in set(range(len(corpus)))}
    for word, similarity in zip(test_words, test_scores):
        similarity = float(similarity) / 100
        print(f"Test word: {word}, score: {similarity}")
        word_matches = possible_matches(word, similarity, corpus_vecs, model, triangulation_margin)
        for word_i in word_matches:
            candidates_dict[word_i] += 1

    df = pd.DataFrame({'index': [corpus[i] for i in candidates_dict.keys()],
                       'count': candidates_dict.values()}).sort_values(by='count',
                                                                       ascending=False)
    df['is_english'] = df['index'].apply(lambda s: isEnglish(s))
    df = df[df['is_english'] == False]
    print("=============================")
    print(df.head(topk))


def main():
    model = word2vec.KeyedVectors.load('model.mdl').wv
    word_corpus = model.index_to_key.copy()
    corpus_vecs = np.load('model.mdl.wv.vectors.npy').T
    corpus_vecs = normalize(corpus_vecs, axis=0, norm='l2')

    df = pd.read_csv('words4.csv')
    test_words = df['word'].tolist()
    test_scores = pd.to_numeric(df['score']).tolist()

    # Higher triangulation_margin allows more words to match a given word and similarity score.
    guess(model, word_corpus, corpus_vecs, test_words, test_scores, triangulation_margin=0.08, topk=20)


if __name__ == "__main__":
    main()