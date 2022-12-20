CREATE DATABASE IF NOT EXISTS steampowered;

CREATE TABLE IF NOT EXISTS steampowered.todo_list (
	id int unsigned,
	app_name varchar(2028) NOT NULL,
	last_import_details datetime NULL DEFAULT NULL,
	last_import_reviews datetime NULL DEFAULT NULL,
	PRIMARY KEY ( id )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS steampowered.controller_support (
	id int unsigned auto_increment,
	label varchar(2028),
	PRIMARY KEY ( id ),
	KEY ( label )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS steampowered.developers (
	id int unsigned auto_increment,
	label varchar(2028),
	PRIMARY KEY ( id ),
	KEY ( label )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS steampowered.publishers (
	id int unsigned auto_increment,
	label varchar(2028),
	PRIMARY KEY ( id ),
	KEY ( label )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS steampowered.categories (
	id int unsigned auto_increment,
	label varchar(2028),
	PRIMARY KEY ( id ),
	KEY ( label )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS steampowered.genres (
	id int unsigned auto_increment,
	label varchar(2028),
	PRIMARY KEY ( id ),
	KEY ( label )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS steampowered.applications (
	id int unsigned,
	id_controller_support int unsigned,

	app_name varchar(2028),
	required_age int unsigned,
	metacritic_score int unsigned,
	recommendations_count int unsigned,

	release_date date,

	is_available_on_windows tinyint unsigned,
	is_available_on_mac tinyint unsigned,
	is_available_on_linux tinyint unsigned,
	is_free tinyint unsigned,

	PRIMARY KEY ( id ),
	CONSTRAINT `fk_applications_controller_support` FOREIGN KEY (id_controller_support) REFERENCES controller_support (id) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS steampowered.app_2_developers (
	id int unsigned auto_increment,
	id_app int unsigned,
	id_developers int unsigned,
	PRIMARY KEY ( id ),
	CONSTRAINT `fk_a2d_applications` FOREIGN KEY (id_app) REFERENCES applications (id) ON DELETE RESTRICT ON UPDATE RESTRICT,
	CONSTRAINT `fk_a2d_developers` FOREIGN KEY (id_developers) REFERENCES developers (id) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS steampowered.app_2_publishers (
	id int unsigned auto_increment,
	id_app int unsigned,
	id_publishers int unsigned,
	PRIMARY KEY ( id ),
	CONSTRAINT `fk_a2p_applications` FOREIGN KEY (id_app) REFERENCES applications (id) ON DELETE RESTRICT ON UPDATE RESTRICT,
	CONSTRAINT `fk_a2p_publishers` FOREIGN KEY (id_publishers) REFERENCES publishers (id) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS steampowered.app_2_categories (
	id int unsigned auto_increment,
	id_app int unsigned,
	id_categories int unsigned,
	PRIMARY KEY ( id ),
	CONSTRAINT `fk_a2c_applications` FOREIGN KEY (id_app) REFERENCES applications (id) ON DELETE RESTRICT ON UPDATE RESTRICT,
	CONSTRAINT `fk_a2c_categories` FOREIGN KEY (id_categories) REFERENCES categories (id) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS steampowered.app_2_genres (
	id int unsigned auto_increment,
	id_app int unsigned,
	id_genres int unsigned,
	PRIMARY KEY ( id ),
	CONSTRAINT `fk_a2g_applications` FOREIGN KEY (id_app) REFERENCES applications (id) ON DELETE RESTRICT ON UPDATE RESTRICT,
	CONSTRAINT `fk_a2g_genres` FOREIGN KEY (id_genres) REFERENCES genres (id) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
