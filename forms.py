from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField, TextAreaField
from wtforms.validators import InputRequired


class AddPetForm(FlaskForm):
    """ Form for adding pets to adoption agency."""

    name = StringField("Pet Name", validators=[InputRequired("Name must be listed.")])
    species = SelectField("Species of Pet", choices=[("cat","Cat"), ("dog","Dog"),("porcupine","Porcupine")])
    photo_url = StringField("Image of Pet")
    age = IntegerField("Age of Pet")
    notes = TextAreaField("Additional notes")


class EditPet(FlaskForm):
    """ Form for editing pet."""
    
    photo_url = StringField("Image of Pet")
    notes = TextAreaField("Additional notes")
    available = BooleanField("Is it available")