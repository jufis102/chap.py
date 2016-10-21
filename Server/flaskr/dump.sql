PRAGMA foreign_keys=ON;
PRAGMA synchronous=OFF;

BEGIN TRANSACTION;
CREATE TABLE Corpus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    corpus TEXT
    );
CREATE TABLE Kette (
    kette TEXT PRIMARY KEY UNIQUE,
    probability INTEGER
    );
CREATE TABLE Entropy (
    wort TEXT PRIMARY KEY UNIQUE,
    entropy INTEGER
    );


COMMIT;
