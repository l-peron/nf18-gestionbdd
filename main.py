import requests as r
from typing import List
import display as d

req = r.Requests()
disp = d.Display(req)


def main():

    i=0

    while i != 5:
        print("GESTION DE COMPTES BANCAIRES")
        print("---------------------------- \n")
        print("Selectionnez l'action souhaitée")
        print("1.Connectez vous")
        print("2.Inscrivez vous")
        print("3. Modifier un profil")
        print("4. Supprimer un profil")
        print("5.Arreter le programme")

        if i == 3:
            return

        if i == 1:
            num = int(input("Entrez votre numéro de téléphone:"))
            raw = req.getUserByNum(num)
            if not raw:
                print("Compte inexistant")
            else:
                userInterface(raw)
        elif i == 2:
            num = int(input("Entrez votre numéro de téléphone:"))
            nom = str(input("Entrez votre prénom et votre nom: "))
            adresse = str(input("Entrez votre adresse: "))
            result = req.createUser(num, nom, adresse)
            if result:
                print("Le client a bien été crée")
            else:
                print("Client déjà existant")
        elif i == 3:
            modifyProfile(num)
        elif i==4:
            deleteProfile(num)


def userInterface(raw: List[str]):
    i = 0
    while i != 10:
        print("---------------------------------------")
        print(
            f"Bonjour {raw[1]}, \n Numéro de téléphone: {raw[0]} \n Adresse: {raw[2]}"
        )
        print("---------------------------------------")
        print("1. Voir vos comptes")
        print("2. Voir vos opérations")
        print("3. Ajouter un compte")
        print("4. Retirer un compte")
        print("5. Réaliser une opération")
        print("6. Rechercher une opération")
        print("7. Rechercher un compte")
        print("8. Créer un compte")

        print("10. Se Deconnecter")

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

# CONNEXION

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
    type = str(input("Quel type d'opération cherchez-vous ? "))
    pass

if __name__ == "__main__":
    main()
