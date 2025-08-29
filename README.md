# 🔍 INTERNSHIP APP BACKEND
*Django + GraphQL + PostgreSQL powered job portal backend*

<div align="center">
  <img src="https://img.shields.io/badge/Django-5.2+-092E20?style=for-the-badge&logo=django" alt="Django">
  <img src="https://img.shields.io/badge/GraphQL-API-E10098?style=for-the-badge&logo=graphql" alt="GraphQL">
  <img src="https://img.shields.io/badge/PostgreSQL-17-336791?style=for-the-badge&logo=postgresql" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python" alt="Python">
</div>

---

## 📂 Repository Files
| File | Description |
|------|-------------|
| `manage.py` | Django management script |
| `requirements.txt` | Python dependencies |
| `myproject/settings.py` | Django settings (PostgreSQL + GraphQL) |
| `myapp/schema.py` | GraphQL schema (queries & mutations) |
| `README.md` | Complete setup guide |

---

## 🚀 Quick Start

### 1️⃣ Clone & Setup Virtual Environment
```bash
git clone https://github.com/your-username/internship-app-backend.git
cd internship-app-backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

2️⃣ Install Dependencies
# If requirements.txt exists
pip install -r requirements.txt

3️⃣ Otherwise install manually
pip install Django==5.2.5
pip install graphene-django==3.2.0
pip install django-cors-headers==4.3.1
pip install django-graphql-jwt==0.3.4
pip install psycopg2-binary==2.9.9

# Save installed packages
pip freeze > requirements.txt

4️⃣ PostgreSQL Setup

Install PostgreSQL
Download from https://www.postgresql.org/download/
.
Default port → 5432

Open psql

cd "C:\Program Files\PostgreSQL\<version>\bin"
psql -U postgres -h localhost -p 5432 -d postgres


Create Database & User

CREATE DATABASE mydb;
CREATE USER myuser WITH PASSWORD 'YourPasswordHere';
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;


Reset Password (optional)

ALTER USER myuser WITH PASSWORD 'NewPassword123';


Connect as New User

psql -U myuser -h localhost -p 5432 -d mydb


Test with Sample Table

CREATE TABLE test_table (
   id SERIAL PRIMARY KEY,
   name VARCHAR(50),
   age INT
);
INSERT INTO test_table (name, age) VALUES ('Alice', 25), ('Bob', 30);
SELECT * FROM test_table;

5️⃣ Django Database Configuration

In backend/settings.py update:

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

6️⃣ Apply Migrations
# Run database migrations
python manage.py migrate

# Create superuser for Django admin
python manage.py createsuperuser
# Example:
# Username: admin
# Email: admin@example.com
# Password: ********

7️⃣ Run the Server
cd backend
venv\Scripts\activate
python manage.py runserver


Backend will be available at 👉 http://127.0.0.1:8000

✅ Done! Your Django + GraphQL + PostgreSQL backend is ready to use 🚀
