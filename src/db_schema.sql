BEGIN TRANSACTION;

CREATE TABLE Addresses (
    user VARCHAR (30) PRIMARY KEY UNIQUE ON CONFLICT REPLACE NOT NULL,
    address VARCHAR (160) NOT NULL
);

CREATE TABLE Gifts (
    sender VARCHAR (30) REFERENCES Addresses (user) NOT NULL UNIQUE,
    receiver VARCHAR (30) REFERENCES Addresses (user) NOT NULL UNIQUE,
    sent DATETIME,
    received DATETIME
);

COMMIT;
