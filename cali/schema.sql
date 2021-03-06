DROP TABLE IF EXISTS article;
DROP TABLE IF EXISTS cart;
DROP TABLE IF EXISTS sale;
DROP TABLE IF EXISTS credit;
DROP TABLE IF EXISTS client;
DROP TABLE IF EXISTS pay_method;

CREATE TABLE article( 
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT  NOT NULL,
	category_id INTEGER NOT NULL,
	description TEXT,
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

CREATE TABLE cart(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT  NOT NULL,
	price REAL,
	SKU TEXT,
	stock INTEGER,
	on_branch_1 INTEGER,
	on_branch_2 INTEGER,
	is_regular INTEGER
);

CREATE TABLE sale(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER,
	branch_id INTEGER,
	client_id INTEGER,
	total INTEGER,
	pay_method_id INTEGER,
	date TEXT,
	FOREIGN KEY (user_id) REFERENCES user(id),
	FOREIGN KEY (client_id) REFERENCES client(id),
	FOREIGN KEY (pay_method_id) REFERENCES pay_method(id)
);

CREATE TABLE credit(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER,
	branch_id INTEGER,
	client_id INTEGER,
	total INTEGER,
	pay_method_id INTEGER,
	date TEXT,
	payed INTEGER,
	credit_time INTEGER,
	FOREIGN KEY (user_id) REFERENCES user(id),
	FOREIGN KEY (branch_id) REFERENCES branch(id),
	FOREIGN KEY (client_id) REFERENCES client(id),
	FOREIGN KEY (pay_method_id) REFERENCES pay_method(id)
);

CREATE TABLE pay_method(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT
);
--Default values
INSERT INTO client VALUES(0, 'Rosa', 718293849, 1);
INSERT INTO client VALUES(1, 'Maria', 928471928, 0);
INSERT INTO client VALUES(2, 'Fernanda', 1728394718, 0);

INSERT INTO article VALUES(0, 'Vestido Negro', 0, 'Vestido Negro sencillo',  100, "1", 3, 2, 1, 1);
INSERT INTO article VALUES(1, 'Vestido flamingo', 0, 'Vestido con dibujos de flamingos',  100, "2", 3, 2, 1, 1);
INSERT INTO article VALUES(2, 'Falda Negra', 1, 'Falda Negra sencilla',  100, "3", 3, 2, 1, 1);
INSERT INTO article VALUES(3, 'Falda Verde', 1, 'Falda Verde sencilla',  100, "4", 3, 2, 1, 1);
INSERT INTO article VALUES(4, 'Vestido Azul', 0, 'Vestido con falda azul',  100, "5", 3, 2, 1, 1);
INSERT INTO article VALUES(5, 'Vestido Blanco', 0, 'Vestido blanco con mono',  100, "6", 3, 2, 1, 1);

INSERT INTO pay_method VALUES(0, 'Cash');
INSERT INTO pay_method VALUES(1, 'Card');
