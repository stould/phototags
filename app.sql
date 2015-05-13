CREATE TABLE fbuser(
	userid		 TEXT PRIMARY KEY NOT NULL,
	username     TEXT NOT NULL,
	status       INT NOT NULL,
	access_token TEXT NOT NULL
);

CREATE TABLE invite(
	id SERIAL NOT NULL PRIMARY KEY,
	username TEXT
);

	
