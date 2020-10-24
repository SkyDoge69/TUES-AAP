from flask import Flask, render_template
from form import *

app = Flask(__name__)
app.secret_key = 'shushumushu'


@app.route("/", methods=["GET", "POST"])
def index():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        return render_template("choice.html", form = register_form)
    return render_template("index.html", form = register_form)

if __name__ == "__main__":
    app.run(debug=True)