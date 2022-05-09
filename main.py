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
        print("1. Afficher vos comptes Courants")
        print("2. Afficher vos comptes Epargnes")
        print("3. Afficher vos comptes Revolvings")
        print("4. Ajouter un propriétaire de compte bancaire")
        print("5. Supprimer un propriétaire de compte bancaire")
        print("5. Réaliser une  opération")
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
            accountsInterface(raw)
        elif i==5:
            pass
        elif i==6:
            modifyProfile(raw[0])
        elif i==7:
            deleteProfile(raw[0])

def accountsInterface(raw: List[str]):
    print('-----------------------------------------')
    print('Compte Courants:')
    print('-----------------------------------------')
    raws = req.getCourantAccounts()
    for raw in raws:
        printAccount(raw, 'courant')
    print('-----------------------------------------')
    print('Compte Epargne:')
    print('-----------------------------------------')
    raws = req.getEpargneAccounts()
    for raw in raws:
        printAccount(raw, 'epargne')
    print('-----------------------------------------')
    print('Compte Revolving:')
    print('-----------------------------------------')
    raws = req.getRevolvingAccounts()
    for raw in raws:
        printAccount(raw, 'revolving')
    print('-----------------------------------------')

    type = str(input("Quel type de compte voulez-vous ajouter à l'utilisateur ? "))
    id = str(input("Quel est l'ID de ce compte ? "))

    result = req.addUserToAccount(raw[0], id, type)
    if result:
        print("L'utilisateur a bien été ajouté")
    else:
        print("Erreur dans l'ajout de l'utilisateur")



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
        printAccount(raw, type)


def printAccount(raw: List[str], type: str) -> None:
    if type == 'courant':
        print(f"ID: {raw[4]}, Statut: {raw[6]} Solde: {raw[9]}, Decouvert autorisé: {raw[10]}, Début découvert: {raw[11]}")
    elif type == 'epargne':
        print(f"ID: {raw[4]}, Statut: {raw[6]}, Solde: {raw[9]}, Interet: {raw[7]}, Plafond: {raw[8]}")
    elif type == 'revolving':
        print(f"ID: {raw[4]}, Statut: {raw[6]}, Solde: {raw[9]}, Taux: {raw[7]}, Montant négocié: {raw[8]}")
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
