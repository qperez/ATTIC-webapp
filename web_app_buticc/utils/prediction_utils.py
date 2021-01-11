class PredictionUtils:

    @staticmethod
    def convert_prediction_dict_to_json(prediction_dict):
        json_dict = {"next_words": []}
        for key in prediction_dict:
            json_dict["next_words"].append({
                "word": key,
                "probability": prediction_dict[key]
            })
        return json_dict
