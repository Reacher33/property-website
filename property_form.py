from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FieldList, FormField, IntegerField
from wtforms.validators import DataRequired


class ImageForm(FlaskForm):
    url = StringField('Image URL', validators=[DataRequired()])


# WTForm for creating a new property
class PropertyForm(FlaskForm):
    id = IntegerField("Property ID", validators=[DataRequired()])
    price = IntegerField("Property price", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    toilet = IntegerField("Number of toilet", validators=[DataRequired()])
    bed = IntegerField("Number of bedrooms", validators=[DataRequired()])
    caption = TextAreaField('Caption')
    images = FieldList(FormField(ImageForm), min_entries=4)  # FieldList to handle multiple images

    submit = SubmitField("Submit Post")
