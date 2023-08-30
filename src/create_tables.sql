-- Primary Keys can't be empty of duplicated
CREATE TABLE IF NOT EXISTS monsters(
	monster_id  VARCHAR(50) PRIMARY KEY, 
	name VARCHAR(50),
	size VARCHAR(50),
	type VARCHAR(50),
	alignment VARCHAR(50),
	natural_ac INT,
	speed_walk DECIMAL(5,2),
	speed_swim DECIMAL(5,2),
	speed_fly DECIMAL(5,2),
	speed_burrow DECIMAL(5,2),
	strength int,
	dexterity int,
	constitution int,
	intelligence int,
	wisdom int,
	charisma int,
	challenge_rating DECIMAL(4,2),
	xp INT,
	image VARCHAR(100),
	descrip VARCHAR(750)
);


CREATE TABLE IF NOT EXISTS monster_resists(
	monster_id  VARCHAR(50), 
	type VARCHAR(50),
	value VARCHAR(50),
	FOREIGN KEY(monster_id) REFERENCES monsters (monster_id)
);



