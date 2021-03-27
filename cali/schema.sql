DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS branch;


CREATE TABLE branch(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	branch_name TEXT UNIQUE NOT NULL
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

-- Default values
INSERT INTO branch VALUES(0, 'Chihuahua');
INSERT INTO branch VALUES(1, 'Madera');

INSERT INTO user VALUES(0, 'Alex', '1234', 1, 1, 0);
INSERT INTO user VALUES(1, 'Ale', '1234', 0, 1, 0);
INSERT INTO user VALUES(2, 'Karla', '1234', 0, 1, 1);

