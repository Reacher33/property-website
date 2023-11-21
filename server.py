from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/properties")
def properties():
    return render_template("properties.html")


@app.route("/property-single")
def property_single():
    return render_template("property-single.html")


@app.route("/service")
def services():
    return render_template("services.html")


if __name__ == "__main__":
    app.run(debug=True)
