
from flask import Flask, render_template, request
import random

app = Flask(__name__)

number = random.randint(1, 10)

@app.route("/", methods=["GET", "POST"])
def game():
    message = ""

    if request.method == "POST":
        guess = int(request.form["guess"])

        if guess == number:
            message = "🎉 Correct! You won!"
        elif guess < number:
            message = "Too low! Try again."
        else:
            message = "Too high! Try again."

    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)