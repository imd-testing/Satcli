# Satcli

Un projet de formation.

## Installation

Créer une fichier .env à la racine de répertoire, et définisez y un mot de passe.

example: 

```bash
# dans le fichier .env 

PGSQL_PASSWORD=<your_other_secret>
AIRFLOW_USER_LOGIN=<your_desired_username>
AIRFLOW_USER_PASSWORD=<your_desired_password>
```

## Liste des API steam

- Détails d'une application https://store.steampowered.com/api/appdetails?appids=730
- Liste des applications : https://api.steampowered.com/ISteamApps/GetAppList/v2/
- liste des commentaires sur une application : https://store.steampowered.com/appreviews/730?json=1


## Classement des jeux

- categories
- platforms
- genres
- metacritic
- developers
- publishers
- name
- is_free
- recommendations
- release_date
- required_age

Pour plus tard : 

- requirements

## Notes 

Il est possible de requeter les IDs au dessus de 100k.


