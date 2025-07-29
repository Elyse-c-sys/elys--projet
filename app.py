from flask import Flask, render_template, request, redirect, url_for, session, send_file
import os
import csv

app = Flask(__name__)
app.secret_key = "cle_super_secrete"
GERANT_MDP = "Pension@2025"

DOSSIER_DONNEES = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DOSSIER_DONNEES, exist_ok=True)
FICHIER_CSV = os.path.join(DOSSIER_DONNEES, "clients.csv")


@app.route("/")
def accueil():
    return render_template("accueil.html")


@app.route("/gerant", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        numero = request.form.get("numero")
        mot_de_passe = request.form.get("mot_de_passe")

        if mot_de_passe == GERANT_MDP:
            session["gerant"] = {"nom": nom, "prenom": prenom, "numero": numero}
            return redirect(url_for("fiche"))
        else:
            return render_template("gerant.html", erreur="Mot de passe incorrect.")
    return render_template("gerant.html")


@app.route("/fiche", methods=["GET", "POST"])
def fiche():
    if "gerant" not in session:
        return redirect(url_for("login"))

    message = ""
    if request.method == "POST":
        type_piece = request.form.get("type_piece", "")
        numero_piece = request.form.get("numero_piece", "")
        nom_autre_piece = request.form.get("nom_autre_piece", "")

        if type_piece == "Autre" and nom_autre_piece:
            numero_piece += f" ({nom_autre_piece})"

        donnees = {
            "Nom": " ".join(request.form.get("nom_client", "").split()),
            "Prenom": " ".join(request.form.get("prenom_client", "").split()),
            "Date_naissance": request.form.get("date_naissance"),
            "Lieu_naissance": request.form.get("lieu_naissance"),
            "Nationalite": request.form.get("nationalite"),
            "Profession": request.form.get("profession"),
            "Organisme": request.form.get("organisme"),
            "Domicile_legal": request.form.get("domicile_legal"),
            "Venant_de": request.form.get("venant_de"),
            "Allant_a": request.form.get("allant_a"),
            "Transport": request.form.get("transport"),
            "Telephone": request.form.get("telephone"),
            "Type_piece": type_piece,
            "Numero_piece": numero_piece,
            "Date_delivrance": request.form.get("date_delivrance"),
            "Lieu_delivrance": request.form.get("lieu_delivrance"),
            "Date_arrivee": request.form.get("date_arrivee"),
            "Date_depart": request.form.get("date_depart"),
            "Motif": request.form.get("motif"),
            "Date_renseignement": request.form.get("date_renseignement")
        }

        ecrire_entete = not os.path.exists(FICHIER_CSV)
        with open(FICHIER_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=donnees.keys())
            if ecrire_entete:
                writer.writeheader()
            writer.writerow(donnees)

        message = "✅ Client enregistré avec succès"

    clients = []
    if os.path.exists(FICHIER_CSV):
        with open(FICHIER_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            clients = list(reader)

    return render_template("fiche.html", clients=clients, message=message)


@app.route("/export")
def export():
    if os.path.exists(FICHIER_CSV):
        return send_file(FICHIER_CSV, as_attachment=True)
    return "Aucune donnée à exporter."


@app.route("/logout")
def logout():
    session.pop("gerant", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
