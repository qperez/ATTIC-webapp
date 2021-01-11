import flask
from flask import render_template, request, json

from web_app_buticc import markov_chains_manager_4tickets, vectorizer, ch2, mlp, PRODUCTIONMODE
from web_app_buticc.utils.prediction_utils import PredictionUtils

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    """Root of the application. Returns an HTML template

    :return: An html page, index.html
    """
    return render_template("public/index.html")


@app.route('/predict/next_word/summary', methods=['POST'])
def predict_next_word_summary():
    """ Uses markov chains manager to return the next words after before word(s) given. This method is used to predict
    words for ticket summary.

    :return: Next words dict for summary according to before word(s) for summary
    """
    previous_words = request.json

    if len(previous_words["previous_words"]) == 1:
        prediction = markov_chains_manager_4tickets.predict("summary_1", previous_words["previous_words"])
        print(prediction)
    else:
        prediction = markov_chains_manager_4tickets.predict("summary_2", previous_words["previous_words"])

        if len(prediction) <= 0:
            prediction = markov_chains_manager_4tickets.predict("summary_1", previous_words["previous_words"])

    payload = PredictionUtils.convert_prediction_dict_to_json(prediction)
    response = app.response_class(response=json.dumps(payload),
                                  status=200,
                                  mimetype='application/json')
    return response


@app.route('/predict/next_word/description', methods=['POST'])
def predict_next_word_description():
    """ Uses markov chains manager to return the next words after before word(s) given. This method is used to predict
    words for ticket.

    :return: Next words dict for summary according to before word(s) for description.
    """
    previous_words = request.json
    if len(previous_words["previous_words"]) == 1:
        prediction = markov_chains_manager_4tickets.predict("description_1", previous_words["previous_words"])
    else:
        prediction = markov_chains_manager_4tickets.predict("description_2", previous_words["previous_words"])
        if len(prediction) <= 0:
            prediction = markov_chains_manager_4tickets.predict("description_1", previous_words["previous_words"])

    payload = PredictionUtils.convert_prediction_dict_to_json(prediction)
    response = app.response_class(response=json.dumps(payload),
                                  status=200,
                                  mimetype='application/json')
    return response


@app.route('/predict/ticket', methods=['POST'])
def predict_ticket():
    """API to predict if a ticket is a buggy ticket according to the description and summary given in parameters.
    Gives in parameters a json object containing a description and a summary of a buggy ticket:
    Example of payload in POST:
    {
        {"description" : "description for the buggy ticket"},
        {"summary" : "summary for the buggy ticket"}
    }

    Example of payload in response:
    {
        {"ticketIsBug": false,
        "summary": "summary for the buggy ticket",
        "description": "description for the buggy ticket",
        "probabilities": 0.25}
    }

    :return: A json object with a boolean field 'ticketIsBug', true if the ticket is a buggy ticket. Returns also
    a buggy probability for the ticket.
    """
    ticket = request.json
    description = ticket["description"]
    summary = ticket["summary"]

    for i in range(0, 3):
        summary += " " + summary

    doc = [summary + " " + description]
    X = vectorizer.transform(doc)
    X = ch2.transform(X)
    y = mlp.predict(X)
    proba = mlp.predict_proba(X)
    proba = [round(x, 3) for x in proba[0]]
    print(proba)
    is_bug = bool(y)

    payload = {"ticketIsBug": is_bug,
               "summary": summary,
               "description": description,
               "probability": proba}
    response = app.response_class(response=json.dumps(payload),
                                  status=200,
                                  mimetype='application/json')
    return response


# @app.route('/predict/developer', methods=['POST'])
# def predict_developer():
#     content = request.json
#     print(content)
#
#     dev_class = predictor.predict(content, name=content["className"])
#     payload = {"name": content["className"], "class": int(dev_class)}
#     print(payload)
#     response = app.response_class(response=json.dumps(payload),
#                                   status=200,
#                                   mimetype='application/json')
#     return response


if __name__ == '__main__':
    if PRODUCTIONMODE:
        app.run(debug=False, host='0.0.0.0', port=80)
    else:
        app.run(debug=True, host='localhost', port=5000)
