CREATE TABLE userroles (
	id serial NOT NULL,
	role_title VARCHAR(100) NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE users (
    id serial NOT NULL,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(100) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    role_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT users_role_id FOREIGN KEY(role_id) REFERENCES userroles(id)
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
	submission_date TIMESTAMP WITH TIME ZONE,
	chorusbattle INTEGER NOT NULL,
	PRIMARY KEY (id),
	CONSTRAINT chorusbattle_id FOREIGN KEY(chorusbattle) REFERENCES chorusbattles(id)
);

CREATE TABLE rounds (
	id serial NOT NULL,
	chorusbattle INTEGER NOT NULL,
	PRIMARY KEY (id),
	CONSTRAINT chorusbattle_id FOREIGN KEY(chorusbattle) REFERENCES chorusbattles(id)
);

CREATE TABLE teams (
	id serial NOT NULL,
	chorusbattle INTEGER NOT NULL,
	PRIMARY KEY (id),
	CONSTRAINT chorusbattle_id FOREIGN KEY(chorusbattle) REFERENCES chorusbattles(id)
);

CREATE TABLE judges (
	user_id INTEGER REFERENCES users(id),
	chorusbattle_id INTEGER REFERENCES chorusbattles(id),
	PRIMARY KEY (user_id, chorusbattle_id)
);

CREATE TABLE chorusbattle_entries (
	entry_id INTEGER REFERENCES entries(id),
	chorusbattle_id INTEGER REFERENCES chorusbattles(id),
	PRIMARY KEY (entry_id, chorusbattle_id)
);

CREATE TABLE user_teams (
	user_id INTEGER REFERENCES users(id),
	team_id INTEGER REFERENCES teams(id),
	PRIMARY KEY (user_id, team_id)
);




