from flask import Flask, render_template, request

app = Flask("ElyseApp")

utilisateurs = []

@app.route("/", methods=["GET", "POST"])
def accueil():
    if request.method == "POST":
        utilisateur = {
            "nom": request.form.get("nom"),
            "prenom": request.form.get("prenom"),
            "situation_matrimoniale": request.form.get("situation_matrimoniale"),
            "age": request.form.get("age"),
            "email": request.form.get("email"),
            "ville": request.form.get("ville"),
            "message": request.form.get("message"),
        }
        utilisateurs.append(utilisateur)
    return render_template("fiche.html", utilisateurs=utilisateurs)
