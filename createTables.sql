CREATE TABLE users (
    id serial PRIMARY KEY,
    firstname VARCHAR(100) not null,
    lastname VARCHAR(100) not null,
    email VARCHAR(120) not null unique,
    password_hash VARCHAR(100) not null,
    username VARCHAR(100) not null unique
    -- role int REFERENCES userroles(id)
);


-- CREATE TABLE userroles (
--     id serial PRIMARY KEY,
--     role_title VARCHAR(100) not null
-- );
