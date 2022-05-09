import requests as r
from typing import List

req = r.Requests()


def main():

    while i != 3:
        print("Selectionnez l'action souhaitée")
        print(" Connectez vous : 1 ")
        print("Inscrivez vous : 2 ")
        print("Arreter le programme : 3")

        i = int(input("Choississez l'option:"))

        if i == 3:
            return

        num = int(input("Entrez votre numéro de téléphone:"))

        if i == 1:
            raw = req.getUserByNum(num)
            if not raw:
                print("Compte inexistant")
            else:
                userInterface(raw, req)
                pass
        elif i == 2:
            nom = str(input("Entrez votre prénom et votre nom"))
            adresse = str(input("Entrez votre adresse"))
            result = req.createUser(num, nom, adresse)
            if result:
                print("Le client a bien été crée")
            else:
                print("Client déjà existant")


def userInterface(raw: List[str]):
    i = 5
    while i != 5:
        print("---------------------------------------")
        print(
            f"Bonjour {raw[1]}, \n Numéro de téléphone: {raw[0]} \n Adresse: {raw[2]}"
        )
        print("---------------------------------------")
        print("1. Afficher vos comptes Courants")
        print("2. Afficher vos comptes Epargnes")
        print("3. Afficher vos comptes Revolvings")
        print("3. Créer/Ajouter un compte bancaire")
        print("4. Supprimer/Retirer un compte bancaire")
        print("5. Modifier votre profil")
        print("6. Supprimer votre profil")

    pass


def displayAccount(num: int, type: str):

    pass


def makeOperation(num: int):
    pass


def addAccount(num: int):
    pass


def removeAccount(num: int):
    pass


def modifyProfile(num: int):
    nom = str(input("Entrez votre prénom et votre nom"))
    adresse = str(input("Entrez votre adresse"))
    result = req.modifyUser(num, nom, adresse)
    if result:
        print("La modification a fonctionné")
    else:
        print("La modification n'a pas fonctionné")
    pass


def deleteProfile(num: int):
    result = req.deleteUser(num)
    if result:
        print("Votre compte a bien été supprimé")
    else:
        print("Votre compte n'a pas être supprimé")


if __name__ == "__main__":
    main()
