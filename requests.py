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
        self.operation_state = ["Traitée", "Non Traitée"]
        self.account_type = ["courant", "revolving", "epargne"]
        self.operation_type = ["cartebleu", "virement", "chequier", "espece"]

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

    def getUserByNum(self, num: int) -> List[str]:
        self.cur.execute("SELECT * FROM clients WHERE telephone = %s", (num,))
        return self.cur.fetchone()

    def getUserAccountsId(self, num: int):
        self.cur.execute(
            "SELECT Courant, Revolving, Epargne FROM Appartenance WHERE client = %s",
            (num,),
        )
        return self.__getAccounts(self.cur.fetchall())

    def __getAccounts(self, ids):
        accounts = []
        for elem, id in zip(self.account_type, ids):
            self.cur.execute(f"SELECT * FROM {elem} WHERE id = {id}")
            accounts.append(self.cur.fetchone())
        return accounts

    # GESTION D'UN UTILISATEUR

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

    def getUserCourantAccounts(self, num: int):
        try:
            self.cur.execute(
                "SELECT * FROM appartenance INNER JOIN comptescourant ON appartenance.courant = comptescourant.id WHERE client=%s",
                (num,),
            )
            return self.cur.fetchall()
        except sql.Error as e:
            self.utils.writeLogs(e)
            return None

    def getUserEpargneAccounts(self, num: int):
        try:
            self.cur.execute(
                "SELECT * FROM appartenance INNER JOIN comptesepargne ON appartenance.epargne = comptesepargne.id WHERE client=%s",
                (num,),
            )
            return self.cur.fetchall()
        except sql.Error as e:
            self.utils.writeLogs(e)
            return None

    def getUserRevolvingAccounts(self, num: int):
        try:
            self.cur.execute(
                "SELECT * FROM appartenance INNER JOIN comptescrevolving ON appartenance.revolving = comptesrevolving.id WHERE client=%s",
                (num,),
            )
            return self.cur.fetchall()
        except sql.Error as e:
            self.utils.writeLogs(e)
            return None

    def getUserOperations(self, num: int, type: str) -> List[List[str]]:
        if type not in self.operation_type:
            return None

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

    def createRevolvingAccount(
        self, num: int, solde: int, taux: int, montant: int
    ) -> bool:
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

    def createEpargneAccount(
        self, num: int, interet: int, plafond: int, solde: int
    ) -> bool:
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
                "UPDATE comptescourant SET decouvert=%s WHERE id=%s", (decouvert, id)
            )
            return True
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    def modifyRevolvingAccount(self, id: int, taux: int) -> bool:
        try:
            self.cur.execute(
                "UPDATE comptesrevolving SET taux=%s WHERE id=%s", (id, taux)
            )
            return True
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    def modifyEpargneAccount(self, num: int, interet: int) -> bool:
        try:
            self.cur.execute(
                "UPDATE comptesrevolving SET interet=%s WHERE id=%s", (id, interet)
            )
            return True
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    # RECUPERATION DES COMPTES BANCAIRES

    def getCourantAccounts(self):
        try:
            self.cur.execute("SELECT * FROM comptescourant")
            return self.cur.fetchall()
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    def getEpargneAccounts(self):
        try:
            self.cur.execute("SELECT * FROM comptesepargne")
            return self.cur.fetchall()
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False

    def getRevolvingAccounts(self):
        try:
            self.cur.execute("SELECT * FROM comptesrevolving")
            return self.cur.fetchall()
        except sql.Error as e:
            self.utils.writeLogs(e)
            return False



    # SUPPRESION D'UN COMPTE

    def deleteAccount(self, id: int):
        pass

    # Insertion d'une opération

    def createOperation(self, compte: int, client: int, op_type: str, acc_type: str, montant: int):
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
            self.__updateSoldById(compte, acc_type, montant)
            return True
        except sql.Error as e:
            print(e)
            self.utils.writeLogs(e)
            return False
        pass

    def operationCheque(self):
        pass

    def operationGuichet(self):
        pass
        pass

    # GESTION DES RELATIONS COMPTES - CLIENTS

    def addUserToAccount(self, num: int, id: int, type: str) -> bool:
        try:
            self.cur.execute(
                "INSERT INTO appartenance (client, %s) VALUES (%s, %s)",
                (AsIs(type), num, id),
            )
            return True
        except sql.Error as e:
            return False

    def removeUserFromAccount(self, num: int, id: int, type: str) -> bool:
        try:
            self.cur.execute(
                "DELETE FROM appartenance WHERE client=%s AND %s=%s",
                (num, AsIs(type), id),
            )
            return True
        except sql.Error as e:
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
            print(e)
            return False
