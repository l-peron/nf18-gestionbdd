CREATE TYPE ETAT_COMPTE AS ENUM('Ouvert', 'Bloqué', 'Fermé');
CREATE TYPE ETAT_OPERATION AS ENUM('Non Traitée', 'Traitée');

CREATE TABLE Clients (
	Telephone INT PRIMARY KEY,
	Nom VARCHAR(30) NOT NULL,
	Adresse VARCHAR(30) NOT NULL
);

CREATE TABLE ComptesCourant (
	Id INT PRIMARY KEY,
	DateCreation timestamp UNIQUE,
	Statut ETAT_COMPTE NOT NULL,
	MaxMois DECIMAL(12, 2) NOT NULL,
	MinMois DECIMAL(12, 2) NOT NULL CHECK (MinMois <= MaxMois),
    Solde DECIMAL(12, 2) NOT NULL CHECK (Solde >= DecouvertAutorise),
    DecouvertAutorise DECIMAL(12, 2) NOT NULL CHECK (DecouvertAutorise <= 0),
    DebutDecouvert timestamp
);

CREATE TABLE ComptesRevolving (
	Id INT PRIMARY KEY,
	DateCreation timestamp UNIQUE,
	Statut ETAT_COMPTE NOT NULL,
	TauxJournalier REAL NOT NULL,
	MontantNegocie DECIMAL(12, 2) NOT NULL CHECK (MontantNegocie < 0),
	Solde DECIMAL(12, 2) NOT NULL CHECK (Solde BETWEEN MontantNegocie AND 0)
);

CREATE TABLE ComptesEpargne (
	Id INT PRIMARY KEY,
	DateCreation timestamp UNIQUE,
	Statut ETAT_COMPTE NOT NULL,
	Interet REAL NOT NULL,
	Plafond DECIMAL(12, 2) NOT NULL CHECK (Plafond >= 300),
Solde  DECIMAL(12, 2) NOT NULL CHECK (Solde BETWEEN 300 AND Plafond)
);

CREATE FUNCTION IntersectionComptes()
RETURNS INT
LANGUAGE plpgsql
AS $$
BEGIN
	IF (SELECT COUNT(Id) FROM (SELECT Id FROM ComptesCourant INTERSECT SELECT Id FROM ComptesRevolving INTERSECT SELECT Id FROM ComptesEpargne) S) THEN RETURN 1; END IF;
	RETURN 0;
END $$;
ALTER TABLE ComptesCourant ADD CONSTRAINT Ck_Intersection CHECK (IntersectionComptes() = 0);
ALTER TABLE ComptesRevolving ADD CONSTRAINT Ck_Intersection CHECK (IntersectionComptes() = 0);
ALTER TABLE ComptesEpargne ADD CONSTRAINT Ck_Intersection CHECK (IntersectionComptes() = 0);

CREATE TABLE Appartenance (
	Client INT REFERENCES Clients(Telephone) NOT NULL,
	Courant INT REFERENCES ComptesCourant(Id),
	Revolving INT REFERENCES ComptesRevolving(Id),
	Epargne INT REFERENCES ComptesEpargne(Id),
	PRIMARY KEY (Client, Courant, Revolving, Epargne),
	CHECK ((Courant IS NOT NULL AND Revolving IS NULL and Epargne IS NULL) OR (Courant IS NULL AND Revolving IS NOT NULL and Epargne IS NULL) OR (Courant IS NULL AND Revolving IS NULL and Epargne IS NOT NULL))
);

CREATE TABLE OperationsVirement (
	Id INT PRIMARY KEY,
	Courant INT REFERENCES ComptesCourant(Id),
	Revolving INT REFERENCES ComptesRevolving(Id),
	Epargne INT REFERENCES ComptesEpargne(Id),
	Client INT REFERENCES Clients(Telephone),
	Montant DECIMAL(12, 2) NOT NULL,
	Date DATE NOT NULL,
	Etat ETAT_OPERATION NOT NULL,
	UNIQUE (Date, Courant, Revolving, Epargne),
	CHECK ((Courant IS NOT NULL AND Revolving IS NULL and Epargne IS NULL)
OR (Courant IS NULL AND Revolving IS NOT NULL and Epargne IS NULL) OR (Courant IS NULL AND Revolving IS NULL and Epargne IS NOT NULL))
);

CREATE TABLE OperationsGuichet (
	Id INT PRIMARY KEY,
	Courant INT REFERENCES ComptesCourant(Id),
	Revolving INT REFERENCES ComptesRevolving(Id),
	Epargne INT REFERENCES ComptesEpargne(Id),
	Client INT REFERENCES Clients(Telephone),
	Montant DECIMAL(12, 2) NOT NULL,
	Date DATE NOT NULL,
	Etat ETAT_OPERATION NOT NULL,
	UNIQUE (Date, Courant, Revolving, Epargne),
	CHECK ((Courant IS NOT NULL AND Revolving IS NULL and Epargne IS NULL) OR (Courant IS NULL AND Revolving IS NOT NULL and Epargne IS NULL) OR (Courant IS NULL AND Revolving IS NULL and Epargne IS NOT NULL))
);

CREATE TABLE OperationsCarteBleue (
	Id INT PRIMARY KEY,
	Courant INT REFERENCES ComptesCourant(Id),
	Revolving INT REFERENCES ComptesRevolving(Id),
	Client INT REFERENCES Clients(Telephone),
	Montant DECIMAL(12, 2) NOT NULL,
	Date DATE NOT NULL,
	Etat ETAT_OPERATION NOT NULL,
	UNIQUE (Date, Courant, Revolving),
	CHECK ((Courant IS NOT NULL AND Revolving IS NULL)
		OR (Courant IS NULL AND Revolving IS NOT NULL))
);

