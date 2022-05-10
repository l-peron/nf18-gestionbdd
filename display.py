from typing import List

class Display:
    def __init__(self, req):
        self.req = req
        self.account_type = ["courant", "revolving", "epargne"]
        self.operation_type = ["cartebleue", "virement", "cheque", "guichet"]

    def printOperation(self, raw: List[str], type: str) -> None:
        if not raw:
            return print('Opération non trouvée')
        if type == 'virement':
            print(
                f"ID: {raw[0]}, Date: {raw[6]}, Montant: {raw[5]}, ID-Compte: {raw[1] or raw[2] or raw[3]}, Etat: {raw[7]}")
        elif type == 'cartebleue':
            print(f"ID: {raw[0]}, Date: {raw[5]}, Montant: {raw[4]}, ID-Compte: {raw[1] or raw[2]}, Etat: {raw[6]}")
        elif type == 'cheque':
            print(f"ID: {raw[0]}, Date: {raw[5]}, Montant: {raw[4]}, ID-Compte: {raw[1] or raw[2]}, Etat: {raw[6]}")
        elif type == 'guichet':
            print(
                f"ID: {raw[0]}, Date: {raw[6]}, Montant: {raw[5]}, ID-Compte: {raw[1] or raw[2] or raw[3]}, Etat: {raw[7]}")
        else:
            print("Bug")

    def printAccount(self, raw: List[str], type: str, join: bool) -> None:
        if not raw:
            return print('Compte non trouvé')
        d = 0
        if join:
            d = 4
        if type == 'courant':
            print(
                f"ID: {raw[0 + d]}, Statut: {raw[2 + d]} Solde: {raw[5 + d]}, Decouvert autorisé: {raw[6 + d]}, Début découvert: {raw[7 + d]}")
        elif type == 'epargne':
            print(
                f"ID: {raw[0 + d]}, Statut: {raw[2 + d]}, Solde: {raw[5 + d]}, Interet: {raw[3 + d]}, Plafond: {raw[4 + d]}")
        elif type == 'revolving':
            print(
                f"ID: {raw[0 + d]}, Statut: {raw[2 + d]}, Solde: {raw[5 + d]}, Taux: {raw[3 + d]}, Montant négocié: {raw[4 + d]}")
        else:
            print("Bug")

    def displayUserAccounts(self, num: int):
        raws=[]
        for type in self.account_type:
            raws = self.req.getUserAccounts(num, type)
            print(f'---------- Compte {type} ----------')
            if raws:
                for raw in raws:
                    self.printAccount(raw, type, True)

    def displayUserOperations(self, num: int):
        raws=[]
        for type in self.operation_type:
            raws = self.req.getUserOperations(num, type)
            print(f'---------- Opérations {type} ----------')
            if raws:
                for raw in raws:
                    self.printOperation(raw, type)

    def displayAllAccounts(self):
        raws = []
        print("---- Affichage de tous les comptes bancaires ----")
        for type in self.account_type:
            raws = self.req.getAccountsByType(type)
            print(f'---------- Compte {type} ----------')
            if raws:
                for raw in raws:
                    self.printAccount(raw, type, False)




