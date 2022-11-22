CREATE DATABASE IF NOT EXISTS steampowered;

CREATE TABLE IF NOT EXISTS steampowered.todo_list (
	id int unsigned,
	app_name varchar(2028) NOT NULL,
	last_import_details datetime NULL DEFAULT NULL,
	last_import_reviews datetime NULL DEFAULT NULL,
	PRIMARY KEY ( id )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


