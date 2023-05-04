#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER steampowered PASSWORD '$STEAMPOWERED_PG_PASSWORD';
	CREATE USER airflow PASSWORD '$AIRFLOW_PG_PASSWORD';
	
	CREATE DATABASE steampowered WITH OWNER "steampowered" ENCODING 'utf8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';
	GRANT ALL PRIVILEGES ON DATABASE steampowered TO steampowered;
	
	CREATE DATABASE airflow WITH OWNER "airflow" ENCODING 'utf8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';
	GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;
EOSQL
