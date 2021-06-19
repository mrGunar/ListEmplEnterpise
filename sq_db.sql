CREATE TABLE if not exists person (
    id integer primary key AUTOINCREMENT,
    name text NOT NULL UNIQUE ,
    department_id integer,
    position_id integer
);


CREATE TABLE if not exists position (
    id integer primary key AUTOINCREMENT,
    title text NOT NULL UNIQUE
);

CREATE TABLE if not exists depart (
    id integer primary key AUTOINCREMENT,
    title text NOT NULL UNIQUE,
    parent integer NOT NUll
);