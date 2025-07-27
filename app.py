from flask import Flask, render_template, request

app = Flask(__name__)

FLAMES_MAP = {
    'F': 'Friendship 🤝',
    'L': 'Love ❤️',
    'A': 'Affection 😊',
    'M': 'Marriage 💍',
    'E': 'Enemy 😡',
    'S': 'Sibling 👫',
}


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


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        name1 = request.form.get("name1")
        name2 = request.form.get("name2")
        if name1 and name2:
            result = flames_logic(name1, name2)
    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
