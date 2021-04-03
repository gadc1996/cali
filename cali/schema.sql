DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS branch;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS article;
DROP TABLE IF EXISTS client;

CREATE TABLE branch(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	branch_name TEXT UNIQUE NOT NULL
);

CREATE TABLE user(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password INTEGER NOT NULL,
	is_super  INTEGER NOT NULL,
	can_discount INTEGER NOT NULL,
	branch_id INTEGER NOT NULL,
	FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
); 

CREATE TABLE category(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	category_name TEXT NOT NULL
);

CREATE TABLE article( 
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE NOT NULL,
	category_id INTEGER NOT NULL,
	description TEXT,
	image_path TEXT,
	price REAL,
	SKU TEXT,
	stock INTEGER,
	on_branch_1 INTEGER,
	on_branch_2 INTEGER,
	is_regular INTEGER,
	FOREIGN KEY (category_id) REFERENCES category(id)
);

CREATE TABLE client(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE NOT NULL,
	contact_phone INTEGER,
	has_credit INTEGER
);
--Default values
INSERT INTO branch VALUES(0, 'Chihuahua');
INSERT INTO branch VALUES(1, 'Madera');

INSERT INTO user VALUES(0, 'Alex', 1234, 1, 1, 0);
INSERT INTO user VALUES(1, 'Ale', 1234, 0, 1, 0);
INSERT INTO user VALUES(2, 'Karla', 1234, 0, 1, 1);

INSERT INTO client VALUES(0, 'Rosa', 718293849, 1);
INSERT INTO client VALUES(1, 'Maria', 928471928, 0);
INSERT INTO client VALUES(2, 'Fernanda', 1728394718, 0);


