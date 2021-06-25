PRAGMA foreign_keys = ON;

-- -- the table exists?

-- DROP tables if already existing
DROP TABLE IF EXISTS credential;
DROP TABLE IF EXISTS logotype;

-- -- if it does not exists, do:

CREATE TABLE IF NOT EXISTS credential (
    Id INTEGER UNIQUE,
    login TEXT DEFAULT '',
    password TEXT DEFAULT '',
    PRIMARY KEY('Id')
);

CREATE TABLE IF NOT EXISTS logotype (
    Id INTEGER UNIQUE,
    image BLOB NOT NULL,
    PRIMARY KEY('Id')
);

-- -- Populate initial data


-- -- Initialize the used passwords

INSERT INTO credential (Id, Login, Password) values (1,'Admin','1234');
INSERT INTO credential (Id, Login, Password) values (2,'Supervisor','951951');

-- -- Initialize the default logotype

-- INSERT INTO logotype VALUES (1,/cycleapp.png);
-- INSERT INTO logotype (Id,image) VALUES (1,?);