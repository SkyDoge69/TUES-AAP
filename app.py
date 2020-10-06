from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'shushumushu'


@app.route("/", methods=["GET", "POST"])
def index():
    return ("And so it begins..")

if __name__ == "__main__":
    app.run(debug=True)