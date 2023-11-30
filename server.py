from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from property_form import PropertyForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///properties.db'
db = SQLAlchemy()
db.init_app(app)


class Property(db.Model):
    __tablename__ = "properties"
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    price = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    toilet = db.Column(db.Integer, primary_key=True)
    bed = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.Text)

    images = relationship("Image", back_populates="property")


class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.Text, nullable=False)

    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"))
    property = relationship("Property", back_populates="images")


with app.app_context():
    db.create_all()

    result = db.session.execute(db.select(Property))
    posts = result.scalars().all()


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


@app.route("/add", methods=["GET", "POST"])
def add_property():
    form = PropertyForm()
    if request.method == "POST":
        new_property = Property(price=form.price.data, address=form.address.data, location=form.location.data,
                                toilet=form.toilet.data, bed=form.bed.data, caption=form.caption.data, id=form.id.data)
        db.session.add(new_property)
        db.session.commit()

        # Get the ID of the newly created property
        property_id = new_property.id

        # Loop through the submitted images and associate them with the new property
        for image_data in form.images.data:
            new_images = Image(img_url=image_data["url"], property_id=property_id)  # Assign the property ID to the image
            db.session.add(new_images)
            db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_property.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
