import requests as r
from typing import List

req = r.Requests()


def main():

    i=0

    while i != 3:
        print("GESTION DE COMPTES BANCAIRES")
        print("---------------------------- \n")
        print("Selectionnez l'action souhaitée")
        print("1.Connectez vous")
        print("2.Inscrivez vous")
        print("3.Arreter le programme")

        i = int(input())

        if i == 3:
            return

        num = int(input("Entrez votre numéro de téléphone:"))

        if i == 1:
            raw = req.getUserByNum(num)
            if not raw:
                print("Compte inexistant")
            else:
                userInterface(raw)
        elif i == 2:
            nom = str(input("Entrez votre prénom et votre nom: "))
            adresse = str(input("Entrez votre adresse: "))
            result = req.createUser(num, nom, adresse)
            if result:
                print("Le client a bien été crée")
            else:
                print("Client déjà existant")


def userInterface(raw: List[str]):
    i = 0
    while i != 7:
        print("---------------------------------------")
        print(
            f"Bonjour {raw[1]}, \n Numéro de téléphone: {raw[0]} \n Adresse: {raw[2]}"
        )
        print("---------------------------------------")
        print("1. Voir vos comptes et réaliser des opérations")
        print("2. Voir vos opérations")
        print("3. Ajouter un compte")
        print("4. Retirer un compte")
        print("6. Modifier votre profil")
        print("7. Supprimer votre profil")
        print("8. Se Deconnecter")

        i = int(input("Choississez l'option: "))


        if i == 1:
            displayAccount(raw[0], 'courant')
        elif i==2:
            displayAccount(raw[0], 'epargne')
        elif i==3:
            displayAccount(raw[0], 'revolving')
        elif i==4:
            type = str(input("Quel type d'opération voulez-vous afficher ? "))
        elif i==12:
            accountsInterface(raw)
        elif i==5:
            pass
        elif i==6:
            modifyProfile(raw[0])
        elif i==7:
            deleteProfile(raw[0])

def accountsInterface(user: List[str]):
    print('-----------------------------------------')
    print('Compte Courants:')
    print('-----------------------------------------')
    raws = req.getCourantAccounts()
    for raw in raws:
        printAccount(raw, 'courant', False)
    print('-----------------------------------------')
    print('Compte Epargne:')
    print('-----------------------------------------')
    raws = req.getEpargneAccounts()
    for raw in raws:
        printAccount(raw, 'epargne', False)
    print('-----------------------------------------')
    print('Compte Revolving:')
    print('-----------------------------------------')
    raws = req.getRevolvingAccounts()
    for raw in raws:
        printAccount(raw, 'revolving', False)
    print('-----------------------------------------')

    type = str(input("Quel type de compte voulez-vous ajouter à l'utilisateur ? "))
    id = str(input("Quel est l'ID de ce compte ? "))

    result = req.addUserToAccount(raw[0], id, type)
    if result:
        print("L'utilisateur a bien été ajouté")
    else:
        print("Erreur dans l'ajout de l'utilisateur")

def userAccountsInterface(num: int, ):
    displayAccount(num, 'courant')
    displayAccount(num, 'epargne')
    displayAccount(num, 'revolving')

def displayAccount(num: int, type: str):
    raws = []
    if type == 'courant':
        raws = req.getUserCourantAccounts(num)
    elif type == 'epargne':
        raws = req.getUserEpargneAccounts(num)
    elif type == 'revolving':
        raws = req.getUserRevolvingAccounts(num)
    if not raws:
        return print(f'Auncun compte {type} trouvé')

    for raw in raws:
        print(f'---------- Compte {type}')
        printAccount(raw, type, True)


def printAccount(raw: List[str], type: str, join: bool) -> None:
    d=0
    if join:
        d = 4
    if type == 'courant':
        print(f"ID: {raw[0+d]}, Statut: {raw[2+d]} Solde: {raw[5+d]}, Decouvert autorisé: {raw[6+d]}, Début découvert: {raw[7+d]}")
    elif type == 'epargne':
        print(f"ID: {raw[0+d]}, Statut: {raw[2+d]}, Solde: {raw[5+d]}, Interet: {raw[3+d]}, Plafond: {raw[4+d]}")
    elif type == 'revolving':
        print(f"ID: {raw[0+d]}, Statut: {raw[2+d]}, Solde: {raw[5+d]}, Taux: {raw[3+d]}, Montant négocié: {raw[4+d]}")
    else:
        print("Bug")


def makeOperation(num: int):
    pass


def addAccount(num: int, id: int):
    result = req.addUserToAccount(num, id, 'courant')
    if result:
        return print("Vous avez bien été ajouté à ce compte")
    else:
        return print("Ce compte n'existe pas ou il vous appartient déjà")


def removeAccount(num: int):
    result = req.removeUserFromAccount(num, id, 'courant')
    if result:
        return print("Vous avez bien été retiré de ce compte")
    else:
        return print("Ce compte n'existe pas ou il ne vous appartient pas")


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
