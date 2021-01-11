import os

import joblib

from web_app_buticc.exception.environment_not_set_exception import EnvironmentNotSetException
from web_app_buticc.model.markov_chains_manager_4_tickets import MarkovChainsManager4Tickets
from web_app_buticc.utils.corpus_utils import CorpusUtils

PYTHONPATH = os.getenv('PYTHONPATH')
PRODUCTIONMODE = os.getenv('PRODUCTIONMODE')
PATH_MODEL = "/web_app_buticc/model/ml_pickle_models/"
PATH_DATA = "/web_app_buticc/app/resources/data/"

if not PRODUCTIONMODE:
    PYTHONPATH = os.getcwd() + "/../.."

# Set global vars for the app
raw_data = CorpusUtils.load_json_corpus(PYTHONPATH + PATH_DATA + "data.json")
corpus_summaries, corpus_descriptions = CorpusUtils.get_summaries_and_descriptions_from_json_data(raw_data)

markov_chains_manager_4tickets = MarkovChainsManager4Tickets(corpus_summaries, corpus_descriptions, 2)

#Load SKlearn precomputed models
mlp = joblib.load(PYTHONPATH + PATH_MODEL + "mlp_model.pkl")
vectorizer = joblib.load(PYTHONPATH + PATH_MODEL + "vectorizer_model.pkl")
ch2 = joblib.load(PYTHONPATH + PATH_MODEL + "ch2_model.pkl")
