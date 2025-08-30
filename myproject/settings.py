import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
import dj_database_url  # Added for Render

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------- SECURITY ----------------
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key-for-development-only')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "internshipapp-backend.onrender.com",
]

# Add Render domain dynamically
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# ---------------- APPS ----------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'corsheaders',
    'graphene_django',

    # Local
    'myapp',
]

# ---------------- MIDDLEWARE ----------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # must be first
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # for static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# ---------------- DATABASE ----------------
# Use Render's DATABASE_URL if available, else local PostgreSQL
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=not DEBUG
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ---------------- AUTH ----------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------- INTERNATIONALIZATION ----------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------- STATIC & MEDIA ----------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# WhiteNoise configuration
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------- CORS ----------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",   # React Vite dev
    "http://127.0.0.1:5173",
    "http://localhost:3000",   # React CRA dev
    "http://127.0.0.1:3000",
    "http://localhost:8000",   # Django dev
    "http://127.0.0.1:8000",
    "https://*.vercel.app",    # Vercel deployment
    "https://internshipapp-backend.onrender.com",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = DEBUG  # allow all in dev

CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    'x-requested-with',
    'x-csrftoken',
    'accept',
    'origin',
    'cache-control',
]

# ---------------- CSRF ----------------
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://*.vercel.app",
    "https://internshipapp-backend.onrender.com",
]

if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

# ---------------- GRAPHQL ----------------
GRAPHENE = {
    'SCHEMA': 'myproject.schema.schema',  # Changed to project-level schema
}

# ---------------- PRODUCTION SETTINGS ----------------
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# TEMPORARY CSRF RELAXATION FOR TESTING
if not DEBUG:
    # Allow all origins temporarily for testing
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True

# ---------------- LOGGING ----------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# ---------------- AUTO SUPERUSER CREATION ----------------
# Add this at the very bottom of the file (after all other settings)
import os
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError

def create_superuser_if_missing():
    """
    Automatically create superuser if environment variables are set
    and user doesn't already exist. This runs every time the app starts.
    """
    try:
        User = get_user_model()
        superuser_username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        superuser_email = os.environ.get('DJANGO_SUPERUSER_EMAIL') 
        superuser_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        
        # Check if all environment variables are set
        if all([superuser_username, superuser_email, superuser_password]):
            # Check if user already exists
            if not User.objects.filter(username=superuser_username).exists():
                User.objects.create_superuser(
                    username=superuser_username,
                    email=superuser_email,
                    password=superuser_password
                )
                print(f"✅ Superuser '{superuser_username}' created successfully!")
            else:
                print(f"ℹ️ Superuser '{superuser_username}' already exists.")
        else:
            print("ℹ️ Superuser environment variables not set. Skipping auto-creation.")
            
    except OperationalError:
        # Database might not be ready/migrated yet
        print("⏳ Database not ready for superuser creation yet.")
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")

# Run the function when settings are loaded
create_superuser_if_missing()