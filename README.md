# 🚀 myhua application repository

## ℹ️ About

`myhua` is a web application developed as part of an undergraduate thesis project for the [Harokopio University of Athens](https://www.hua.gr/), titled: **«Σύστημα διαχείρισης πανεπιστημιακών οργάνων σε Python/Django»**.

The `myhua` project is an attempt to streamline the collective body operations of the University. Ιt is implemented using **Python/Django** and is containerized with **Docker**.

## ⚙️ Requirements

You need to have `docker`, `docker compose` and `git` installed in your system. For Ubuntu check out:

- https://docs.docker.com/engine/install/ubuntu/
- https://docs.docker.com/compose/install/
- https://docs.gitlab.com/topics/git/how_to_install_git/?tab=Ubuntu+Linux

### ⚠️ IMPORTANT
You also need to be connected to the [University's VPN](https://www.hua.gr/portal/vpn/) in order for the Django container to be able to access the openldap directory. Otherwise authentication will not work, at least out-of-the-box.


## 📚 Project Docs

- ⚙️ [Main Guide](./README.md)
- 🧰 [Django Migrations Guide](./MIGRATIONS.readme)

## 🌱 Project Overview

This project is a Django-based web application for managing university collective bodies and all related actions concerning them. The application is organized into multiple Django apps, each responsible for a specific part of the system:

- **`accounts:`** User authentication, user profiles and role management
- **`api:`** API endpoints
- **`attachments:`** File attachment management
- **`bodies:`** Management of university collective bodies
- **`bodyapplications:`** Management of applications submitted to collective bodies
- **`core:`** Shared functionality used across multiple apps to avoid code duplication
- **`curricula:`** Management of academic curricula
- **`hua_cbms:`** Main Django project configuration and settings
- **`locale:`** Application translation and localization files
- **`mailer:`** Email handling and notification functionality
- **`meetings:`** Management of collective body meetings
- **`scopes:`** User access scopes and permission-related functionality
- **`scripts:`** Scripts for loading initial data
- **`static:`** Static files such as .css, .js, and images
- **`subjects:`** Management of subjects, decisions, subject types and categories

## 📁 Project Structure

```bash
myhua/
├── code/                      # Django application source code
│   └── hua_cbms/                       
│       ├── accounts/                   
│       ├── api/                        
│       ├── attachments/                
│       ├── bodies/                     
│       ├── bodyapplications/           
│       ├── core/                       
│       ├── curricula/                  
│       ├── hua_cbms/                  
│       ├── locale/                     
│       ├── mailer/                     
│       ├── meetings/                   
│       ├── scopes/                    
│       ├── scripts/                    
│       ├── static/                     
│       ├── subjects/                   
│       └── manage.py                   
│
├── nginx/                     # NGINX configuration file
│
├── docker-compose.yaml        # Defines images and runs all components via Docker Compose for local/development deployment
├── docker-compose-prod.yaml   # Docker Compose configuration for production deployment using Gunicorn WSGI server
├── Dockerfile		           # Custom Dockerfile for the application (installs required dependencies and copies the code directory)
│
├── .dockerignore              # Docker exclusions
├── .gitignore                 # Git exclusions
├── .env.template              # Template for required environment variables
├── requirements.txt		   # Python dependencies required by the application
│
├── rm-migrations.sh           # Script for removing Django migration files
├── MIGRATIONS.readme          # Ιnstructions for managing Django migrations and backing up data
│
└── README.md                  # Project documentation

```

## 🏗️ Architecture

The main services are:

- **`web:`** Django application
  - Uses Django's development server in the local/development environment
  - Uses Gunicorn in production
- **`db:`** PostgreSQL 17
- **`redis:`** Redis 7
- **`worker:`** Celery worker for asynchronous background tasks (notify in mailer app)
- **`nginx:`** Reverse proxy used in the production environment for serving static and media files

## 🗃️ Installation

Since this is a **private repository**, you must first have access to it as a collaborator.

You can clone the repository using either **SSH** or **HTTPS**.

### 🔑 Option 1 — SSH (Recommended)

If you have an SSH key configured with your GitHub account, clone the repository using:

```
git clone git@github.com:it2022057/myhua.git
```

> ⚠️ Make sure your public SSH key has been added to your GitHub account before cloning the repository.

### 🎟️ Option 2 — HTTPS

Alternatively, clone the repository using HTTPS:

```
git clone https://github.com/it2022057/myhua.git
```

When prompted for authentication, use:

- **Username:** Your GitHub username
- **Password:** Your GitHub Personal Access Token (PAT)

> ⚠️ GitHub account passwords cannot be used for Git operations over HTTPS. You must use a **Personal Access Token (PAT)** instead.

> 💡 Each collaborator should authenticate using their **own GitHub account and credentials**. Never share Personal Access Tokens or private SSH keys.

### ➡️ Move into the cloned repository's root directory

```
cd myhua
```

### 📂 Where does the code live?

The code lives in the `code/` folder of the root directory. This is volume-mounted in the `web` container and it already contains a Django project named `hua_cbms`.

### 💾 Data persistence

The folder `data/` is volume-mounted to the `postgres` container to enable database persistence when the container is stopped.


## 🔧 Create the `.env` file

Use the `env.template` file to create your `.env` file using

```
cp env.template .env
```

Edit the `.env` file to reflect your data. You will need to obtain a **RECAPTCHA v2 pair**. For `AUTH_LDAP_BIND_DN` use your DN on the **University's LDAP server**. For example if your username is `it048579` your DN should be set:

```
AUTH_LDAP_BIND_DN=it048579,ou=People,dc=hua,dc=gr
```

The `AUTH_LDAP_BIND_PASSWORD` should be set to the password you use to login to your university Gmail account. The Django app needs these *credentials* to carry out user searches at the **University's LDAP server**. Remember to stay connected at the University's **VPN service** for the searches to work properly!

## 🐳 Docker Deployment (Development Environment)

The development environment is defined in: **`docker-compose.yaml`**

Build the docker containers using:

```
docker compose pull
docker compose build
```

Run the docker containers:

```
docker compose up
```

View running containers:

```
docker compose ps
```

View logs:

```
docker compose logs -f
```

Stop the environment:

```
docker compose down
```

### 📦 Docker containers

- **`db`** is a standard PostgreSQL container pulled from the official Docker image. 

- **`web`** is built from the `Dockerfile` included in the root folder and it is the main Django application container that runs using:

  ```yaml
  python manage.py runserver 0.0.0.0:8000
  ```

  Docker maps the container's port `8000` to port `30100` on the host.

  ```yaml
  ports:
    - "30100:8000"
  ```

- **`redis`** is a standard Redis container that can be built from the official Docker archives. 

  Redis is used as the message broker for Celery and is available internally to the other containers at:

  ```yaml
  redis://redis:6379/0
  ```

- **`worker`** is built from the same `Dockerfile` as the web container and runs a Celery worker for asynchronous and background tasks.

  ```yaml
  celery -A hua_cbms worker --loglevel=INFO
  ```

### 🛠️ Initialize database and make migrations

You need to execute the migrations

```
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

### 👤 Create Django admin username

To create a superuser issue:

```
docker compose exec web python manage.py createsuperuser
```

### 🗄️ Initial data

You can run scripts to create some initial data.

```
docker compose exec web python manage.py runscript initial_data
docker compose exec web python manage.py runscript initial_data2
```

### 🌐 Compile messages

To run the multilingual site we also need to compile the messages:

```
docker compose exec web django-admin compilemessages
```

You should now be able to access the multilingual site.

## 🖥️ Docker Deployment (Production Environment)

The production environment is defined in: **`docker-compose-prod.yaml`**

Build the docker containers using:

```
docker compose -f docker-compose-prod.yaml pull
docker compose -f docker-compose-prod.yaml build
```

Run the docker containers:

```
docker compose -f docker-compose-prod.yaml up
```

View running containers:

```
docker compose -f docker-compose-prod.yaml ps
```

View logs:

```
docker compose -f docker-compose-prod.yaml logs -f
```

Stop the production environment:

```
docker compose -f docker-compose-prod.yaml down
```

### 📦 Docker containers

- **`web`** is built from the `Dockerfile` included in the root folder and runs the main Django application using **Gunicorn**.

  ```yaml
  gunicorn --workers=8 --bind=0.0.0.0:8000 hua_cbms.wsgi:application
  ```

  The container is not exposed directly to the host. Requests are forwarded to it through **NGINX**.

- **`nginx`** is a standard NGINX container that can be built from the official Docker archives and used as a *reverse proxy* in production. It also serves the application's **static** and **media** files directly.

  It exposes port `30100` on the host.

  ```yaml
  ports:
    - "30100:30100"
  ```

### 🛠️ Initialize database and make migrations

You need to execute the migrations

```
docker compose -f docker-compose-prod.yaml exec web python manage.py makemigrations
docker compose -f docker-compose-prod.yaml exec web python manage.py migrate
```

### 👤 Create Django admin username

To create a superuser issue:

```
docker compose -f docker-compose-prod.yaml exec web python manage.py createsuperuser
```

### 🗄️ Initial data

You can run scripts to create some initial data.

```
docker compose -f docker-compose-prod.yaml exec web python manage.py runscript initial_data
docker compose -f docker-compose-prod.yaml exec web python manage.py runscript initial_data2
```

### 🌐 Compile messages

To run the multilingual site we also need to compile the messages:

```
docker compose -f docker-compose-prod.yaml exec web django-admin compilemessages
```

You should now be able to access the multilingual site.

## 🔗 Application site URL 

The Django site is accessible though http at: 

```
http://localhost:30100
```

## 🔐 Admin site URL

The Django admin site is accessible though http at:

```
http://localhost:30100/admin
```

## 📬 Contact

For questions or issues, feel free to reach out at: 

📧 it2022057@hua.gr

## ✍️ Author

Made with ❤️ by **it2022057**
