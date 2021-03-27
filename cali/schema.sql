DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS branch;


CREATE TABLE branch(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE NOT NULL
);

CREATE TABLE user(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL,
	is_super  INTEGER NOT NULL,
	can_discount BIT NOT NULL,
	branch_id BIT NOT NULL,
	FOREIGN KEY (branch_id) REFERENCES branch(branch_id)
); 

INSERT INTO branch VALUES(0, 'Chihuahua');
INSERT INTO branch VALUES(1, 'Madera');
