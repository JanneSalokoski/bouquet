DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS quests;
DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS types;
DROP TABLE IF EXISTS sessions;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE quests (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  diet TEXT NOT NULL,
  participating BOOL NOT NULL DEFAULT FALSE,
  responded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  edited TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  grp_id INT NOT NULL,
  type_id INT NOT NULL,

  FOREIGN KEY (grp_id) REFERENCES groups (id),
  FOREIGN KEY (type_id) REFERENCES types (id)
);

CREATE TABLE groups (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  passkey TEXT NOT NULL
);

CREATE TABLE types (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);

CREATE TABLE sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,

  FOREIGN KEY (user_id) REFERENCES users (id)
);

INSERT INTO groups (
  name, passkey
) VALUES ( "hääpari", "testi" );

INSERT INTO types (
  name
) VALUES ( "sukulaiset" );

INSERT INTO quests (
  name, email, diet, grp_id, type_id
) VALUES ( "Janne", "janne.salokoski@helsinki.fi", "Laktoositon", 1, 1 );
