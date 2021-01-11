import codecs
import json


class CorpusUtils:

    @staticmethod
    def load_json_corpus(path):
        with codecs.open(path, "r",
                         "utf-8") as fin:
            raw_data = json.load(fin)
        return raw_data

    @staticmethod
    def get_summaries_and_descriptions_from_json_data(raw_data):
        # Corpus building.
        corpus_descriptions = []
        corpus_summaries = []
        for n_file in raw_data:
            if n_file["label"] == "BUG":
                corpus_descriptions.append(n_file["description"])
                corpus_summaries.append(n_file["summary"])

        return corpus_summaries, corpus_descriptions
