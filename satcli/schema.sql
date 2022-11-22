CREATE DATABASE IF NOT EXISTS steampowered;

CREATE TABLE IF NOT EXISTS steampowered.todo_list (
	id int unsigned,
	app_name varchar(2028),
	last_import datetime,
	PRIMARY KEY ( id )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

