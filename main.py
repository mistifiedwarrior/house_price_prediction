from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from core import get_training_data, predict_price, train_model

app = Flask(__name__)
CORS(app, support_credentials=True)

def validate_data(all_locations, data):
    try:
        location = data["location"]
        size = int(data["size"])
        area = int(data["area"])
        bath = int(data["bath"])
        error = False
        if all_locations.count(location) == 0 or \
                not (0 < size <= 50) or \
                not ((size * 300) <= area <= (size * 600)) or \
                not (0 <= bath <= size):
            error = True
        return error, location, size, area, bath
    except ValueError:
        return True, "", 0, 0, 0

@app.route("/locations", methods=["GET"])
@cross_origin(supports_credentials=True)
def get_locations():
    return jsonify({"locations": locations})

@app.route('/predict-price', methods=['POST'])
@cross_origin(supports_credentials=True)
def predict_house_price():
    error, location, size, area, bath = validate_data(locations, request.get_json())
    if error:
        return app.response_class(status=400)
    price = predict_price(regression, X, location, size, area, bath)
    return jsonify({"price": price})

if __name__ == '__main__':
    print("Training Model ...")
    X, Y = get_training_data()
    locations = list(X.columns[3:])
    regression = train_model(X, Y)
    print("Training Completed")
    app.run()
