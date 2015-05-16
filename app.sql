CREATE TABLE fbuser(
	userid		 TEXT PRIMARY KEY NOT NULL,
	access_token TEXT NOT NULL
);

CREATE TABLE invite(
	id SERIAL NOT NULL PRIMARY KEY,
	username TEXT
);

	
