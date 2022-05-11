import requests as r
from typing import List
import display as d

req = r.Requests()
disp = d.Display(req)

def main():

    i = 0

    try:
        while True:
            print("GESTION DE COMPTES BANCAIRES")
            print("---------------------------- \n")
            print("Selectionnez l'action souhaitée")
            print("1. Connectez vous")
            print("2. Inscrivez vous")
            print("3. Modifier un profil")
            print("4. Supprimer un profil")
            print("5. Arreter le programme")

            i = int(input("Choississez l'option: "))

            if i == 5:
                return

            num = int(input("Entrez votre numéro de téléphone: "))

            if i == 1:
                raw = req.getUserByNum(num)
                if not raw:
                    print("Compte inexistant")
                else:
                    userInterface(raw)
            elif i == 2:
                createProfile(num)
            elif i == 3:
                modifyProfile(num)
            elif i==4:
                deleteProfile(num)
    finally:
        req.close()


def userInterface(raw: List[str]):
    i = 0
    while i != 12:
        print("---------------------------------------")
        print(
            f"Bonjour {raw[1]}, \n Numéro de téléphone: {raw[0]} \n Adresse: {raw[2]}"
        )
        print("---------------------------------------")
        print("1. Voir vos comptes")
        print("2. Voir vos opérations")
        print("3. Déclarer l'appartenance d'un compte")
        print("4. Retirer l'appartenance d'un compte")
        print("5. Réaliser une opération")
        print("6. Rechercher une opération")
        print("7. Rechercher un compte")
        print("8. Créer un compte")
        print("9. Supprimer un compte")
        print("10. Traiter une opération")
        print("11. Modifier l'état d'un compte")

        print("12. Se Deconnecter")

        i = int(input("Choississez l'option: "))

        if i == 1:
            disp.displayUserAccounts(raw[0])
        elif i==2:
            disp.displayUserOperations(raw[0])
        elif i == 3:
            disp.displayAllAccounts()
            addUser(raw[0])
        elif i == 4:
            disp.displayUserAccounts(raw[0])
            removeAccount(raw[0])
        elif i==5:
            makeOperation(raw[0])
            pass
        elif i==6:
            findOperation()
        elif i==7:
            findCompte()
        elif i==8:
            creerCompte(raw[0])
        elif i==9:
            disp.displayUserAccounts(raw[0])
            supprimerCompte(raw[0])
        elif i==10:
            disp.displayUntreatedUserOperations(raw[0])
            traiterOperation(raw[0])
        elif i==11:
            disp.displayUserAccounts(raw[0])
            modifierStatutCompte(raw[0])

# CONNEXION

def createProfile(num: int):
    nom = str(input("Entrez votre prénom et votre nom: "))
    adresse = str(input("Entrez votre adresse: "))
    result = req.createUser(num, nom, adresse)
    if result:
        print("Le client a bien été crée")
    else:
        print("Client déjà existant")

def modifyProfile(num: int):
    nom = str(input("Entrez votre prénom et votre nom"))
    adresse = str(input("Entrez votre adresse"))
    result = req.modifyUser(num, nom, adresse)
    if result:
        print("La modification a fonctionné")
    else:
        print("La modification n'a pas fonctionné")

def deleteProfile(num: int):
    result = req.deleteUser(num)
    if result:
        print("Votre compte a bien été supprimé")
    else:
        print("Votre compte n'a pas être supprimé")


# INTERFACE DE COMPTE

def addUser(num: int):
    type = str(input("A quel type de compte voulez-vous être ajouté ? "))
    id = str(input("Quel est l'id de ce compte ? "))
    result = req.addUserToAccount(num, id, type)
    if result:
        return print("Vous avez bien été ajouté à ce compte")
    else:
        return print("Ce compte n'existe pas ou il vous appartient déjà")

def removeAccount(num: int):
    type = str(input("A quel type de compte voulez-vous être retiré ? "))
    id = str(input("Quel est l'id de ce compte ? "))
    result = req.removeUserFromAccount(num, id, type)
    if result:
        return print("Vous avez bien été retiré de ce compte")
    else:
        return print("Ce compte n'existe pas ou il ne vous appartient pas")

def findOperation():
    type = str(input("Quel type d'opération cherchez-vous ? "))
    date = str(input("Quelle est la date de cette opération ? "))
    result = req.getOperationByDate(date, type)
    disp.printOperation(result, type)

def findCompte():
    type = str(input("Quel type de compte cherchez-vous ? "))
    id = str(input("Quel est l'id de ce compte ? "))
    result = req.getAccountById(id)
    disp.printAccount(result, result, type, False)

def makeOperation(num: int):
    typeOperation = str(input("Quel type d'opération voulez-vous faire ? "))
    montant = int(input("Quel est le montant de l'opération ? "))
    disp.displayUserAccounts(num)
    typeCompte = str(input("Sur quel type de compte voulez-vous faire l'opération ? "))
    id = int(input("Quel est l'id du compte ? "))
    result = req.createOperation(id, num, typeOperation, typeCompte, montant)
    if result:
        return print("L'opération a bien été effectué")
    else:
        return print("Erreur dans la réalisation de l'opération")

def creerCompte(num: int):
    typeCompte = str(input("Quel type de compte? "))

    result = None
    if typeCompte == "epargne":
        solde = float(input("Solde du compte: "))
        interet = float(input("Interet mensuel: "))
        plafond = float(input("Plafond du solde: "))
        result = req.createEpargneAccount(num, interet, plafond, solde)
    elif typeCompte == "revolving":
        solde = float(input("Solde du compte: "))
        taux = float(input("Taux journalier: "))
        montant = float(input("Montant minimal: "))
        result = req.createRevolvingAccount(num, solde, taux, montant)
    elif typeCompte == "courant":
        solde = float(input("Solde du compte: "))
        decouvert = float(input("Decouvert maximal: "))
        result = req.createCourantAccount(num, solde, decouvert)
    else:
        print("Le type de compte est invalide")
        return

    if result:
        print("Le compte a bien été crée")
    else:
        print("La création du compte a echoué")

def supprimerCompte(num: int):
    typeCompte = str(input("Quel type de compte? "))
    id = str(input("Quel est l'id du compte à supprimer? "))
    result = req.deleteAccount(num, typeCompte, id)

    if result:
        print("Compte supprimé avec succès")
    else:
        print("Le compte n'existe pas ou la suppression du compte a échouée")

def traiterOperation(num: int):
    typeOperation = str(input("Quel est le type d'opération? "))
    id = int(input("Quel est l'id de l'opération? "))

    result = req.treatOperation(num, typeOperation, id)
    if result:
        print("L'opération a été traitée")
    else:
        confirmation = str(input("Le traitement a échoué. Souhaitez vous supprimer l'opération (O/N)? "))
        if confirmation in ["O", "o"]:
            result = req.deleteOperation(num, typeOperation, id)

def modifierStatutCompte(num: int):
    typeCompte = str(input("Quel type de compte voulez-vous modifier ? "))
    id = str(input("Quel est l'id de ce compte ? "))
    statut = str(input("Quel est le nouvel état du compte (Ouvert, Bloqué, Fermé) ? "))
    result = req.modifyAccountStatus(num, typeCompte, id, statut)

    if result:
        return print("Le statut du compte a bien été modifé")
    else:
        return print("Ce compte n'existe pas ou le changement de statut a échoué")


if __name__ == "__main__":
    main()