CREATE TABLE OperationsCheque (
	Id INT PRIMARY KEY,
	Courant INT REFERENCES ComptesCourant(Id),
	Revolving INT REFERENCES ComptesRevolving(Id),
	Client INT REFERENCES Clients(Telephone),
	Montant DECIMAL(12, 2) NOT NULL,
	Date DATE NOT NULL,
	Etat ETAT_OPERATION NOT NULL,
	UNIQUE (Date, Courant, Revolving),
	CHECK ((Courant IS NOT NULL AND Revolving IS NULL)
OR (Courant IS NULL AND Revolving IS NOT NULL))
);

CREATE FUNCTION IntersectionOperations()
RETURNS INT
LANGUAGE plpgsql
AS $$
BEGIN
	IF (SELECT COUNT(Id) FROM (SELECT Id FROM OperationsVirement INTERSECT SELECT Id FROM OperationsGuichet INTERSECT SELECT Id FROM OperationsCarteBleue INTERSECT SELECT Id FROM OperationsCheque) S) THEN RETURN 1; END IF;
	RETURN 0;
END $$;
ALTER TABLE OperationsVirement ADD CONSTRAINT Ck_Intersection CHECK (IntersectionOperations(Id) = 0);
ALTER TABLE OperationsGuichet ADD CONSTRAINT Ck_Intersection CHECK (IntersectionOperations(Id) = 0);
ALTER TABLE OperationsCarteBleue ADD CONSTRAINT Ck_Intersection CHECK (IntersectionOperations(Id) = 0);
ALTER TABLE OperationsCheque ADD CONSTRAINT Ck_Intersection CHECK (IntersectionOperations(Id) = 0);

CREATE FUNCTION EtatCompte(T VARCHAR(25), Compte INT, Montant DECIMAL(12, 2))
RETURNS INT
LANGUAGE plpgsql
AS $$
BEGIN
	IF (Compte IS NULL) THEN RETURN 2; END IF;
	IF (SELECT CASE T
		WHEN 'Courant' THEN (Compte IN (SELECT Id FROM ComptesCourant WHERE (Statut='Ouvert')))
		WHEN 'Revolving' THEN (Compte IN (SELECT Id FROM ComptesRevolving WHERE (Statut='Ouvert')))
		WHEN 'Epargne' THEN (Compte IN (SELECT Id FROM ComptesEpargne WHERE (Statut='Ouvert')))
	END) THEN RETURN 2; END IF;
	IF (SELECT CASE T
		WHEN 'Courant' THEN (Compte IN (SELECT Id FROM ComptesCourant WHERE (Statut='Bloqué')))
		WHEN 'Revolving' THEN (Compte IN (SELECT Id FROM ComptesRevolving WHERE (Statut='Bloqué')))
		WHEN 'Epargne' THEN (Compte IN (SELECT Id FROM ComptesEpargne WHERE (Statut='Bloqué')))
	END) THEN
		IF (Montant > 0) THEN RETURN 2; END IF;
		RETURN 1;
	END IF;
	RETURN 0;
END $$;
ALTER TABLE OperationsVirement ADD CONSTRAINT Ck_Comptes CHECK (EtatCompte('Courant', Courant, Montant) = 2 AND EtatCompte('Revolving', Revolving, Montant) = 2 AND EtatCompte('Epargne', Epargne, Montant) = 2 OR Etat='Non Traitée');
ALTER TABLE OperationsGuichet ADD CONSTRAINT Ck_Comptes CHECK (EtatCompte('Courant', Courant, Montant) >= 1 AND EtatCompte('Revolving', Revolving, Montant) >= 1 AND EtatCompte('Epargne', Epargne, Montant) >= 1 OR Etat='Non Traitée');
ALTER TABLE OperationsCarteBleue ADD CONSTRAINT Ck_Comptes CHECK (EtatCompte('Courant', Courant, Montant) = 2 AND EtatCompte('Revolving', Revolving, Montant) = 2 OR Etat='Non Traitée');
ALTER TABLE OperationsCheque ADD CONSTRAINT Ck_Comptes CHECK (EtatCompte('Courant', Courant, Montant) = 2 AND EtatCompte('Revolving', Revolving, Montant) = 2 OR Etat='Non Traitée');

CREATE OR REPLACE FUNCTION set_datedecouvert()
RETURNS TRIGGER as $set_dd$
	BEGIN
		UPDATE comptescourant SET datedecouvert = current_timestamp WHERE solde < 0;
		UPDATE comptescourant SET datedecouvert = NULL WHERE solde >= 0;
	END;
$set_dd$ LANGUAGE plpgsql;
CREATE TRIGGER decouvert_courant AFTER UPDATE OF solde ON comptescourant FOR EACH ROW EXECUTE FUNCTION set_datedecouvert();

CREATE OR REPLACE FUNCTION set_minmax_courant()
RETURNS TRIGGER as $set_dd$
	BEGIN
		UPDATE comptescourant SET maxmois = solde WHERE solde > maxmois;
		UPDATE comptescourant SET minmois = solde WHERE solde < minmois;
		RETURN NEW;
	END;
$set_dd$ LANGUAGE plpgsql;

CREATE TRIGGER update_minmax_courant AFTER UPDATE OF solde ON comptescourant FOR EACH ROW EXECUTE FUNCTION set_minmax_courant();
