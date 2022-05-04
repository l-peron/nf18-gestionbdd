import utils
import psycopg2 as sql


class Requests:
    def __init__(self):
        self.utils = utils.Utils()
        self.datas = self.utils.loadDatas()
        self.conn = self.__connect()
        self.cur = self.__getCursor()
        self.account_state = ["Ouvert", "Bloqué", "Fermé"]
        self.operation_state = ["Traitée", "Non Traitée"]
        self.account_type = ["Epargne", "Courant", "Revolving"]

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
        if self.conn[0]:
            return self.conn.cursor()
        else:
            return None

    def getUserByNum(self, num):
        self.cur.execute(f"SELECT * FROM table WHERE num = {num}")
        return self.cur.fetchone()

    def getUsersByName(self, nom, prenom):
        self.cur.execute(f"SELECT * FROM table WHERE nom = {nom} AND prenom = {prenom}")
        return self.cur.fetchall()

    def getUserAccountsId(self, num):
        self.cur.execute(
            f"SELECT Courant, Revolving, Epargne FROM Appartenance WHERE id = {num}"
        )
        return self.__getAccounts(self.cur.fetchone())

    def __getAccounts(self, ids):
        accounts = []
        for elem, id in zip(self.account_type, ids):
            self.cur.execute(f"SELECT * FROM {elem} WHERE id = {id}")
            accounts.append(self.cur.fetchone())
        return accounts

    def getAccountById(self, id):
        self.cur.execute(
            f"SELECT * FROM Courant, Revolving, Epargne WHERE Courant.id = {id} OR Revolving.id = {id} OR Epargne.id = {id}"
        )

    def getUserAccounts(self, num):
        return self.getUserAccountsId(num)

    def updateSoldById(self, var, type):
        self.cur.execute(
            f"SELECT Courant, Revolving, Epargne FROM Appartenance WHERE id = {num}"
        )
        pass
