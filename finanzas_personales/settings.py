# finanzas_personales/settings.py

import os
from pathlib import Path
import dj_database_url # Para leer la URL de la base de datos
from dotenv import load_dotenv # Para cargar variables de entorno desde .env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno del archivo .env
# Esto buscará un archivo .env en el directorio raíz del proyecto (BASE_DIR)
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)
# 
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Es buena práctica también mover SECRET_KEY a variables de entorno para producción.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'una-clave-secreta-por-defecto-para-desarrollo-si-no-esta-en-env')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True' # Lee DEBUG desde .env, por defecto True

ALLOWED_HOSTS_str = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_str.split(',') if host.strip()]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gestion', # Nuestra aplicación de finanzas
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'finanzas_personales.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Aquí añadimos la ruta a nuestra carpeta 'templates' principal
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True, # Esto permite que Django busque plantillas dentro de las apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'finanzas_personales.wsgi.application'


# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases

# Configuración para usar Supabase (PostgreSQL)
# La URL de la base de datos se carga desde la variable de entorno DATABASE_URL
# que a su vez se carga desde el archivo .env
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600, # Segundos que las conexiones pueden permanecer abiertas
            conn_health_checks=True, # Habilita chequeos de salud para las conexiones (Django 4.1+)
        )
    }
else:
    # Configuración de respaldo a SQLite si DATABASE_URL no está definida
    # (útil para entornos donde .env no esté disponible o para pruebas rápidas)
    print("ADVERTENCIA: DATABASE_URL no encontrada. Usando SQLite como base de datos de respaldo.")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = 'es-mx' # Español de México

TIME_ZONE = 'America/Mexico_City' # Zona horaria

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

STATIC_URL = 'static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles' # Descomentar para producción al recolectar estáticos

# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
