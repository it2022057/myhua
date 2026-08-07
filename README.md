# myhua application repository

`myhua` is a web application developed as part of a thesis project in Harokopio University of Athens titled: **«Σύστημα διαχείρισης πανεπιστημιακών οργάνων σε Python/Django»**.

The `myhua` project is an attempt to streamline the collective body operations of the University, it is implemented using **Python/Django** and is containerized with **Docker**.


## Requirements

You will need to install `docker`, `docker compose` and `git`

## Installation

Clone the repo using:
```
git clone https://github.com/it2022057/myhua.git
```
Then build the docker containers using:
```
cd myfaculty_pub2
docker compose pull
docker compose build
```
## Create the `.env` file

Use the `env.template` file to create your `.env` file using
```
cp env.template .env
```
Edit the .env file to reflect your data. You will need to obtain a RECAPTCHA v2 pair. For `AUTH_LDAP_BIND_DN` use your DN on the university LDAP server. For example if your username is `it048579` your DN should be set:
```
AUTH_LDAP_BIND_DN=it048579,ou=People,dc=hua,dc=gr
```
The `AUTH_LDAP_BIND_PASSWORD` should be set to the password you use to login to your university Gmail account.

## Initialize database and make migrations
You need to execute the migrations
```
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

## Create Django admin username
To create a superuser issue:
```
docker compose exec web python manage.py createsuperuser
```
You should now be able to access the django admin site at:
```
http://localhost:30100/admin
```

## Initial data
You can run a script to create some initial data 
```
docker compose exec web python manage.py runscript initial_data
```


## Compile messages
To run the multilingual site we also need to compile the messages:
```
docker compose exec web django-admin compilemessages
```
You should now be able to access the multilingual site at:
```
http://localhost:30100
```





