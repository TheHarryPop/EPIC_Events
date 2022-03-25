# EPIC Events

Cette API créée avec Django ORM permet aux équipes de vente et de support de gérer leurs clients, contrats et évènements

## Installation et lancement

```bash
$ git clone https://github.com/TheHarryPop/EPIC_Events.git
$ cd EPIC_Events
$ python3 -m venv env (Sous Windows => python -m venv env)
$ source env/bin/activate (Sous Windows => env\Scripts\activate)
$ pip install -r requirements.txt
$ python manage.py runserver
```

## Endpoints

Ci dessous une liste des endpoints disponibles. La documentation Postman les présente en détail.

http://127.0.0.1:8000/api/login/
http://127.0.0.1:8000/api/customers/
http://127.0.0.1:8000/api/customers/{{customer_id}}/
http://127.0.0.1:8000/api/contracts/
http://127.0.0.1:8000/api/contracts/{{contract_id}}/
http://127.0.0.1:8000/api/events/
http://127.0.0.1:8000/api/events/{{event_id}}/

## Filtres de recherche

Ci dessous la liste des filtres disponibles pour chaque URL.

Customers :
	http://127.0.0.1:8000/api/customers/ : 'surname', 'email'

Contracts :
	http://127.0.0.1:8000/api/contracts/ : 'customer__surname', 'customer__email', 'date_created', 'amount'

Events :
	http://127.0.0.1:8000/api/events/ : 'customer__surname', 'customer__email', 'event_date'

## Documentation

La documentation Postman est disponible à cette adresse :

https://documenter.getpostman.com/view/19052717/UVsTqNBU

## Base de données : PostgreSQL

- Créer une base de données sous PostgreSQL

- Dans le projet : EPIC_Events/EPIC_Events_app/settings.py :
	
	```bash
	DATABASES = {
    		'default': {
        		'ENGINE': 'django.db.backends.postgresql_psycopg2',
        		'NAME': '<database_name>',
        		'USER': '<database_user>',
        		'PASSWORD': '<database_user_password>',
        		'HOST': 'localhost',
        		'PORT': '',
    		}
	}
	```
	
	Remplacer :
		- <database_name> par le nom de la database créée
		- <database_user> par le nom de l'utilisateur de la database
		- <database_user_password> par le mot de passe de l'utilisateur de la database

	Puis dans le terminal :
		
		```bash
		$ py manage.py makemigrations
		$ py manage.py migrate
		```

## Création des profils utilisateurs
	
- Dans le terminal, créer un profil administrateur :

	```bash
	$ py manage.py createsuperuser
	```
	
- Puis lancer le serveur en local avec :
	
	```bash
	$ py manage.py runserver
	```

	- Ouvrir son navigateur et se rendre à l'adresse http://127.0.0.1:8000/. 
	- Se connecter avec le profil superuser créé précédemment.
	- Créer un nouvel utilisateur ayant pour rôle "Manager"
	- Ce nouveau profil manager sera ensuite en mesure de se connecter à la partie administration pour créer de nouveaux utilisateurs "seller" ou "support" qui pourront travailler sur les endpoints.

## Tests
	
Mesure de couverture du code par les tests (coverage) : 82%