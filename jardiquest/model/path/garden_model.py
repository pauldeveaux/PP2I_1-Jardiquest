import os.path
import uuid

from jardiquest.model.database.entity.jardin import Jardin
from flask import *
from flask_login import *

from jardiquest.model.database.entity.user import User
from jardiquest.model.database.upload import upload_file, delete_file, file_exist
from jardiquest.setup_flask import UPLOAD_FOLDER
from jardiquest.setup_sql import db


def garden_model():
    jardin_de_user = Jardin.query.filter_by(idJardin=current_user.idJardin).first()
    # all the gardens he can access
    if jardin_de_user is not None:
        jardins = Jardin.query.filter(Jardin.idJardin != jardin_de_user.idJardin)
    else:
        jardins = Jardin.query.all()
    if request.method == 'POST':
        nom = request.form['filtreNom']
        description = request.form['filtreDescription']
        monnaie = request.form['filtreMonnaie']
        ville = request.form['filtreVille']
        adresse = request.form['filtreAdresse']

        name = "%{}%".format(nom)
        monnaie = "%{}%".format(monnaie)
        description = "%{}%".format(description)
        ville = "%{}%".format(ville)
        adresse = "%{}%".format(adresse)

        if jardin_de_user is not None:
            jardins = Jardin.query.filter(Jardin.name.like(name),
                                          Jardin.idJardin != jardin_de_user.idJardin,
                                          Jardin.moneyName.like(monnaie),
                                          Jardin.description.like(description),
                                          Jardin.ville.like(ville),
                                          Jardin.adresse.like(adresse)
                                          ).all()
        else:
            jardins = Jardin.query.filter(Jardin.name.like(name),
                                          Jardin.moneyName.like(monnaie),
                                          Jardin.description.like(description),
                                          Jardin.ville.like(ville),
                                          Jardin.adresse.like(adresse)
                                          ).all()

    table = []
    for i in jardins:
        row = [i.name, i.description.replace('\r', '').replace('\n', "<br>"), i.moneyName, i.ville, i.adresse, i.nbParticipants, i.idJardin]
        table.append(row)

    return render_template('garden.html', jsTable=table, user=current_user,
                           ispicture=file_exist(os.path.join(UPLOAD_FOLDER, "garden"), current_user.idJardin),
                           jardin=jardin_de_user, total=len(table))


def new_garden_model():
    if request.method == 'POST':
        nom = request.form['nom']
        description = request.form['description']
        monnaie = request.form['monnaie']
        adresse = request.form['adresse']
        ville = request.form['ville']

        # verification if name and money are unique
        jar = Jardin.query.filter_by(name=nom).first()
        mon = Jardin.query.filter_by(moneyName=monnaie).first()
        error = False

        if jar is not None:
            flash(f"Le nom de jardin \"{nom}\" existe déjà")
            error = True
        if mon is not None:
            flash(f"Le nom de monnaie \"{monnaie}\" existe déjà")
            error = True

        if error:
            return redirect(url_for('controller.new_garden'))

        id = generate_id(nom)

        # create it
        new_garden = Jardin(idJardin=id, name=nom, moneyName=monnaie, description=description, adresse=adresse,
                            ville=ville, nbParticipants=1)
        db.session.add(new_garden)

        # update user status
        current_user.update_garden(id)
        current_user.update_role('Proprietaire')
        current_user.update_balance(0)

        upload_file(request, 'garden', id)

        db.session.commit()

        return redirect(url_for('controller.garden'))

    return render_template("new_garden.html", user=current_user)


def choose_model(choose):
    jar = Jardin.query.filter_by(idJardin=choose).first()
    jar.update_nbParticipants(int(jar.nbParticipants) + 1)
    flash(f"Vous avez rejoint le jardin \"{jar.name}\" en tant que participant")

    # update user status
    current_user.update_garden(choose)
    current_user.update_balance(0)
    db.session.commit()
    return redirect(url_for('controller.garden'))


def leave_model(id):
    jar = Jardin.query.filter(Jardin.idJardin == id).first()
    nb = int(jar.nbParticipants) - 1
    if nb < 0:
        nb = 0
    jar.update_nbParticipants(nb)
    current_user.update_garden('')
    db.session.commit()
    flash(f"Vous avez quitté le jardin")
    return redirect(url_for('controller.garden'))


def delete_model():
    idJardin = current_user.idJardin

    users = User.query.filter(User.idJardin == current_user.idJardin)
    for user in users:
        if user.role == "Participant":
            user.update_garden('')
    db.session.commit()

    Jardin.query.filter(Jardin.idJardin == current_user.idJardin).delete()
    if file_exist(os.path.join(UPLOAD_FOLDER, 'garden'), idJardin):
        delete_file(os.path.join(UPLOAD_FOLDER, 'garden'), idJardin)

    current_user.update_garden('')
    current_user.update_role('Participant')
    db.session.commit()
    flash(f"Vous avez supprimé votre jardin")
    return redirect(url_for('controller.garden'))


def modify_garden_model():
    jardin = Jardin.query.filter_by(idJardin=current_user.idJardin).first()
    if request.method == 'POST':
        nom = request.form['nom']
        description = request.form['description']
        monnaie = request.form['monnaie']
        adresse = request.form['adresse']
        ville = request.form['ville']

        garden = Jardin.query.filter_by(idJardin=jardin.idJardin).first()
        own_name = garden.name
        own_money = garden.moneyName

        error = False

        # if the name if modified --> verify if already exists
        if nom != own_name:
            jar = Jardin.query.filter(Jardin.idJardin != jardin.idJardin, Jardin.name == nom).first()
            if jar is not None:
                flash(f"Le nom de jardin \"{nom}\" existe déjà")
                error = True

        # if the money if modified --> verify if already exists
        if monnaie != own_money:
            mon = Jardin.query.filter(Jardin.idJardin != jardin.idJardin, Jardin.moneyName == monnaie).first()
            if mon is not None:
                flash(f"Le nom de monnaie \"{monnaie}\" existe déjà")
                error = True

        if error:
            return redirect(url_for('controller.modify_garden'))

        # modify it
        jardin.update_name(nom)
        jardin.update_description(description)
        jardin.update_money(monnaie)
        jardin.update_address(adresse)
        jardin.update_city(ville)

        print(upload_file(request, 'garden', jardin.idJardin))

        db.session.commit()

        flash(f"Le jardin a été modifié avec succès")
        return redirect(url_for('controller.garden'))

    return render_template("modify_garden.html", user=current_user, jardin=jardin)


def generate_id(moneyName):
    return uuid.uuid1().hex
