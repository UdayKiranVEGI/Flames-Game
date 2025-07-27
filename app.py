from flask import Flask, render_template, request
import json
import os
from datetime import datetime

app = Flask(__name__)

FLAMES_MAP = {
    'F': 'Friendship 🤝',
    'L': 'Love ❤️',
    'A': 'Affection 😊',
    'M': 'Marriage 💍',
    'E': 'Enemy 😡',
    'S': 'Sibling 👫',
}

RESULTS_FILE = "results.json"

def flames_logic(name1, name2):
    n1 = name1.lower().replace(" ", "")
    n2 = name2.lower().replace(" ", "")

    for char in name1:
        if char in n2:
            n1 = n1.replace(char, '', 1)
            n2 = n2.replace(char, '', 1)

    count = len(n1 + n2)
    flames = list("FLAMES")
    index = 0

    while len(flames) > 1:
        index = (index + count - 1) % len(flames)
        flames.pop(index)

    return FLAMES_MAP[flames[0]]

def save_to_json(name1, name2, result):
    entry = {
        "name1": name1,
        "name2": name2,
        "result": result,
        "timestamp": datetime.now().isoformat()
    }

    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(RESULTS_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        name1 = request.form.get("name1")
        name2 = request.form.get("name2")
        if name1 and name2:
            result = flames_logic(name1, name2)
            save_to_json(name1, name2, result)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
