# 🚀 Django Backend with GraphQL API & PostgreSQL

This project is a **Django backend** with **GraphQL (Graphene)** and **PostgreSQL** database.  
It includes authentication, migrations, and API management for a scalable backend.

---

## 📂 Project Structure
backend/
│── myapp/ # Django app (models, schema, views)
│── myproject/ # Main Django project (settings, urls, wsgi)
│── manage.py # Django management script
│── requirements.txt # Python dependencies
│── README.md # Project guide (this file)
│── .gitignore # Git ignored files


---

## 🛠️ Setup Instructions

### 1️⃣ Prerequisites
Install the following before starting:
- [Python 3.8+](https://www.python.org/downloads/)
- [PostgreSQL 17+](https://www.postgresql.org/download/)
- Git

---

3️⃣ Create Virtual Environment
# Create venv
python -m venv venv

# Activate venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

4️⃣ Install Dependencies

Install everything needed for Django + GraphQL + PostgreSQL:

pip install django==5.2.5
pip install graphene-django==3.2.0
pip install django-cors-headers==4.3.1
pip install django-graphql-jwt==0.3.4
pip install psycopg2-binary==2.9.9
pip install requests==2.32.3
pip install Pillow==10.4.0
pip install djangorestframework==3.15.2


Export dependencies:
pip freeze > requirements.txt

5️⃣ PostgreSQL Setup
Open PostgreSQL bin folder in command prompt:

cd "C:\Program Files\PostgreSQL\17\bin"


Login as superuser:
psql -U postgres -h localhost -p 5432 -d postgres

Create database and user:

CREATE DATABASE mydb;
CREATE USER myuser WITH PASSWORD 'YourPasswordHere';
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;


Test login with new user:
psql -U myuser -h localhost -p 5432 -d mydb


6️⃣ Configure Django Database
Edit myproject/settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'YourPasswordHere',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

7️⃣ Run Migrations & Superuser
python manage.py migrate
python manage.py createsuperuser

8️⃣ Run Development Server
python manage.py runserver
Now open 👉 http://127.0.0.1:8000

✅ Summary

Python virtual environment created
Dependencies installed (Django, GraphQL, JWT, PostgreSQL driver)
PostgreSQL database & user created
Django connected to PostgreSQL
Migrations + superuser setup
Server runs locally on port 8000

👨‍💻 Author: Ritik Mehta
