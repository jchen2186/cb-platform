CREATE TABLE users (
    id serial NOT NULL,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(100) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT users_role_id FOREIGN KEY(role) REFERENCES userroles(id)
);

CREATE TABLE userroles (
	id serial NOT NULL,
	role_title VARCHAR(100) NOT NULL,
	PRIMARY KEY (id),


);

CREATE TABLE chorusbattles (
	id serial NOT NULL, 
	name VARCHAR(150) NOT NULL, 
	organizers integer NOT NULL, 
	entries integer NOT NULL,
	PRIMARY KEY (id)

);

CREATE TABLE entries (
	id serial NOT NULL,
	submission_date TIMESTAMP,
	PRIMARY KEY (id)
	CONSTRAINT chorusbattle_id FOREIGN KEY(chorusbattle) REFERENCES chorusbattles(id)
);

CREATE TABLE rounds {
	id serial NOT NULL
	PRIMARY KEY (id)
	CONSTRAINT chorusbattle_id FOREIGN KEY(chorusbattle) REFERENCES chorusbattles(id)
}

CREATE TABLE teams (
	id serial NOT NULL
	PRIMARY KEY (id)
	CONSTRAINT chorusbattle_id FOREIGN KEY(chorusbattle) REFERENCES chorusbattles(id)
);



