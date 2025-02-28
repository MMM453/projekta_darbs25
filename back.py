from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

seasons = ["2023", "2022", "2021"]
race_data = {
    "2023": {
        "races": [
            {"name": "Australian GP", "date": "2023-04-02", "position": random.randint(1, 10)},
            {"name": "Bahrain GP", "date": "2023-03-05", "position": random.randint(1, 10)}
        ]
    },
    "2022": {
        "races": [
            {"name": "French GP", "date": "2022-07-24", "position": random.randint(1, 10)},
            {"name": "British GP", "date": "2022-07-03", "position": random.randint(1, 10)}
        ]
    },
    "2021": {
        "races": [
            {"name": "Monaco GP", "date": "2021-05-23", "position": random.randint(1, 10)},
            {"name": "Azerbaijan GP", "date": "2021-06-06", "position": random.randint(1, 10)}
        ]
    }
}

@app.route('/')
def index():
    return render_template('index.html', seasons=seasons)

@app.route('/get_race_data/<season>', methods=['GET'])
def get_race_data(season):
    if season in race_data:
        return jsonify(race_data[season])
    else:
        return jsonify({"error": "Season not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
