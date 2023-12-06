from flask import Flask, render_template, redirect, url_for, request, jsonify
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


# Custom Jinja2 filter to format number with commas
def format_number(value):
    return "{:,}".format(value)


# Adding the filter to the Jinja2 environment
app.jinja_env.filters['format'] = format_number


class Property(db.Model):
    __tablename__ = "properties"
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    toilet = db.Column(db.Integer, nullable=True)
    bed = db.Column(db.Integer, nullable=True)
    caption = db.Column(db.String(200))

    images = relationship("Image", back_populates="property")

    def to_dict(self):
        # Method 1.
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

        # Method 2. Alternatively use Dictionary Comprehension to do the same thing.
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}


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
    property_data = db.session.execute(db.select(Property)).scalars().all()

    return render_template("index.html", property_data=property_data)


@app.route("/properties")
def properties():
    property_data = db.session.execute(db.select(Property)).scalars().all()

    return render_template("properties.html", property_data=property_data)


@app.route("/property-single/<int:property_id>")
def property_single(property_id):
    requested_property = db.get_or_404(Property, property_id)
    return render_template("property-single.html", property=requested_property)


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
            new_images = Image(img_url=image_data["url"],
                               property_id=property_id)  # Assign the property ID to the image
            db.session.add(new_images)
            db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_property.html", form=form)


@app.route("/search")
def search_property():
    image = []
    query_location = request.args.get("loc")
    all_properties = db.session.execute(db.select(Property).where(Property.location == query_location)).scalars().all()
    for property in all_properties:
        property_images = property.images
        for images in property_images:
            image.append(images.img_url)
    if all_properties:
        return jsonify(data={"property_images": [img for img in image], 'property': [property.to_dict() for property in all_properties]})
    else:
        return jsonify(error={"Not Found": "Sorry doesnt exist"})


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/service")
def services():
    return render_template("services.html")


if __name__ == "__main__":
    app.run(debug=True)
