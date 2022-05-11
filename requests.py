import utils
import psycopg2 as sql
from psycopg2._psycopg import AsIs
from datetime import datetime as dt
from typing import List


class Requests:
    def __init__(self):
        self.utils = utils.Utils()
        self.datas = self.utils.loadDatas()
        self.conn = self.__connect()
        self.conn.autocommit = True
        self.cur = self.__getCursor()
        self.account_state = ["Ouvert", "Bloqué", "Fermé"]
        self.operation_state = ["Non Traitée", "Traitée"]
        self.account_type = ["courant", "revolving", "epargne"]
        self.operation_type = ["cartebleue", "virement", "cheque", "guichet"]

    def __connect(self):
        try:
            conn = sql.connect(
                f'host={self.datas["host"]} dbname={self.datas["dbname"]} user={self.datas["user"]} password={self.datas["pswd"]}'
            )
            return conn
        except sql.Error as e:
            print("Erreur de connexion")
            return None

    def __getCursor(self):
        if self.conn:
            return self.conn.cursor()
        else:
            return None

    def close(self):
        self.conn.close()
        self.utils.close()

    # GESTION D'UN UTILISATEUR

    def getUserByNum(self, num: int) -> List[str]:
        self.cur.execute("SELECT * FROM clients WHERE telephone=%s", (num,))
        return self.cur.fetchone()

    def createUser(self, num: int, prenom: str, adresse: str) -> bool:
        try:
            self.cur.execute(
                "INSERT INTO clients VALUES (%s,%s,%s)", (num, prenom, adresse)
            )
            return True
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    def modifyUser(self, num: int, prenom: str, adresse: str) -> bool:
        try:
            self.cur.execute(
                "UPDATE clients SET prenom=%s, adresse=%s WHERE telephone=%s",
                (prenom, adresse, num),
            )
            return True
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    def deleteUser(self, num: int) -> bool:
        try:
            self.cur.execute("DELETE FROM clients WHERE telephone=%s", (num,))
            return True
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    def getUserAccounts(self, num: int, type: str) -> List[List[str]]:
        if (type not in self.account_type):
            print("Type de compte invalide")
            return False
        
        try:
            self.cur.execute(
                "SELECT * FROM appartenance INNER JOIN %s ON appartenance.%s = %s.id WHERE client=%s",
                (AsIs("comptes"+type), AsIs(type),AsIs("comptes"+type), num),
            )
            return self.cur.fetchall()
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    def getUserOperations(self, num: int, type: str) -> List[List[str]]:
        if (type not in self.operation_type):
            print("Type d'opération invalide")
            return False

        try:
            self.cur.execute(
                "SELECT * FROM %s WHERE client=%s",
                (AsIs("operations" + type), num)
            )
            return self.cur.fetchall()
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    def getUntreatedUserOperations(self, num: int, type: str) -> List[List[str]]:
        if (type not in self.operation_type):
            print("Type d'opération invalide")
            return False

        try:
            self.cur.execute(
                "SELECT * FROM %s WHERE client=%s AND etat=%s",
                (AsIs("operations" + type), num, self.operation_state[0])
            )
            return self.cur.fetchall()
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False


    # CREATION DES COMPTES BANCAIRES

    def createCourantAccount(self, num: int, solde: int, decouvert: int) -> bool:
        id = self.__generateAccountId()
        try:
            self.cur.execute(
                "INSERT INTO comptescourant VALUES (%s, current_timestamp , %s,%s,%s,%s,%s)",
                (id, self.account_state[0], solde, solde, solde, decouvert),
            )
            self.addUserToAccount(num, id, "courant")
            return True
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    def createRevolvingAccount(self, num: int, solde: int, taux: int, montant: int) -> bool:
        id = self.__generateAccountId()
        try:
            self.cur.execute(
                "INSERT INTO comptesepargne VALUES (%s, current_timestamp, %s,%s,%s,%s)",
                (id, self.account_state[0], taux, montant, solde),
            )
            self.addUserToAccount(num, id, "revolving")
            return True
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    def createEpargneAccount(self, num: int, interet: int, plafond: int, solde: int) -> bool:
        id = self.__generateAccountId()
        try:
            self.cur.execute(
                "INSERT INTO ComptesEpargne VALUES (%s, current_timestamp, %s,%s,%s,%s)",
                (id, self.account_state[0], interet, plafond, solde),
            )
            self.addUserToAccount(num, id, "epargne")
            return True
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    # MODIFICATION DES COMPTES BANCAIRES

    def modifyCourantAccount(self, id: int, decouvert: int) -> bool:
        try:
            self.cur.execute(
                "UPDATE comptescourant SET decouvert=%s WHERE id=%s AND id IN (SELECT courant FROM appartenance WHERE client=%s)", (decouvert, id, num)
            )
            return True
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    def modifyRevolvingAccount(self, id: int, taux: int) -> bool:
        try:
            self.cur.execute(
                "UPDATE comptesrevolving SET taux=%s WHERE id=%s AND id IN (SELECT courant FROM appartenance WHERE client=%s)", (id, taux, num)
            )
            return True
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    def modifyEpargneAccount(self, num: int, interet: int) -> bool:
        try:
            self.cur.execute(
                "UPDATE comptesrevolving SET interet=%s WHERE id=%s AND id IN (SELECT revolving FROM appartenance WHERE client=%s)", (id, interet, num)
            )
            return True
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    def modifyAccountStatus(self, num: int, type: str, id: int, statut: str) -> bool:
        if (type not in self.account_type):
            print("Type de compte invalide")
            return False

        if (statut not in self.account_state):
            print("Etat de compte invalide")
            return False

        try:

            self.cur.execute("UPDATE comptes%s SET statut=%s WHERE id=%s AND id IN (SELECT %s FROM appartenance WHERE client=%s)", (AsIs(type), statut, id, AsIs(type), num))
            return True
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    # RECUPERATION DES COMPTES BANCAIRES

    def getAccountsByType(self, type: str):
        if (type not in self.account_type):
            print("Type de compte invalide")
            return False

        try:
            self.cur.execute("SELECT * FROM comptes%s", (AsIs(type),))
            return self.cur.fetchall()
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    # SUPPRESION D'UN COMPTE

    def deleteAccount(self, num: int, type: str, id: int):
        if (type not in self.account_type):
            print("Type de compte invalide")
            return False

        try:
            self.cur.execute("DELETE FROM comptes%s WHERE id=%s AND id IN (SELECT %s FROM appartenance WHERE client=%s)", (AsIs(type), id, AsIs(type), num))
            return True
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    # Insertion d'une opération

    def createOperation(self, compte: int, client: int, op_type: str, acc_type: str, montant: int):
        if (acc_type not in self.account_type):
            print("Type de compte invalide")
            return False

        if (op_type not in self.operation_type):
            print("Type d'opération invalide")
            return False

        id = self.__generateOperationId()
        try:
            self.cur.execute(
                "INSERT INTO %s (id, %s, montant, etat, date, client) VALUES (%s, %s, %s, %s, current_timestamp, %s)",
                (
                    AsIs("operations" + op_type),
                    AsIs(acc_type),
                    id,
                    compte,
                    montant,
                    self.operation_state[0],
                    client
                ),
            )
            return True
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False
        pass

    def getOperationByDate(self, date: str, type: str):
        if (type not in self.operation_type):
            print("Type d'opération invalide")
            return False

        try:
            self.cur.execute(
                "SELECT * FROM %s WHERE date=%s",
                (AsIs("operations" + type), date)
            )
            return self.cur.fetchone()
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    # TRAITEMENT D'UNE OPERATION

    def treatOperation(self, num: int, id: str, type: str):
        if (type not in self.operation_type):
            print("Type d'opération invalide")
            return False

        try:
            self.cur.execute("SELECT * FROM operations%s WHERE id=%s AND etat=%s AND client=%s", (AsIs(type), id, operation_state[0], num))
            operation = self.cur.fetchone()
            if operation:
                result = self.__updateSoldById(compte, acc_type, montant)
                if result:
                    self.cur.execute("UPDATE operations%s SET etat=%s WHERE id=%s", (AsIs(type), operation_state[1], id))
                    return True
                else:
                    confirmation = str(input("La mise à jour du solde a échoué. Souhaitez vous supprimer l'opération (O/N)? "))
                    if confirmation in ["O", "o"]:
                        result = req.deleteOperation(num, typeOperation, id)
                    return False
            else:
                print("Aucune opération trouvée")
                return False
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    def deleteOperation(self, num: int, type: str, id: int):
        if (type not in self.operation_type):
            print("Type d'opération invalide")
            return False

        try:
            self.cur.execute("DELETE FROM operations%s WHERE id=%s AND client=%s", (AsIs(type), id, num))
            return True
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False


    # GESTION DES RELATIONS COMPTES - CLIENTS

    def addUserToAccount(self, num: int, id: int, type: str) -> bool:
        if (type not in self.account_type):
            print("Type de compte invalide")
            return False

        try:
            self.cur.execute(
                "INSERT INTO appartenance (client, %s) VALUES (%s, %s)",
                (AsIs(type), num, id),
            )
            return True
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    def removeUserFromAccount(self, num: int, id: int, type: str) -> bool:
        if (type not in self.account_type):
            print("Type de compte invalide")
            return False

        try:
            self.cur.execute(
                "DELETE FROM appartenance WHERE client=%s AND %s=%s",
                (num, AsIs(type), id),
            )
            return True
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    # GENERATIONS CLES COMPTES ET OPERATIONS

    def __generateAccountId(self) -> int:
        self.cur.execute(
            "SELECT MAX(id) FROM (SELECT id FROM ComptesEpargne UNION SELECT id FROM ComptesRevolving UNION SELECT id FROM ComptesCourant) AS comptes"
        )
        cle = self.cur.fetchone()
        if not cle[0]:
            return 1
        return cle[0] + 1

    def __generateOperationId(self) -> int:
        self.cur.execute(
            "SELECT MAX(id) FROM (SELECT id FROM operationscartebleue UNION SELECT id FROM operationscheque UNION SELECT id FROM operationsguichet UNION SELECT id FROM operationsvirement) AS operation"
        )
        cle = self.cur.fetchone()
        if not cle[0]:
            return 1
        return cle[0] + 1

    def getAccountById(self, id):
        self.cur.execute(
            "SELECT * FROM comptecourant, compterevolving, comptecourant WHERE Courant.id = {id} OR Revolving.id = {id} OR Epargne.id = {id}"
        )

    def __updateSoldById(self, id: int, type: str, var: int) -> bool:
        try:
            self.cur.execute("SELECT solde FROM %s WHERE id =%s", (AsIs('comptes'+type), id))
            raw = self.cur.fetchone()
            self.cur.execute(
                "UPDATE %s SET solde=%s WHERE id=%s",
                (AsIs("comptes" + type), raw[0] + var, id),
            )
            return True
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False
