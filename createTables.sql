CREATE TABLE userroles (
	id serial NOT NULL,
	role_title VARCHAR(100) NOT NULL,
	PRIMARY KEY (id)
);

INSERT INTO userroles(id, role_title) 
	VALUES  (1, 'Administrator'),
			(2, 'Unassigned'),
			(3, 'Judge'),
			(4, 'Singer'),
			(5, 'Artist'),
			(6, 'Mixer'),
			(7, 'Animator');

CREATE TABLE users (
    id serial NOT NULL,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(100) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    role_id INTEGER NOT NULL,
    user_icon BYTEA,
    PRIMARY KEY (id),
    CONSTRAINT users_role_id FOREIGN KEY(role_id) REFERENCES userroles(id)
);


CREATE TABLE chorusbattles (
	id serial NOT NULL PRIMARY KEY, 
	name VARCHAR(150) NOT NULL,
    description VARCHAR(500) NOT NULL,
    rules VARCHAR(500),
    prizes VARCHAR(500),
    video_link VARCHAR(150),
    start_date TIMESTAMP WITHOUT TIME ZONE,
    no_of_rounds INTEGER NOT NULL,
    creator_id INTEGER NOT NULL REFERENCES users(id)
);


CREATE TABLE entries (
	id SERIAL NOT NULL PRIMARY KEY,
	chorusbattle INTEGER NOT NULL REFERENCES chorusbattles(id), 
	team_id INTEGER NOT NULL REFERENCES teams(id),
	round_number INTEGER NOT NULL,
	title VARCHAR(100),
	description VARCHAR(500),
	submission_date TIMESTAMP WITH TIME ZONE,
	video_link VARCHAR(500)
);


CREATE TABLE orders(
	ord_no integer PRIMARY KEY,
	ord_date date,
	item_code integer REFERENCES items(item_code),
	item_grade character(1),
	ord_qty numeric,
	ord_amount numeric
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
