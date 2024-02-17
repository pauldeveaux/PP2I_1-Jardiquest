import math
import uuid
from datetime import datetime

from flask import *
from flask_login import *

from jardiquest.model.database.entity.catalogue import Catalogue
from jardiquest.model.database.entity.commande import Commande
from jardiquest.model.database.entity.jardin import Jardin
from jardiquest.model.database.entity.recolte import Recolte
from jardiquest.setup_sql import db


def suggestion_model():
    jardin = Jardin.query.filter_by(idJardin=current_user.idJardin).first()
    if jardin is not None:
        recoltes = Recolte.query.filter(Recolte.idJardin == jardin.idJardin)
    else:
        recoltes = []

    solde = current_user.balance  # money the customer has
    if request.method == 'POST':
        if request.form['balance'] !='' :
            solde = int(float(request.form['balance']))

    if solde is None:
        solde = 0

    panier = glouton_solution(recoltes, solde)  # recommended product bundles
    prix = prix_panier(panier)  # total price

    result = creation_dictionnaire(panier)  # dictionary {id_produit,[qtt,lot]}

    produits, numbs, recoltes, ids = [], [], [], []

    for cle, valeur in result.items():  # creating tables for template
        catalogue = Catalogue.query.filter(Catalogue.idCatalogue == valeur[1][0]).first()
        recolte = Recolte.query.filter(Recolte.idRecolte == cle).first()
        produits.append(catalogue)
        recoltes.append(recolte)
        numbs.append(valeur[0])
        ids.append(cle)

    return render_template('suggestion.html', jardin=jardin, user=current_user, recoltes=recoltes, numbs=numbs,
                           produits=produits, prix=prix, length=len(result), ids=ids)


def buy_model(numbs, ids):
    try:
        ids = jsonify(ids)
        numbs = json.loads(numbs)
    except:
        ids = []
        numbs = []
    for i in range(0, len(numbs)):
        selling = db.session.query(Recolte).filter(Recolte.idRecolte == ids[i]).first()
        if selling.qtt_recommandee is not None:
            buy_product(numbs[i] * selling.qtt_recommandee, selling)
    return redirect(url_for('controller.suggestion'))


def jsonify(ids):
    ids = ids.replace("'", "")
    ids = ids.replace(" ", "")
    ids = ids.replace("[", "")
    ids = ids.replace("]", "")
    return ids.split(',')


def buy_product(quantity, selling):
    if selling is None or quantity > selling.quantity or quantity <= 0 or selling.jardin != current_user.jardin:
        abort(404)

    total_price = selling.cost * quantity

    if current_user.balance < total_price:
        flash("Votre solde n'est pas suffisant", "error")
    else:
        # If no error :
        # Decrease quantity, and delete if no more
        selling.quantity -= quantity
        selling.quantity = math.floor(selling.quantity * 100) / 100

        # Decrease user balance
        current_user.balance -= total_price
        current_user.balance = math.floor(current_user.balance * 100) / 100

        # Create an order
        commande = Commande(idCommande=uuid.uuid1().hex, acheteur=current_user.email, idRecolte=selling.idRecolte,
                            quantite=quantity, cout=total_price, dateAchat=datetime.now())
        db.session.add(commande)
        db.session.commit()


def creation_dictionnaire(panier):
    return dict((i[3], [panier.count(i), i]) for i in panier)


def prix_panier(panier):
    somme = 0
    for i in range(0, len(panier)):
        somme = somme + panier[i][1]
    return somme


def glouton_solution(recoltes, solde):
    tab = creation_lots(recoltes)  # First step : creation of batches according to the recommended quantity

    tri_bulle(tab)  # Second step : sorting lots by price to minimize the final basket price

    ordre = tri_loop(tab, [])  # Third step : sorting to maximize diversity

    panier = remplir_panier(ordre, solde)  # Fourth step :creation of the basket according to the limit of the balance

    return panier


def creation_lots(recoltes):
    tab = []
    for i in range(0, len(recoltes[:])):
        if (recoltes[i].cost is not None and recoltes[i].quantity is not None and
                recoltes[i].qtt_recommandee is not None and
                recoltes[i].idCatalogue is not None and recoltes[i].idRecolte is not None):
            for j in range(0, int(recoltes[i].quantity / recoltes[i].qtt_recommandee)):
                tab.append([recoltes[i].idCatalogue, recoltes[i].cost * recoltes[i].qtt_recommandee,
                            recoltes[i].qtt_recommandee, recoltes[i].idRecolte])
    return tab


def remplir_panier(ordre, solde):
    panier = []
    for i in range(0, len(ordre)):
        if solde - ordre[i][1] > 0:
            solde = solde - ordre[i][1]
            panier.append(ordre[i])
    return panier


def tri_bulle(tab):  # bubble sorting
    n = len(tab)
    for i in range(n):
        for j in range(0, n - i - 1):
            if tab[j][1] > tab[j + 1][1]:
                tab[j], tab[j + 1] = tab[j + 1], tab[j]


def tri_loop(tab, last):  # recursive sorting of batches to maximize diversity
    liste = tab[:]
    memoire = []
    panier = []
    for i in range(0, len(liste)):
        if liste[i][0] not in memoire:
            memoire.append(liste[i][0])
            panier.append(liste[i])
            liste[i] = 0
    liste = [value for value in liste if value != 0]

    if liste:
        return tri_loop(liste, last + panier)
    else:
        return last + panier
