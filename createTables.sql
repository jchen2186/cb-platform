CREATE TABLE users (
    id serial NOT NULL PRIMARY KEY,
    firstname VARCHAR(100) not null,
    lastname VARCHAR(100) not null,
    email VARCHAR(120) not null unique,
    password_hash VARCHAR(100) not null,
    username VARCHAR(100) not null unique
    -- role int REFERENCES userroles(id)
);

CREATE TABLE userroles (
	id serial NOT NULL PRIMARY KEY,
	role_title VARCHAR(100) NOT NULL
);

CREATE TABLE chorusbattles (
	id serial NOT NULL PRIMARY KEY, 
	name VARCHAR(150) NOT NULL, 
	organizers integer NOT NULL, 
	entries integer NOT NULL
);

CREATE TABLE entries (
	id serial NOT NULL PRIMARY KEY
);
