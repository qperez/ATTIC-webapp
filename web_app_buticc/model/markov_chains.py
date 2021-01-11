import re
import nltk

nltk.download('punkt')

from nltk import trigrams, RegexpTokenizer, bigrams
from collections import defaultdict

from web_app_buticc.model.singleton import singleton

class MarkovChains:
    """
    Singleton class to create markov chains to predict next words according to before words
    """

    def __init__(self, n_grams_size, corpus):
        """ Constructor for MarkovChains.

        Inits a tokenizer to tokenize sentences in corpus, the n-gram size for the markov chains, the markov model
        (a dict with 0). It creates the markov model with the method '__create_model_from_corpus' from corpus and
        computes probabilities for each n-grams.

        :param n_grams_size: n-gram size used to predict next word
        :param corpus: Corpus used to create markov model
        """
        self.__tokenizer = RegexpTokenizer(r'\w+')
        self.__n_grams_size = n_grams_size
        self.__markov_model = defaultdict(lambda: defaultdict(lambda: 0))
        self.__create_model_from_corpus(corpus)
        self.__compute_probabilities()

    def __preprocessing_sentence(self, sentence):
        """ Preprocess sentences in the corpus.

        Keeps only alphabetic chars and tokenizes sentence.

        :param sentence: Corpus sentence to preprocess and tokenize
        :return: Tokenized word list
        """
        # remove numeric chars and lower
        sentence = re.sub(r'\d+', '', sentence).lower()
        return self.__tokenizer.tokenize(sentence)

    def __create_model_from_corpus(self, corpus):
        """ Create markov model using the corpus given in parameter

        Count the number of n-grams tuple associated to the next word.

        :param corpus: Corpus to compute the markov model
        """
        for corpus_elem in corpus:
            sentences = nltk.sent_tokenize(corpus_elem)
            for sentence in sentences:
                tokens = self.__preprocessing_sentence(sentence)

                if self.__n_grams_size == 1:
                    for word_1, word_2 in bigrams(tokens):  # , pad_right=True, pad_left=True):
                        self.__markov_model[word_1][word_2] += 1

                if self.__n_grams_size == 2:
                    for word_1, word_2, word_3 in trigrams(tokens):  # , pad_right=True, pad_left=True):
                        self.__markov_model[(word_1, word_2)][word_3] += 1

    def __compute_probabilities(self):
        """
        Computes the probabilities for each next words accroding to the word tuple before
        """
        for n_gram_tuple in self.__markov_model:
            total_count = float(sum(self.__markov_model[n_gram_tuple].values()))
            for word_next in self.__markov_model[n_gram_tuple]:
                self.__markov_model[n_gram_tuple][word_next] /= total_count
                self.__markov_model[n_gram_tuple][word_next] = round(self.__markov_model[n_gram_tuple][word_next], 4)
            self.__markov_model[n_gram_tuple] = dict(sorted(self.__markov_model[n_gram_tuple].items(),
                                                            key=lambda item: item[1], reverse=True))

    def predict(self, words_before):
        """
        Predict next words according to the before word(s) given in parameter
        :param words_before: List of word(s) before
        :return: A dict with the prediction
        """
        if len(words_before) <= 0:
            return {}
        words_before = [word.lower() for word in words_before]
        if self.__n_grams_size == 1:
            return dict(self.__markov_model[words_before[0]])
        if self.__n_grams_size >= 2:
            return dict(self.__markov_model[tuple(words_before)])
