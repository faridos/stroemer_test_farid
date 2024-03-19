# Project README

## Installation

To run and install everything, follow these steps:

A. Run migrations and fetch data manually:

```bash
docker-compose run --rm app python manage.py makemigrations
docker-compose run --rm app python manage.py migrate
docker-compose run --rm app python manage.py fetch_posts_comments # Manually fetch data
docker-compose run --rm app python manage.py test blog --debug-mode --force-color  --traceback  # for tests
```

B. Start the server:

```bash
docker-compose up -d
```

This command ensures that the code passes `flake8` linting, performs migrations, and then spins up the server. The server runs with the following command:

```bash
command: sh -c "flake8 --ignore=E501 . &&
    python manage.py makemigrations &&
    python manage.py migrate &&
    python manage.py runserver 0.0.0.0:8000"
```

## API Documentation

Access API documentation through the following URLs:

- Swagger: [http://localhost:8000/api/v1/swagger/](http://localhost:8000/api/v1/swagger/)
- Redoc: [http://localhost:8000/api/v1/redoc/](http://localhost:8000/api/v1/redoc/)

API specifications are defined in `stroemer_test_farid/posts-api.yml` in the root directory.

## Authentication

For authentication:

A. FakeUser class is used since no user model implementation is required. The default authentication class from `rest_framework` is customized to return `FakeUser`. `DEFAULT_AUTHENTICATION_CLASSES` setting is modified to use this custom class.

B. Endpoints:
   - Token Generation: [http://localhost:8000/api/v1/mytoken/](http://localhost:8000/api/v1/mytoken/)
   - Refresh Token: [http://localhost:8000/api/v1/mytoken/refresh/](http://localhost:8000/api/v1/mytoken/refresh/)

## Docker and Docker-compose

1. Dockerfile is configured to work with a non-root user for better security.
2. Docker-compose contains services for:
   - Django app
   - PostgreSQL server
   - Celery
   - Celery beat
   - RabbitMQ
3. Purpose:
   - The setup is for scheduling tasks to run heavy tasks asynchronously and concurrently.
   - Asyncio and aiohttp libraries are used for better performance and support for async programming.
   - Celerybeat is configured to run daily tasks, such as syncing remote data with the local database using Django commands.

## Synchronization Local Master -> Master

- CRUD endpoints send data to Celery.
- Celery tasks handle data and perform actions accordingly, including sending requests to the remote server.
- Asyncio is utilized for better performance.

## Unit Tests

- Includes unit tests for views, models, serializers, commands, and integration tests.
- Coverage is installed to check code coverage.

## Sensitive Data

- Sensitive data should not be pushed and should be added to `.gitignore`.
- Environment variables are stored in `.env.dev` file.

## Takeaways

1. `.env.data` file is shared via email.
2. Celery setup can be troublesome; encountered issues like "connection to server failed" which may not be fully resolved.
3. Docker-compose file is for development and not production-ready. Additional setup like NGINX or Traefik combined with Gunicorn is recommended.
4. Due to testing errors, `DATABASES` configuration is adjusted to switch between SQLite and PostgreSQL:

```python
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),  # This is the name of the PostgreSQL service defined in Docker Compose
            'PORT': os.environ.get('DB_PORT'),
        }
    }
```
