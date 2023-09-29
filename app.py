from forms import AddPetForm, EditPet
from flask import Flask, render_template, request, redirect, flash, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///petadoption'
""" app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_RECORD_QUERIES'] = True """
""" app.config['DEBUG'] = True """
app.config['SECRET_KEY'] = "SECRET!"

toolbar = DebugToolbarExtension(app)
""" app.debug = True
 """

connect_db(app)
""" db.create_all() """
app.app_context().push()


@app.route("/")
def home_page():
    """ Render home page. Show all pets."""

    pets = Pet.query.all()

    return render_template('index.html', pets=pets)


@app.route("/add")
def add_pet_form():
    """ Render form for new pet."""

    form = AddPetForm()
    print("******************")
    print(form)

    return render_template("add.html", form=form)


@app.route("/add", methods=["POST"])
def add_pet():
    """Add new pet."""
    
    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        print(name)
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        new_pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(new_pet)
        db.session.commit()
        print(new_pet)

        return redirect("/")

    else:

        return render_template("add.html", form=form)


@app.route('/<int:pet_id>', methods=["GET"])
def render_edit_form(pet_id):
    """ Render edit form."""

    pet = Pet.query.get_or_404(pet_id)
    form = EditPet(obj=pet)

    return render_template("edit_pet.html", pet=pet, form=form)    


@app.route('/<int:pet_id>', methods=["POST"])
def edit_pet(pet_id):
    """ Handle edit form."""

    pet = Pet.query.get_or_404(pet_id)
    form = EditPet(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()

        return redirect("/")
        
    else:
        
        return render_template("edit_pet.html", form=form, pet=pet)


@app.route("/api/pets/<int:pet_id>", methods=['GET'])
def api_get_pet(pet_id):
    """Return basic info about pet in JSON."""

    pet = Pet.query.get_or_404(pet_id)
    info = {"name": pet.name, "age": pet.age}

    return jsonify(info)