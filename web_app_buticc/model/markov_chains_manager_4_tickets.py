from web_app_buticc.model.markov_chains import MarkovChains


class MarkovChainsManager4Tickets:
    """
    Manager to have a simple interface for markov chains. Allowing easily to predict newt word for summary
    or description for tickets.
    """
    def __init__(self, corpus_summaries, corpus_descriptions, n_grams_max):
        """
        Constructor to create a manager (a dict) for markov chains
        :param corpus_summaries: Corpus of summary for Markov Model to predict next word for summary
        :param corpus_descriptions: Corpus of description for Markov Model to predict next word for description
        :param n_grams_max: Max size of n-grams to used
        """
        self.__markov_chains_dict = {}
        for i in range(1, n_grams_max + 1):
            self.__markov_chains_dict.update({"summary_" + str(i): MarkovChains(i, corpus_summaries)})
            self.__markov_chains_dict.update({"description_" + str(i): MarkovChains(i, corpus_descriptions)})

    def predict(self, field, words_before):
        """
        Predict next word according to field (summary or description) and before word(s).
        :param field: String for the field to used
        :param words_before: Word(s) before next word to predict
        :return: A dict with the prediction
        """
        return self.__markov_chains_dict[field].predict(words_before)
